# This file contains data for songs that were previously official DLC for Fuser, but have been patched to work as custom songs instead.
# These patched DLC files have a different format compared to regular customs. This list of songs will also never change, given Fuser has been delisted (unless it somehow gets re-listed again).

# steps to make the list:
# first, extract all of the patched DLC songs into the custom_songs folder in Fuser
# load FModel and point it towards Fuser
# for each song, double click the song, right click on the topmost folder and click "save folder's packages properties (.json)"
# then, point this program towards 
    # E:\Steam\SteamApps\common\Fuser\FModel\Output\Exports\Fuser\Content\DLC\Songs\(songname)\Meta_(songname).json
# and
    # E:\Steam\SteamApps\common\Fuser\FModel\Output\Exports\Fuser\Content\DLC\Songs\(songname)\(songname)bs\Meta_(filename)bs.json
    # (this one may need to somehow check against files with different casings? unsure how to do this)
    # could handle the casing issue by just searching for the file that matches the pattern "Meta_*bs.json"

# within the first json file, all within Properties, pull out the values of these keys:
# Artist.CultureInvariantString
# Genre
# Year

# and from the second json file, all within Properties, pull out the values of these keys:
# Title.CultureInvariantString
# Key
# Mode
# BPM

import json
import glob
import os
from program_enums import Genres, SongKey, SongMode
from manager_classes import Song

# for songname in "E:\Steam\SteamApps\common\Fuser\FModel\Output\Exports\Fuser\Content\DLC\Songs"
    # get {songname}\Meta_{songname}.json
    # get appropriate contents from this file
    # get all files that match the pattern of {songname}\{songname}bs\Meta_*bs.json
    # for each of those files (should just be one), get appopriate contents for that file

def get_metadata_for_patched_song(songname):
    print(songname)
    # load patched_dlc_metadata.json
    # search for song with filename = songname
    # return song object with appropriate metadata

    f = open("patched_dlc_metadata.json")
    data = json.load(f)
    f.close()
    song_data = None
    for item in data:
        if item['filename'] == songname:
            song_data = item
            break
    print(item)
    #print(data)
    return_song = Song(songname + "_P", song_data['song_name'], song_data['song_artist'], song_data['song_year'], Genres[song_data['song_genre']], SongKey[song_data['song_key']], SongMode[song_data['song_mode']], song_data['song_bpm'], True, 3, "Patched DLC song", "Harmonix")
    return return_song



# start by just handling a single file
def create_patched_dlc_json():
    songs_path = "E:\\Steam\\SteamApps\\common\\Fuser\\FModel\\Output\\Exports\\Fuser\\Content\\DLC\\Songs"
    items = os.listdir(songs_path)
    song_folders = []
    #print(items)
    for item in items:
        if os.path.isdir(songs_path + "\\" + item):
            song_folders.append(item)
    #print(song_folders)

    #print(song_folders)
    #quit()

    song_objs = []
    for song in song_folders:
        #print("NEXT SONG:")
        song_path = songs_path + f"\\{song}\\Meta_{song}.json"
        f = open(song_path)

        data = json.load(f)
        props = data[0]['Properties']

        # artist name
        artist_name = props['Artist']['CultureInvariantString'] # artist name
        song_genre = Genres[props['Genre'][8:]] # song genre
        song_year = props['Year'] # year released

        f.close()

        song_bs_path = songs_path + f"\\{song}\\{song}bs\\Meta_*bs.json"
        song_bs_path = glob.glob(song_bs_path)[0]
        f = open(song_bs_path)

        data = json.load(f)
        props = data[0]['Properties']
        song_key = None
        song_mode = None
        song_bpm = None
        #print(props)
        song_name = props['Title']['CultureInvariantString'] # song name
        try:
            song_key = SongKey[props['Key'][6:]] # song key
        except KeyError:
            song_key = SongKey.C
        try:
            song_mode = SongMode[props['Mode'][10:]] # song mode
        except KeyError:
            song_mode = SongMode.Major
        try:
            song_bpm = props['BPM'] # BPM
        except KeyError:
            song_bpm = 120
        
        new_song_obj = Song(song, song_name, artist_name, song_year, song_genre, song_key, song_mode, song_bpm, True, 3, "Patched DLC song", "Harmonix")
        #new_song_obj.
        #new_song_obj.print()
        song_objs.append(new_song_obj)
        #print()

    # write data to json file
    dicts_list = []
    for song in song_objs:
        #song.print()
        dictionary = {
            "filename": song.short_name,
            "song_name": song.song_name,
            "song_artist": song.artist,
            "song_bpm": song.bpm,
            "song_genre": song.genre.name,
            "song_key": song.key.name,
            "song_mode": song.mode.name,
            "song_year": song.year
        }
        dicts_list.append(dictionary)
    #print(dicts_list)
    json_object = json.dumps(dicts_list, indent=4)
    with open("patched_dlc_metadata.json", "w") as outfile:
        outfile.write(json_object)


#create_patched_dlc_json()
#get_metadata_for_patched_song("boombastic").print()