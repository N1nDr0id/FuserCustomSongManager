import patoolib
import string
import random
import os
import sys
import shutil
import pathlib
from loader import get_folder_path_to_file

# NOTE: This script is part of the Fuser Custom Song Manager program. Its contents are here for both reference and for use within that program.

def extract_song(archive_path, output_path, enabled_directory, disabled_directory, pak_directory):
    # pass in path to archive and desired output directory
    # create temp folder within output directory
    # archive_path = sys.argv[1]
    # output_path = sys.argv[2]
    if (not archive_path.endswith("zip") and not archive_path.endswith("rar") and not archive_path.endswith("7z")):
        #print(archive_file[-3:])
        print("not a valid archive, quitting")
        quit()
    #archive_file_path = main_path + "\\" + archive_file
    rand_string = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=5))
    temp_folder = "fuser_songmanager_temp" + rand_string
    extract_directory_path = pak_directory + "\\temp\\" + temp_folder
    pathlib.Path(extract_directory_path).mkdir(parents=True, exist_ok=True)
    patoolib.extract_archive(archive_path, outdir=extract_directory_path)

    # find pak and sig files
    # move them to main path
    # delete temp
    matches_pak = []
    matches_sig = []
    for root, dirnames, filenames in os.walk(extract_directory_path):
        for filename in filenames:
            if (filename.endswith(".pak")):
                matches_pak.append(os.path.join(root, filename))
            elif (filename.endswith(".sig")):
                matches_sig.append(os.path.join(root, filename))
    #print(matches)
    
    # ensure that we only copy items that have both a pak and sig file
    matches = []
    for pak_item in matches_pak:
        for sig_item in matches_sig:
            pak_filename = os.path.splitext(os.path.basename(pak_item))[0]
            sig_filename = os.path.splitext(os.path.basename(sig_item))[0]
            if pak_filename == sig_filename:
                matches.append(pak_item)
                matches.append(sig_item)


    for match in matches:
        print(match)
        # copy to main path
        filename = os.path.basename(match)
        print(filename)
        # if file exists in disabled directory, but we're trying to copy into enabled directory, disallow this
        if (output_path == enabled_directory and get_folder_path_to_file(filename, disabled_directory) != None):
            continue
        # if file exists in enabled directory, but we're trying to copy into disabled directory, disallow this
        if (output_path == disabled_directory and get_folder_path_to_file(filename, enabled_directory) != None):
            continue
        # if file exists in enabled directory and we're copying into enabled directory, copy to wherever file currently exists
        if (enabled_directory in output_path):
            folder_path = get_folder_path_to_file(filename, enabled_directory)
            if folder_path != None:
                subfolders = folder_path[len(enabled_directory) + 1:]
                shutil.copyfile(match, enabled_directory + "\\" + subfolders + "\\" + filename)
            else:
                shutil.copyfile(match, output_path + "\\" + filename)
        elif (disabled_directory in output_path):
            folder_path = get_folder_path_to_file(filename, disabled_directory)
            if folder_path != None:
                subfolders = folder_path[len(disabled_directory) + 1:]
                shutil.copyfile(match, disabled_directory + "\\" + subfolders + "\\" + filename)
            else:
                shutil.copyfile(match, output_path + "\\" + filename)

        

        #shutil.copyfile(match, output_path + "\\" + filename)

    # delete temp_folder
    shutil.rmtree(extract_directory_path)

