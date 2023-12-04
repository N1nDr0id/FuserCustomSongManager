#import tkinter as tk
#from tkinter import filedialog as fd
import os
import glob
import pathlib
import psutil
import subprocess
import sys

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

def process_exists_2(process_name):
    process_list = {p.name() for p in psutil.process_iter(attrs=['name'])}
    if process_name in process_list:
        # do whatever you want
        print("Process found!")

def process_exists_3(process_name):
    progs = str(subprocess.check_output('tasklist'))
    if process_name in progs:
        return True
    else:
        return False
    
def check_for_updates():
    version_number = "v1.0.0"
    

startupinfo_hideconsole = subprocess.STARTUPINFO()
startupinfo_hideconsole.dwFlags |= subprocess.STARTF_USESHOWWINDOW

def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call, startupinfo=startupinfo_hideconsole).decode(encoding=sys.stdout.encoding)
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower()) 

process_to_find = "chrome.exe"
print(process_exists(process_to_find))
process_exists_2(process_to_find)
print(process_exists_3(process_to_find))

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