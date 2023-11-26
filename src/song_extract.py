import patoolib
import string
import random
import os
import sys
import shutil

# NOTE: This script is part of the Fuser Custom Song Manager program. Its contents are here for both reference and for use within that program.

def extract_song(archive_path, output_path):
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
    extract_directory_path = output_path + "\\" + temp_folder
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
        # copy to main path
        filename = os.path.basename(match)
        shutil.copyfile(match, output_path + "\\" + filename)

    # delete temp_folder
    shutil.rmtree(extract_directory_path)

