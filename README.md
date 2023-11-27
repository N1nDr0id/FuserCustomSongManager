# Fuser Custom Song Manager
An all-in-one custom song manager for Fuser.
 
More info to be added here soon!

### Instructions
To run this program, downloaded the latest release from the Releases section, then unzip into a folder and run "Fuser Custom Song Manager.exe".

You can also choose to download the latest executable within the dist folder. NOTE: this version is typically in development and may not be ready for use.

### Building
To build the application, you need PyInstaller downloaded. Then:

```shell
pyinstaller manager.py --onefile --windowed --icon=gui_icons/program_icon.ico --name="Fuser Custom Song Manager"
```

This will place "Fuser Custom Song Manager.exe" in the src/dist folder. Ensure the gui_icons folder and patched_dlc_metadata.json are placed alongside the .exe for the program to properly run.
