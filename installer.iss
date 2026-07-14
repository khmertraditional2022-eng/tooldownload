[Setup]
; Basic Setup Information
AppName=ReelDownloader
AppVersion=1.0.0
AppPublisher=Your Company Name
DefaultDirName={autopf}\ReelDownloader
DefaultGroupName=ReelDownloader
UninstallDisplayIcon={app}\ReelDownloader.exe
Compression=lzma2
SolidCompression=yes
OutputDir=Output
OutputBaseFilename=ReelDownloader_Setup_v1.0.0
SetupIconFile=icon.ico

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Main Executable
Source: "dist\ReelDownloader.exe"; DestDir: "{app}"; Flags: ignoreversion

; FFmpeg Dependencies (REQUIRED FOR VIDEO DOWNLOADING)
; Important: Make sure ffmpeg.exe and ffprobe.exe are in the same folder as this .iss file before compiling!
Source: "ffmpeg.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "ffprobe.exe"; DestDir: "{app}"; Flags: ignoreversion

; Optional: Include cookies if needed
; Source: "cookies.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu Shortcut
Name: "{group}\ReelDownloader"; Filename: "{app}\ReelDownloader.exe"
; Desktop Shortcut
Name: "{autodesktop}\ReelDownloader"; Filename: "{app}\ReelDownloader.exe"; Tasks: desktopicon

[Run]
; Launch application after installation finishes
Filename: "{app}\ReelDownloader.exe"; Description: "{cm:LaunchProgram,ReelDownloader}"; Flags: nowait postinstall skipifsilent
