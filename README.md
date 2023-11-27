# Fuser Custom Song Manager
 An all-in-one custom song manager for Fuser.
 
 More info to be added here soon!

 ### Building
 To build the application, you need PyInstaller downloaded. Then:

```shell
pyinstaller manager.py --onefile --windowed --icon=gui_icons/program_icon.ico --name="Fuser Custom Song Manager"
```

This will place "Fuser Custom Song Manager.exe" in the src/dist folder. Ensure the gui_icons folder and patched_dlc_metadata.json are placed alongside the .exe for the program to properly run.
