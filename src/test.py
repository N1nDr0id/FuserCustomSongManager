#import tkinter as tk
#from tkinter import filedialog as fd
import os
import glob
import pathlib

# NOTE: This script is part of the Fuser Custom Song Manager program. Its contents are here for reference and archival purposes.

def get_folder_path_to_file(base_file_name, directory_to_search):
    path = directory_to_search + "\\**\\*.pak"
    for file in glob.glob(path, recursive=True):
        if os.path.basename(file) == base_file_name:
            return os.path.dirname(file)
        
def get_newest_subfolder_date(base_folder):
    sub_path_dates = []
    sub_path_dates.append(pathlib.Path(base_folder).stat().st_mtime)
    for (root, dirs, files) in os.walk(base_folder):
        for dir in dirs:
            print(root, dir)
            #for file in files:
                #print(file)
            sub_path_dates.append(pathlib.Path(root + "\\" + dir).stat().st_mtime)

    print(max(sub_path_dates))

#get_newest_subfolder_date("E:\\Steam\\SteamApps\\common\\Fuser\\Fuser\\Content\\Paks\\custom_songs")

#print(get_folder_path_to_file("JusShv_BuckBumbleTheme_P.pak", "E:\\Steam\\SteamApps\\common\\Fuser\\Fuser\\Content\\Paks\\custom_songs"))

# window = tk.Tk()

# def get_unique_files():
#     result = list(fd.askopenfilenames())
#     item_to_remove = "Fuser"
#     final_list = []
#     for i in range(len(result)):
#         file_name_no_ext = os.path.splitext(os.path.basename(result[i]))[0]
#         print(file_name_no_ext)
#         if (file_name_no_ext != item_to_remove):
#             final_list.append(result[i])
#     print(final_list)

# button = tk.Button(window, text="pick file", command=get_unique_files)
# button.pack()

# window.mainloop()