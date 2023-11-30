<h1 align="center">Fuser Custom Song Manager</h1>
<p align="center">
<img src="https://github.com/N1nDr0id/FuserCustomSongManager/blob/main/src/gui_icons/program_icon.png?raw=true" alt="Fuser CUstom Song Manager Icon">
</p>
<p align="center">
<i>An all-in-one custom song manager for Fuser.</i>
</p>

# Features
<ul>
  <li>Rate songs and add custom information like song authors and comments!<br><img src="https://github.com/N1nDr0id/FuserCustomSongManager/blob/main/docs/edit_song.gif?raw=true" alt="An example gif of adding metadata to a song in the program"></li>
  <li>Search by a variety of attributes, such as song name, artist, year and BPM ranges, and more!<br><img src="https://github.com/N1nDr0id/FuserCustomSongManager/blob/main/docs/search.gif?raw=true" alt="An example gif of searching for songs in the program"></li>
  <li>Add songs without ever needing to extract a zip file again!</li>
  <li>Delete troublesome songs, or temporarily disable songs and enable them later!</li>
  <li>Automatically delete customSongsUnlocked_P.pak and .sig when adding, deleting, or toggling songs, or launching the game from the manager!</li>
  <li>And more! (potentially)</li>
</ul>

### Note
<b><ins>PLEASE NOTE:</ins></b> No warranty is provided with use of this program. Please ensure that all of your songs are backed up elsewhere if you already have an existing custom song collection.

This program is intended for Windows only. Behavior may not be consistent on macOS or Linux.

Windows may prevent you from running this app due to it being rather new. You may have to allow the program through Windows Defender or choose to run the program if SmartScreen prevents it.

### Instructions
To run this program, downloaded the latest release from the Releases section, then unzip into a folder and run "Fuser Custom Song Manager.exe".

Also provided within this folder is "Fuser Custom Song Manager Console.exe". This version of the program displays a console alongside the app, which may help with determining issues should you run into any.

You can also choose to download the latest executable within the dist folder. NOTE: this version is typically in development and may not be ready for use.

### Building
To build the application, you need PyInstaller downloaded.

Then, if you don't already have it, you'll need to follow the steps in [this thread](https://github.com/pyinstaller/pyinstaller/issues/3013#issuecomment-363916070) to get PyInstaller to recognize what's required for patoolib (the library used for extracting archive files when adding songs).

Then:

```shell
pyinstaller "src/manager.py" --onefile --windowed --icon=src/gui_icons/program_icon.ico --name="Fuser Custom Song Manager"
```

This will place "Fuser Custom Song Manager.exe" in the src/dist folder. Ensure the gui_icons folder and patched_dlc_metadata.json are placed alongside the .exe for the program to properly run.

For the console version of this program, run:

```shell
pyinstaller "src/manager.py" --onefile --icon=src/gui_icons/program_icon.ico --name="Fuser Custom Song Manager Console"
```
