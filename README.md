# Fuser Custom Song Manager
An all-in-one custom song manager for Fuser.

### Note
PLEASE NOTE: No warranty is provided with use of this program. Please ensure that all of your songs are backed up elsewhere if you already have an existing custom song collection.

This program is intended for Windows only. Behavior may not be consistent on macOS or Linux.

Windows may prevent you from running this app due to it being rather new. You may have to allow the program through Windows Defender or choose to run the program if SmartScreen prevents it.

### Instructions
To run this program, downloaded the latest release from the Releases section, then unzip into a folder and run "Fuser Custom Song Manager.exe".

You can also choose to download the latest executable within the dist folder. NOTE: this version is typically in development and may not be ready for use.

### Building
To build the application, you need PyInstaller downloaded.

Then, if you don't already have it, you'll need to follow the steps in [this thread](https://github.com/pyinstaller/pyinstaller/issues/3013#issuecomment-363916070) to get PyInstaller to recognize what's required for patoolib (the library used for extracting archive files when adding songs).

Then:

```shell
pyinstaller "src/manager.py" --onefile --windowed --icon=src/gui_icons/program_icon.ico --name="Fuser Custom Song Manager"
```

This will place "Fuser Custom Song Manager.exe" in the src/dist folder. Ensure the gui_icons folder and patched_dlc_metadata.json are placed alongside the .exe for the program to properly run.
