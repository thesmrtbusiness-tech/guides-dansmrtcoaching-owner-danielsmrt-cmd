$app = Split-Path -Parent $MyInvocation.MyCommand.Path
$lnk = Join-Path ([Environment]::GetFolderPath('Desktop')) 'Finals.lnk'
$s = (New-Object -ComObject WScript.Shell).CreateShortcut($lnk)
$s.TargetPath = 'wscript.exe'
$s.Arguments = '"' + (Join-Path $app 'Launch Finals.vbs') + '"'
$s.WorkingDirectory = $app
$s.IconLocation = (Join-Path $app 'icon.ico')
$s.Save()
