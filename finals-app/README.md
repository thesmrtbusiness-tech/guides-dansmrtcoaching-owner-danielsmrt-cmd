# Finals (DanSmrtCoaching desktop app)

One place on your PC for each longform video: rendered video, title, description, thumbnail, tags, in YouTube publish order. It never uploads anything to YouTube.

## Setup (once)

1. Install Python from python.org/downloads (default options are fine). It is the only thing needed: the app uses nothing else, so there is no `pip install`.
2. Download this `finals-app` folder to somewhere permanent (e.g. `C:\DanSmrtFinals-app`).
3. Double-click **Install Finals Shortcut.bat**. A **Finals** shortcut appears on the desktop.

## Use

Double-click the **Finals** desktop shortcut. It opens in your browser at http://127.0.0.1:8765 (only this PC can reach it). Closing the tab leaves the app running quietly in the background; clicking the shortcut again just reopens the page.

Everything is stored in `C:\Users\<you>\DanSmrtFinals\<video>\`:

```
video.mp4        copied as-is, no re-encoding, no size limit
thumbnail.jpg
data.json        title, description, tags (saved as you type)
```

**Open folder** and **Open file location** open Windows Explorer there, ready to drag into YouTube Studio.

The first run creates the Cortisol Belly entry and, if `cortisol-belly-thumbnail.jpg` is in your Downloads folder, copies it in as the thumbnail.

## Settings (optional environment variables)

`FINALS_DIR` (storage folder), `FINALS_PORT` (default 8765).
