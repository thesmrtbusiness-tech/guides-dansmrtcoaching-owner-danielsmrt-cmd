#!/usr/bin/env python3
"""Finals: a local app that holds everything for each longform video.

Standard library only (no pip install). Serves on http://127.0.0.1:8765 and
stores each video in its own folder under ~/DanSmrtFinals/<slug>/:

    video.mp4  thumbnail.jpg  data.json   (files are copied in as-is)
"""
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

APP_DIR = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("FINALS_DIR") or Path.home() / "DanSmrtFinals")
PORT = int(os.environ.get("FINALS_PORT", "8765"))
HOSTS = {f"127.0.0.1:{PORT}", f"localhost:{PORT}"}

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
KINDS = {"video": ("video", VIDEO_EXTS), "thumbnail": ("thumbnail", IMAGE_EXTS)}
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
CHUNK = 1 << 20

SEED_SLUG = "cortisol-belly-cycle"
SEED_TITLE = "Inside the Cortisol Belly Cycle: What 10 Years Keeping 125 lbs Off Taught Me"
SEED_THUMB = "cortisol-belly-thumbnail.jpg"


def log(msg):
    try:
        ROOT.mkdir(parents=True, exist_ok=True)
        with open(ROOT / "finals.log", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
    except OSError:
        pass


def slugify(text):
    words = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return words[:50].rstrip("-") or "video"


def find_asset(folder, kind):
    stem, exts = KINDS[kind]
    for p in sorted(folder.glob(stem + ".*")):
        if p.suffix.lower() in exts:
            return p
    return None


def read_data(folder):
    try:
        with open(folder / "data.json", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        data = {}
    return {
        "title": str(data.get("title", "")),
        "description": str(data.get("description", "")),
        "tags": str(data.get("tags", "")),
        "created": data.get("created", folder.stat().st_mtime),
    }


def write_data(folder, data):
    tmp = folder / "data.json.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, folder / "data.json")


def asset_info(folder, kind):
    p = find_asset(folder, kind)
    if not p:
        return None
    st = p.stat()
    return {"name": p.name, "size": st.st_size, "mtime": int(st.st_mtime)}


def video_summary(folder):
    d = read_data(folder)
    return {"slug": folder.name, "title": d["title"], "created": d["created"]}


def video_detail(folder):
    d = read_data(folder)
    d.update(
        slug=folder.name,
        path=str(folder),
        video=asset_info(folder, "video"),
        thumbnail=asset_info(folder, "thumbnail"),
    )
    return d


def create_video(title):
    base = slugify(title)
    slug, n = base, 2
    while (ROOT / slug).exists():
        slug = f"{base}-{n}"
        n += 1
    folder = ROOT / slug
    folder.mkdir(parents=True)
    write_data(folder, {"title": title, "description": "", "tags": "", "created": time.time()})
    return folder


def seed():
    ROOT.mkdir(parents=True, exist_ok=True)
    folder = ROOT / SEED_SLUG
    if not any(p.is_dir() for p in ROOT.iterdir()):
        folder.mkdir()
        write_data(folder, {"title": SEED_TITLE, "description": "", "tags": "", "created": time.time()})
    # Pick up the locked thumbnail from Downloads if it has not been added yet.
    src = Path.home() / "Downloads" / SEED_THUMB
    if folder.is_dir() and not find_asset(folder, "thumbnail") and src.is_file():
        shutil.copyfile(src, folder / "thumbnail.jpg")


def open_in_explorer(path, select=False):
    if sys.platform == "win32":
        if select:
            subprocess.Popen(["explorer", f"/select,{path}"])
        else:
            os.startfile(str(path))
    elif sys.platform == "darwin":
        subprocess.Popen(["open", "-R", str(path)] if select else ["open", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path.parent if select else path)])


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "Finals"

    def log_message(self, fmt, *args):
        pass

    # ---- helpers -------------------------------------------------------
    def send_json(self, obj, status=200):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def fail(self, status, message, drop=False):
        # drop=True when the request body was not read, so the connection can't be reused.
        if drop:
            self.close_connection = True
        self.send_json({"error": message}, status)

    def read_json(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n > 5_000_000:
            raise ValueError("too large")
        return json.loads(self.rfile.read(n) or b"{}")

    def guard(self):
        """Reject requests that did not come from our own page (DNS rebinding / CSRF)."""
        if self.headers.get("Host") not in HOSTS:
            self.fail(403, "Forbidden", drop=True)
            return False
        if self.command != "GET":
            origin = self.headers.get("Origin")
            if origin not in {f"http://{h}" for h in HOSTS}:
                self.fail(403, "Forbidden", drop=True)
                return False
        return True

    def folder_for(self, slug, drop=False):
        if SLUG_RE.match(slug or ""):
            folder = ROOT / slug
            if folder.is_dir():
                return folder
        self.fail(404, "Video not found", drop=drop)
        return None

    # ---- routing -------------------------------------------------------
    def do_GET(self):
        if not self.guard():
            return
        url = urlparse(self.path)
        parts = [p for p in url.path.split("/") if p]
        if not parts:
            return self.serve_file(APP_DIR / "index.html")
        if parts == ["api", "videos"]:
            videos = [video_summary(p) for p in ROOT.iterdir() if p.is_dir() and SLUG_RE.match(p.name)]
            videos.sort(key=lambda v: v["created"], reverse=True)
            return self.send_json({"root": str(ROOT), "videos": videos})
        if len(parts) == 3 and parts[:2] == ["api", "videos"]:
            folder = self.folder_for(parts[2])
            return self.send_json(video_detail(folder)) if folder else None
        if len(parts) == 3 and parts[0] == "files" and parts[2] in KINDS:
            folder = self.folder_for(parts[1])
            if not folder:
                return
            asset = find_asset(folder, parts[2])
            if not asset:
                return self.fail(404, "No file yet")
            return self.serve_file(asset)
        self.fail(404, "Not found")

    def do_POST(self):
        if not self.guard():
            return
        url = urlparse(self.path)
        parts = [p for p in url.path.split("/") if p]
        if parts == ["api", "videos"]:
            try:
                title = str(self.read_json().get("title", "")).strip()
            except ValueError:
                return self.fail(400, "Bad request", drop=True)
            if not title:
                return self.fail(400, "Give the video a title first")
            return self.send_json(video_detail(create_video(title)), 201)
        if len(parts) == 4 and parts[:2] == ["api", "videos"] and parts[3] == "open":
            folder = self.folder_for(parts[2], drop=True)
            if not folder:
                return
            what = parse_qs(url.query).get("what", ["folder"])[0]
            if what == "folder":
                open_in_explorer(folder)
            elif what in KINDS and find_asset(folder, what):
                open_in_explorer(find_asset(folder, what), select=True)
            else:
                return self.fail(404, "No file yet")
            return self.send_json({"ok": True})
        self.fail(404, "Not found", drop=True)

    def do_PUT(self):
        if not self.guard():
            return
        url = urlparse(self.path)
        parts = [p for p in url.path.split("/") if p]
        if len(parts) < 3 or parts[:2] != ["api", "videos"]:
            return self.fail(404, "Not found", drop=True)
        folder = self.folder_for(parts[2], drop=True)
        if not folder:
            return
        if len(parts) == 3:
            try:
                body = self.read_json()
            except ValueError:
                return self.fail(400, "Bad request", drop=True)
            data = read_data(folder)
            for key in ("title", "description", "tags"):
                if key in body:
                    data[key] = str(body[key])
            write_data(folder, data)
            return self.send_json({"ok": True})
        if len(parts) == 4 and parts[3] in KINDS:
            return self.receive_file(folder, parts[3], parse_qs(url.query).get("name", [""])[0])
        self.fail(404, "Not found", drop=True)

    # ---- file transfer -------------------------------------------------
    def receive_file(self, folder, kind, name):
        """Stream the request body to disk untouched (no re-encoding, no size limit)."""
        stem, exts = KINDS[kind]
        ext = Path(name).suffix.lower()
        if ext not in exts:
            return self.fail(400, f"That file type isn't supported ({ext or 'no extension'}).", drop=True)
        try:
            length = int(self.headers.get("Content-Length") or "")
        except ValueError:
            return self.fail(411, "Missing file size", drop=True)
        if shutil.disk_usage(folder).free < length + (64 << 20):
            return self.fail(507, "Not enough free disk space for this file.", drop=True)

        tmp = folder / f"{stem}{ext}.part"
        remaining = length
        try:
            with open(tmp, "wb") as f:
                while remaining:
                    chunk = self.rfile.read(min(CHUNK, remaining))
                    if not chunk:
                        break
                    f.write(chunk)
                    remaining -= len(chunk)
        except OSError as e:
            tmp.unlink(missing_ok=True)
            return self.fail(500, f"Couldn't write the file: {e}", drop=True)
        if remaining:
            # Upload was cancelled or the connection dropped part-way.
            tmp.unlink(missing_ok=True)
            self.close_connection = True
            return

        try:
            old = find_asset(folder, kind)
            if old:
                old.unlink()
            os.replace(tmp, folder / f"{stem}{ext}")
        except OSError as e:
            tmp.unlink(missing_ok=True)
            return self.fail(409, f"Couldn't replace the old file (is it open in another program?): {e}")
        self.send_json(video_detail(folder))

    def serve_file(self, path):
        try:
            size = path.stat().st_size
        except OSError:
            return self.fail(404, "Not found")
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        start, end, status = 0, size - 1, 200
        rng = self.headers.get("Range")
        if rng:
            m = re.match(r"bytes=(\d*)-(\d*)$", rng.strip())
            if m and (m.group(1) or m.group(2)):
                s, e = m.groups()
                if s:
                    start = int(s)
                    end = min(int(e), size - 1) if e else size - 1
                else:
                    start = max(0, size - int(e))
                if start > end or start >= size:
                    self.send_response(416)
                    self.send_header("Content-Range", f"bytes */{size}")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                status = 206
        length = end - start + 1 if size else 0
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(length))
        self.send_header("Cache-Control", "no-cache")
        if status == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        try:
            with open(path, "rb") as f:
                f.seek(start)
                left = length
                while left > 0:
                    chunk = f.read(min(CHUNK, left))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    left -= len(chunk)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            self.close_connection = True


def main():
    seed()
    url = f"http://127.0.0.1:{PORT}/"
    try:
        server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    except OSError:
        # Already running: just bring up the page.
        webbrowser.open(url)
        return
    server.daemon_threads = True
    log(f"Finals running at {url}, storing in {ROOT}")
    if "--no-browser" not in sys.argv:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
