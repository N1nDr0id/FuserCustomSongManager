import glob
import struct
from PyPAKParser import PakParser
from program_enums import Genres, SongMode, SongKey
from manager_classes import Song
import os
import pathlib
import time
import sqlite3
from sqlite3 import Error
import list_ops
from patched_dlc_lists import get_metadata_for_patched_song
import shutil

#global debug constant
DEBUG = False

# NOTE: This script is part of the Fuser Custom Song Manager program. Its contents are here for both reference and for use within that program.
# Any attempts to run this script on its own may result in issues. Do not run this script on its own unless you know what you are doing.


patched_DLC_list = {'adoreyou', 'alittlerespect', 'alot', 
                    'alwaysontime', 'amongtheliving', 'animals', 
                    'apache', 'astronautintheocean', 'babyimjealous', 
                    'boombastic', 'bop', 'breakingme', 
                    'bringmetolife', 'buddyholly', 'burningdownthehouse', 
                    'circles', 'concalma', 'countingstars', 
                    'cradles', 'crankdat', 'crystalbeach', 
                    'dancingsnotacrime', 'daysahead', 'daysgoby', 
                    'djgotusfallinginlove', 'dontyoudare', 'dreams', 
                    'feelssogood', 'fireburning', 'followyou', 
                    'fridayiminlove', 'funkycoldmedina', 'gentleonmymind', 
                    'getbusy', 'golden', 'gravelpit', 
                    'grooveisintheheart', 'happier', 'headandheart', 
                    'herecomesthehotstepper', 'higher', 'hiphophooray', 
                    'holdingoutforahero', 'iloveit', 'ily', 
                    'imeltwithyou', 'imgonnabe', 'insideout', 
                    'ironic', 'juice', 'kingsandqueens', 
                    'kissandmakeup', 'latch', 'leavealittlelove', 
                    'letslove', 'levitating', 'lifeisahighway', 
                    'lights', 'linger', 'lipslikesugar', 
                    'livinlavidaloca', 'lococontigo', 'lookwhatyouvedone', 
                    'looppack01', 'looppack07', 'looppack11', 
                    'looppack12', 'low', 'lowrider', 
                    'maneater', 'manoftheyear', 'maps', 
                    'maskoff', 'megusta', 'montero', 
                    'mood', 'mrbrightside', 'murdershewrote', 
                    'myexsbestfriend', 'myheadandmyheart', 'newrules', 
                    'norolemodelz', 'nothingbreakslikeaheart', 'numb', 
                    'onething', 'pidelimon', 'poison', 
                    'redlights', 'renegades', 'rockyourbody', 
                    'rosesimanbek', 'royceplease', 'rumors', 
                    'sandstorm', 'savage', 'selfesteem', 
                    'sevennationarmy', 'shedrivesmecrazy', 'shookonesptii', 
                    'shouldistayorshouldigo', 'smokeonthewater', 'sourcandy', 
                    'starships', 'stay', 'stronger', 
                    'superfreak', 'taintedlove', 'takeovercontrol', 
                    'takeyoudancing', 'thebusiness', 'thegamegotyou', 
                    'thenightporter', 'thereforeiam', 'thisishow', 
                    'toomuch', 'trapqueen', 'tubthumping', 
                    'unanochemas', 'unbelievable', 'unforgettable', 
                    'venus', 'walkingonsunshine', 'weliketoparty', 
                    'wellerman', 'whatifs', 'whatislove', 
                    'whatspoppin', 'wherethemgirlsat', 'whineup', 
                    'whoompthereitis', 'xotourllif3', 'youngdumbandbroke', 
                    'yourlove9pm'}

# Most of the wizardry going on in this function is credited to NarrikSynthfox. Thank you!!
def get_metadata(output_bin_name, reg_data, uexp_data, should_save_output, debug_print):
    if debug_print:
        print("BEGIN get_metadata")
    indata=reg_data
    offset=0

    def structread(str,len):
            nonlocal offset
            retval=struct.unpack(str,indata[offset:offset+len])
            offset+=len
            return retval
    #all offset+=number are always null and can be ignored

    usig=structread("BBBB",4) #signature, always (193,131,42,158)
    ver=structread("<I",4)[0] ^ 0xffffffff #version, xor'd with FFFFFFFF, result should be 6
    offset+=16
    fdiroffset=structread("<I",4)[0] #file directory offset?
    unk1=structread("<I",4)[0]
    pn=structread("<I",4)[0]
    offset+=4
    unk2=structread("B",1)[0] #should be 128
    num_names=structread("<I",4)[0]
    off_names=structread("<I",4)[0]
    offset+=8
    num_exp=structread("<I",4)[0]
    off_exp=structread("<I",4)[0]
    num_imp=structread("<I",4)[0]
    off_imp=structread("<I",4)[0]
    offset+=20
    guidhash=structread("BBBBBBBBBBBBBBBB",16) #16 byte guid hash, probably not needed
    unk3=structread("<I",4)[0] # 1
    unk4=structread("<I",4)[0] # 1 or 2
    unk5=structread("<I",4)[0] # same as number of names?
    offset+=36
    unk6=structread("<I",4)[0]
    offset+=4
    padding_offset=structread("<I",4)[0]
    flen=structread("<I",4)[0] # file length + 4, but seems to sometimes be unknown length/offset
    offset+=12
    unk7=structread("<i",4)[0]
    fdataoffset=structread("<I",4)[0]

    names=[[]]*num_names
    for name in range(num_names):
        strlen=structread("<I",4)[0]
        strdata=indata[offset:offset+strlen]
        offset+=strlen
        flags=structread("<I",4)[0]

        names[name]=(strlen,strdata,flags)
    imports=[[]]*num_imp
    for imp in range (num_imp):
        parent_nameid=names[structread("<Q",8)[0]][1][:-1]
        class_id=names[structread("<Q",8)[0]][1][:-1]
        parent_importid=structread("<I",4)[0]^0xffffffff
        nameid=names[structread("<I",4)[0]][1][:-1]
        unkid=structread("<I",4)[0]
        imports[imp]=[parent_nameid,class_id,parent_importid,nameid,unkid]
    exports=[b'']*num_exp
    for exp in range(num_exp):
        exports[exp]=indata[offset:offset+100]
        offset+=100
    offset+=4
    indatauexp=uexp_data
    offsetuexp=0

    def structreaduexp(str,len):
        nonlocal offsetuexp
        retval=struct.unpack(str,indatauexp[offsetuexp:offsetuexp+len])
        offsetuexp+=len
        return retval

    uexp_data=[]


    while offsetuexp<=len(indatauexp):
        nameid=names[structreaduexp("<Q",8)[0]][1][:-1]
        # quit once we hit IsStreamOptimized, we don't use this data (yet?)
        if (nameid == b'IsStreamOptimized'):
            break
        if debug_print:
            print(nameid)
        if nameid==b'None':
            try:
                nameid=names[structreaduexp("<Q",8)[0]][1][:-1]
            except:
                break
        classid=names[structreaduexp("<Q",8)[0]][1][:-1]
        
        if debug_print:
            print(nameid, classid)
        lendata=structreaduexp("<Q",8)[0]
        propdata=[]
        if classid==b'NameProperty':
            offsetuexp+=1
            name=names[structreaduexp("<I",4)[0]]
            nameunk=structreaduexp("<I",4)[0]
            propdata=[name,nameunk]
        elif classid==b'SoftObjectProperty':
            offsetuexp+=1
            name=names[structreaduexp("<I",4)[0]]
            value=structreaduexp("<Q",8)[0]
            propdata=[name,value]
        elif classid==b'TextProperty':
            offsetuexp+=1
            flag=structreaduexp("<i",4)[0]
            historytype=structreaduexp("<b",1)[0]
            strings=[]
            if historytype == -1:
                numstr=structreaduexp("<i",4)[0]
                for i in range(numstr):
                    strlen=structreaduexp("<i",4)[0]
                    if strlen<0:
                        strlen=strlen*-2
                        u16str=indatauexp[offsetuexp:offsetuexp+strlen]
                        #print(u16str.decode('utf-16'))
                        #strings.append(u16str.decode('utf-16'))
                        strings.append((u16str, 'utf-16'))
                    else:
                        #print(indatauexp[offsetuexp:offsetuexp+strlen].decode('utf-8'))
                        #strings.append(indatauexp[offsetuexp:offsetuexp+strlen].decode('utf-8'))
                        strings.append((indatauexp[offsetuexp:offsetuexp+strlen], 'utf-8'))
                    offsetuexp+=strlen
            propdata=[flag,historytype,strings]
        elif classid==b'EnumProperty':
            enumType=names[structreaduexp("<Q",8)[0]]
            offsetuexp+=1            
            enumValue=names[structreaduexp("<Q",8)[0]]
            propdata=[enumType,enumValue]
        elif classid==b'IntProperty':
            offsetuexp+=1
            propdata=structreaduexp("<i",4)[0]
        elif classid==b'ArrayProperty':
            aclass=names[structreaduexp("<Q",8)[0]][1][:-1]
            offsetuexp+=1
            num_values=structreaduexp("<I",4)[0]
            values=[]
            if aclass==b'ObjectProperty':
                for i in range(num_values):
                    values.append(imports[structreaduexp("<I",4)[0]^0xffffffff])
            elif aclass==b'FloatProperty':
                for i in range(num_values):
                    values.append(structreaduexp("<f",4)[0])
            elif aclass==b'SoftObjectProperty':
                for i in range(num_values):
                    offsetuexp+=1
                    name=names[structreaduexp("<I",4)[0]]
                    value=structreaduexp("<Q",8)[0]
                    values.append([name,value])
                offsetuexp-=1
            propdata=[aclass,num_values,values]
        elif classid==b'ObjectProperty':
            offsetuexp+=1
            propdata=imports[structreaduexp("<I",4)[0]^0xffffffff]
        elif classid==b'StructProperty':
            curoffset=offsetuexp
            structclass=names[structreaduexp("<Q",8)[0]][1][:-1]
            structvalues=[]
            if structclass==b'Transposes':
                offsetuexp+=1
                guid=indatauexp[offsetuexp:offsetuexp+16]
                offsetuexp+=16
                while offsetuexp<=curoffset+lendata:
                    key=names[structreaduexp("<Q",8)[0]][1][:-1]
                    offsetuexp+=8
                    value=structreaduexp("<i",4)[0]
                    offsetuexp+=9
                    structvalues.append([key,value])
            propdata=structvalues
        elif classid==b'mReferencedChildAssets':
            reftype=names[structreaduexp("<Q",8)[0]][1][:-1]
            if debug_print:
                print(reftype)
            if reftype==b'HmxMidiFileAsset':
                if debug_print:
                    print(names[structreaduexp("<Q",8)[0]])
                offsetuexp+=1
                if debug_print:
                    print(names[structreaduexp("<I",4)[0]][1][:-1])
                    print(imports[structreaduexp("<I",4)[0]^0xffffffff])
                    print(imports[structreaduexp("<I",4)[0]^0xffffffff])
                    print(structreaduexp("<i",4)[0])
                    print(structreaduexp("<i",4)[0])
                    print(structreaduexp("<i",4)[0])
                    print(structreaduexp("<i",4)[0])
                    print(structreaduexp("<i",4)[0])
        curdata=[nameid,classid,lendata,propdata]
        uexp_data.append(curdata)
        if should_save_output:
            temp = open(f'{output_bin_name}_out2.bin','wb')
            temp.write(indatauexp[offsetuexp:])
            temp.close()
    if should_save_output:
        output=open(f'{output_bin_name}_out.txt','w')
        for thing in uexp_data:
            output.write(str(thing)+"\n")
        output.close()
    if debug_print:
        print("END get_metadata")
    return uexp_data

# Searches the given directory recursively (including looking through subdirectories) and finds the directory for the first instance of a given file
def get_folder_path_to_file(file_name, directory_to_search):
    base_file_name = os.path.basename(file_name) # just to ensure filename is actually base file name
    extension = pathlib.Path(base_file_name).suffix
    #print("searching for, in:")
    #print(base_file_name, directory_to_search)
    path = glob.escape(directory_to_search) + f"\\**\\*{extension}"
    for file in glob.glob(path, recursive=True):
        if os.path.basename(file) == base_file_name:
            #print("Path:", os.path.dirname(file))
            return os.path.dirname(file)
        
    # if the file couldn't be found, return None
    return None

# Using get_metadata, we get the metadata for a given song file and return said data as a Song object.
def get_song_info(file_location, is_enabled, debug_print):
    if debug_print:
        print("BEGIN get_song_info")
        print("FILE TO GET DATA FROM:")
        print(file_location)
    #short_name = pak_name[:-6]
    #file_location = pak_directory + "\\" + short_name + "_P.pak"
    short_name = os.path.basename(file_location)[:-6]
    if (debug_print):
        print("SHORT NAME:")
        print(short_name)

    # check if short_name is in list of patched DLC songs
    # if so, just get appropriate data from premade list and return that song data
    if short_name in patched_DLC_list:
        if debug_print:
            print("GETTING METADATA FOR PATCHED SONG")
        return get_metadata_for_patched_song(short_name)

    with open(file_location, "rb") as pak_file:
        try:
            if debug_print:
                print("GETTING DATA USING PYPAKPARSER")
            PP = PakParser(pak_file)
            #for item in PP.List():
                #print(item)
            #asset = "DLC/Songs/whales_hail_mary_mallon/Meta_whales_hail_mary_mallon.uasset"
            reg_asset = f"DLC/Songs/{short_name}/Meta_{short_name}.uasset"
            if debug_print:
                print("UNPACKING ASSET " + reg_asset)
            reg_asset_data = PP.Unpack(reg_asset).Data
            reg_asset_uexp = f"DLC/Songs/{short_name}/Meta_{short_name}.uexp"
            if debug_print:
                print("UNPACKING UEXP ASSET " + reg_asset_uexp)
            reg_asset_uexp_data = PP.Unpack(reg_asset_uexp).Data
            if debug_print:
                print("REG ASSET DATA:")
                print(reg_asset_data)
                print()
            bs_asset = f"Audio/Songs/{short_name}/{short_name}bs/Meta_{short_name}bs.uasset"
            if debug_print:
                print("UNPACKING BS ASSET " + bs_asset)
            bs_asset_data = PP.Unpack(bs_asset).Data
            bs_asset_uexp = f"Audio/Songs/{short_name}/{short_name}bs/Meta_{short_name}bs.uexp"
            if debug_print:
                print("UNPACKING BS UEXP ASSET " + bs_asset_uexp)
            bs_asset_uexp_data = PP.Unpack(bs_asset_uexp).Data
            if debug_print:
                print("BS ASSET DATA:")
                print(bs_asset_data)

            # start metadata.py
            data_final = get_metadata(short_name, reg_asset_data, reg_asset_uexp_data, False, debug_print=debug_print)
            if debug_print:
                print("DATA FINAL:")
                for item in data_final:
                    print(item)
            #print("---REGULAR ASSET DONE---")
            song_artist = data_final[3][3][2][0][0].decode(data_final[3][3][2][0][1])[:-1] # artist
            #song_artist = data_final[3][3][2][0]
            song_genre = data_final[4][3][1][1][8:-1].decode() # genre
            #print(type(song_genre))
            song_year = data_final[5][3] # year
            if debug_print:
                print("SONG DATA:")
                print(song_artist)
                print(Genres[song_genre])
                print(song_year)
                print(len(data_final))
                print("---REGULAR ASSET DONE---")
            data_final_2 = get_metadata(f"{short_name}_2", bs_asset_data, bs_asset_uexp_data, False, debug_print=debug_print)
            if debug_print:
                print("---BS ASSET DONE---")
                for item in data_final_2:
                    print(item)
            song_title = data_final_2[2][3][2][0][0].decode(data_final_2[2][3][2][0][1])[:-1] # title
            song_bpm = data_final_2[8][3]
            song_mode = data_final_2[14][3][1][1].decode()[10:-1]
            song_key = data_final_2[3][3][1][1].decode()[6:-1]

            # print song info
            #print(f"Song: {song_title}, Artist: {song_artist}, Year: {song_year}")
            #print(f"Key: {song_key}, Mode: {song_mode}, BPM: {song_bpm}")
            #print()
            new_song = Song(short_name + "_P", song_title, song_artist, song_year, Genres[song_genre], SongKey[song_key], SongMode[song_mode], song_bpm, is_enabled, 0, "", "")
            if debug_print:
                print("RETURN SONG INFO:")
                new_song.print()
                print("END get_song_info")
            return new_song
            #print(song_title, SongKey[song_key], SongMode[song_mode], song_bpm)
        except AssertionError as e:
            print("ASSERT ERROR")
            print("is enabled?", is_enabled)
            new_song = Song(short_name + "_P", "Unknown", "Unknown", 0, Genres.Classical, SongKey.Num, SongMode.Num, 0, is_enabled, 0, "An assertion error occurred with this song. Please get in touch with the developer to resolve this issue.", "Unknown")
            if debug_print:
                print("RETURN SONG INFO:")
                new_song.print()
                print("END get_song_info")
            return new_song

# Returns a list of unique .pak file names, sorted alphabetically(?)
def get_pak_file_names(directory):
    pak_list = glob.glob(f'{glob.escape(directory)}\\**\\*.pak', recursive=True)
    print("Pak names:")
    for i in range(len(pak_list)):
        pak_list[i] = os.path.basename(pak_list[i])[:-4]
        print(pak_list[i])
    #print(pak_list)
    return pak_list

# SQLite helper functions
def create_db_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_db_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' has occurred")
        print("Query: ")
        print(query)

def execute_db_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' has occurred")
        print("Query: ")
        print(query)

# Takes in a song object and inserts said song into the database with a db query
def insert_song_into_db(connection, song):
    if DEBUG:
        print("BEGIN insert_song_into_db")
    # find and replace all single quotes in short_name, song_name, artist, and notes
    # replace single quotes with two single quotes
    new_song_db_query = f"""
    INSERT INTO songs VALUES (
    '{song.short_name.replace("'", "''")}',
    '{song.song_name.replace("'", "''")}',
    '{song.artist.replace("'", "''")}',
    '{song.year}',
    '{song.genre.value}',
    '{song.key.value}',
    '{song.mode.value}',
    '{song.bpm}',
    '{int(song.is_enabled)}',
    '{song.rating}',
    '{song.notes.replace("'", "''")}',
    '{song.author.replace("'", "''")}'
    );
    """
    #print(new_song_db_query)
    execute_db_query(connection, new_song_db_query)
    if DEBUG:
        print("END insert_song_into_db")

# Loops through a given directory and inserts each song in said directory into the database
def create_db_from_files(pak_directory, db_connection, is_disabled_directory, disabled_directory_path):
    #print("IN CREATE DB FROM FILES")
    if DEBUG:
        print("BEGIN create_db_from_files")
        print("PAK directory to search through:")
        print(pak_directory)
        print("Disabled directory:")
        print(disabled_directory_path)
    path = f'{glob.escape(pak_directory)}\\**\\*.pak'
    if DEBUG:
        print("PATH TO SEARCH:")
        print(path)
    #print(path)
    pak_list = glob.glob(path, recursive=True)
    pak_files = []
    print("Pak files:")
    for item in pak_list:
        #pak_files.append(os.path.basename(item))
        pak_files.append(item)
        print(item)
        
    for i in range(len(pak_files)):
    #for i in range(10):
        #print(pak_files[i])
        sig_file = pak_files[i][:-3] + "sig"
        #print("SIG FILE TO LOOK FOR: ", sig_file)
        if not os.path.exists(sig_file):
            print("The file \n" + pak_files[i] + "\nis missing the requisite .sig file\n" + sig_file + ".\nEnsure this .sig file exists and run program again to allow for song to be enabled.\nThis song has been disabled for now.")
            #is_disabled_directory = True
            song_subfolders = os.path.dirname(pak_files[i])[len(disabled_directory_path) + 1:]
            if (not is_disabled_directory):
                song_subfolders = os.path.dirname(pak_files[i])[len(pak_directory) + 1:]
                dest_path = disabled_directory_path + "\\" + song_subfolders
                pathlib.Path(dest_path).mkdir(parents=True, exist_ok=True)
                shutil.move(pak_files[i], dest_path + "\\" + os.path.basename(pak_files[i]))
            song = get_song_info(disabled_directory_path + "\\" + song_subfolders + "\\" + os.path.basename(pak_files[i]), is_enabled=False, debug_print=DEBUG)
            insert_song_into_db(db_connection, song)
            continue
            #continue
        song = get_song_info(pak_files[i], not is_disabled_directory, debug_print=DEBUG)
        #song.print()
        if is_disabled_directory:
            song.is_enabled = False

        insert_song_into_db(db_connection, song)
    if DEBUG:
        print("END create_db_from_files")
    #db_connection.commit()

# Gets the newest modified date of a given folder and all subfolders within
def get_newest_subfolder_date(base_folder):
    if DEBUG:
        print("BEGIN get_newest_subfolder_date")
    sub_path_dates = []
    sub_path_dates.append(pathlib.Path(base_folder).stat().st_mtime)
    for (root, dirs, files) in os.walk(base_folder):
        for dir in dirs:
            #print(root, dir)
            #for file in files:
                #print(file)
            sub_path_dates.append(pathlib.Path(root + "\\" + dir).stat().st_mtime)
    if DEBUG:
        print("END get_newest_subfolder_date")
    return max(sub_path_dates)

# Initializes the database, creating the main table as needed, etc.
def init_database(database_location, pak_directory, disabled_directory, force_update):
    if DEBUG:
        print("BEGIN init_database")
    db_folder_path = os.path.dirname(database_location)
    pathlib.Path(db_folder_path).mkdir(parents=True, exist_ok=True)
    if DEBUG:
        print("DATABASE FOLDER PATH:")
        print(db_folder_path)
        print("PAK DIRECTORY (custom songs folder):")
        print(pak_directory)
        print("DISABLED SONGS DIRECTORY:")
        print(disabled_directory)
        print("FORCE UPDATE?")
        print(force_update)
    connection = create_db_connection(database_location)
    # if database exists, load it into memory
    # check if new songs exist (i.e. compare files in pak directory to files in database. if not an exact match, refresh database (define this later))
    # else, create a new database and start loading songs from pak directory, converting them into
    # read all files from pak directory and place them in database
    # if the database already exists, skip loading it
    
    query = """
    CREATE TABLE IF NOT EXISTS songs (
    filename TEXT PRIMARY KEY,
    name TEXT,
    artist TEXT,
    year INTEGER,
    genre INTEGER,
    key INTEGER,
    mode INTEGER,
    bpm INTEGER,
    enabled INTEGER,
    rating INTEGER,
    notes TEXT,
    author TEXT
    );
    """
    execute_db_query(connection, query)

    # check here to see if new files exist compared to database's last modified time
    # INSTEAD get last modified date of pak_directory itself
    #newest_file_date = get_newest_file_date(pak_directory)


    # ensure folders exist before trying to use them
    pathlib.Path(pak_directory).mkdir(parents=True, exist_ok=True)
    #pak_date = pathlib.Path(pak_directory).stat().st_mtime
    pak_date = get_newest_subfolder_date(pak_directory)
    pathlib.Path(disabled_directory).mkdir(parents=True, exist_ok=True)
    #disabled_date = pathlib.Path(disabled_directory).stat().st_mtime
    disabled_date = get_newest_subfolder_date(disabled_directory)
    newest_file_date = max(pak_date, disabled_date)
    # comparing both modified and creation time. in some cases, creation time can be more recent than modified time
    # notably, this happens when copying a file from one location to another
    db_date = max(pathlib.Path(database_location).stat().st_mtime, pathlib.Path(database_location).stat().st_ctime)
    # check if db is empty via sql query, or if newest file date is newer than db_date
    new_files_exist = True if (newest_file_date > db_date) else False
    if (force_update):
        new_files_exist = True
    #print(new_files_exist)
    number_of_songs = execute_db_read_query(connection, "SELECT count(*) FROM songs")[0][0]
    #new_files_exist = True
    # get number of items from database
    if (number_of_songs == 0):
        if DEBUG:
            print("NO SONGS FOUND, INIT FROM FILES")
        create_db_from_files(pak_directory, connection, False, disabled_directory)
        create_db_from_files(disabled_directory, connection, True, disabled_directory)
        return connection
    if (new_files_exist):
        if DEBUG:
            print("SONGS FOUND, ADDING NEW SONGS")
        # clear existing database and rebuild
        #execute_db_query(connection, "DELETE FROM songs;")

        db_song_list = execute_db_read_query(connection, "SELECT filename FROM songs")
        for i in range(len(db_song_list)):
            db_song_list[i] = db_song_list[i][0]
        
        enabled_songs_in_dir = get_pak_file_names(pak_directory)
        disabled_songs_in_dir = get_pak_file_names(disabled_directory)

        new_enabled_songs = list_ops.difference(enabled_songs_in_dir, db_song_list)

        broken_enabled_songs = []

        # for each song in new_enabled_songs, add to db
        for song_item in new_enabled_songs:
            # get file path associated with said song
            file_path = get_folder_path_to_file(song_item + ".pak", pak_directory)
            sig_file = file_path + "\\" + song_item + ".sig"
            if not os.path.exists(sig_file):
                # attempt at handling subfolders

                # print("The file \n" + song_item + ".pak\nis missing the requisite .sig file\n" + sig_file + ".\nEnsure this .sig file exists and run program again to allow for song to be enabled.\nThis song has been disabled for now.")
                # # handle potential subfolder for item
                # new_path = disabled_directory + "\\" + os.path.basename(file_path)
                # #print("BASENAME:", os.path.basename(file_path))
                # #print("FIRST NEWPATH:", new_path)
                # subfolder = ""
                # if (file_path != pak_directory):
                #     subfolder = file_path[len(pak_directory)+1:]
                #     #print("SUBFOLDER = ", subfolder)
                #     #print(disabled_directory + "\\" + subfolder)
                #     pathlib.Path(disabled_directory + "\\" + subfolder).mkdir(parents=True, exist_ok=True)
                #     new_path = disabled_directory + "\\" + subfolder
                
                # #print("NEW PATH =", new_path)
                # #print("FILE TO MOVE:", file_path + "\\" + song_item + ".pak")
                # shutil.move(file_path + "\\" + song_item + ".pak", new_path)
                # song = get_song_info(new_path + "\\" + song_item + ".pak", False, False)
                # song.is_enabled = False
                # song.print()
                # insert_song_into_db(connection, song)

                # current implementation
                broken_enabled_songs.append(song_item)
                print("The file \n" + song_item + ".pak\nis missing the requisite .sig file\n" + sig_file + ".\nEnsure this .sig file exists and run program again to allow for song to be enabled.\nThis song has been disabled for now.")
                song_subfolders = file_path[len(pak_directory)+1:]
                song = None
                if (len(song_subfolders) > 0):
                    pathlib.Path(disabled_directory + "\\" + song_subfolders).mkdir(parents=True, exist_ok=True)
                    shutil.move(file_path + "\\" + song_item + ".pak", disabled_directory + "\\" + song_subfolders)
                    song = get_song_info(disabled_directory + "\\" + song_subfolders + "\\" + song_item + ".pak", is_enabled=False, debug_print=DEBUG)
                else:
                    shutil.move(file_path + "\\" + song_item + ".pak", disabled_directory + "\\" + os.path.basename(file_path))
                    song = get_song_info(disabled_directory + "\\" + song_item + ".pak", is_enabled=False, debug_print=DEBUG)
                song.print()
                insert_song_into_db(connection, song)
            else:
            #print("SONG IS IN ENABLED PATH")
                song_object = get_song_info(file_path + "\\" + song_item + ".pak", is_enabled=True, debug_print=DEBUG)
                insert_song_into_db(connection, song_object)
            db_song_list.append(song_item)

        for item in broken_enabled_songs:
            enabled_songs_in_dir.remove(item)
        
        new_disabled_songs = list_ops.difference(disabled_songs_in_dir, db_song_list)
        #print()
        for song_item in new_disabled_songs:
            #print(song_item + ".pak")
            #song_file_path = disabled_directory + "\\" + song_item + "_P.pak"
            file_path = get_folder_path_to_file(song_item + ".pak", disabled_directory)
            sig_file = file_path + "\\" + song_item + ".sig"
            if not os.path.exists(sig_file):
                print("The file \n" + song_item + ".pak\nis missing the requisite .sig file\n" + sig_file + ".\nEnsure this .sig file exists and run program again to allow for song to be enabled.\nThis song has been disabled for now.")
                song = get_song_info(file_path, is_enabled=False, debug_print=DEBUG)
                insert_song_into_db(connection, song)
            else:
                song_object = get_song_info(file_path + "\\" + song_item + ".pak", is_enabled=False, debug_print=DEBUG)
                insert_song_into_db(connection, song_object)
                
            db_song_list.append(song_item)

        # songs that exist locally and are in database after previous steps
        all_songs_in_dirs = list_ops.union(enabled_songs_in_dir, disabled_songs_in_dir)
        all_songs_in_dirs = list_ops.union(all_songs_in_dirs, broken_enabled_songs)
        if DEBUG:
            print("SONGS FOUND:")
            print(all_songs_in_dirs)
        # songs that only exist in database, may have more items than songs in dirs
        songs_only_in_db = list_ops.difference(db_song_list, all_songs_in_dirs)
        if DEBUG:
            print("SONGS IN DATABASE BUT NOT IN FILE SYSTEM:")
            print(songs_only_in_db)
        
        for song_item in songs_only_in_db:
            # if db_song_list[i] not in enabled_songs AND not in disabled_songs (covered by above statements)
            # delete row in songs where filename = db_song_list[i]
            execute_db_query(connection, f"DELETE FROM songs WHERE filename = '{song_item}'")

        for song_item in enabled_songs_in_dir:
            execute_db_query(connection, f"UPDATE songs SET enabled = 1 WHERE filename = '{song_item}'")

        for song_item in disabled_songs_in_dir:
            execute_db_query(connection, f"UPDATE songs SET enabled = 0 WHERE filename = '{song_item}'")

        for song_item in broken_enabled_songs:
            execute_db_query(connection, f"UPDATE songs SET enabled = 0 WHERE filename = '{song_item}'")

        #connection.commit()
        # rather than clearing out the database entirely, we check to see what needs to be added or removed.
        # to do this, we get the list of pak files in the pak directory (the unique song names), then compare that list to the existing songs in the database
        # for each song in the directory, if it doesn't exist in the database, create a new entry
        # after that, we search the other way around. i.e. for each song in the database, if it doesn't exist in the pak directory (or disabled directory), delete it from the database.

        # 1: if item in enabled_songs but not in overall db, add it.
        # 2: if item in disabled_songs but not in overall db, add it
        # 3: after that, if item in db but not in enabled_songs AND not in disabled_songs, delete from db
        # 4: after all of that, we ensure the enabled/disabled status of each song is updated in the database if a song has been moved

        # for the first step (finding songs that exist in the directory, but not database), should be able to do a left outer join on the file names,
        # as this will get a list of all items that are in the directory, but not the database.
        # for the second step, we do a right outer join on the file names (all items in database that aren't in directory)
        # NOTE: "directory" in this case would be the union of the enabled and disabled paths
        
    if DEBUG:
        print("END init_database")
    return connection

#print(get_newest_file_date(pak_directory))
#exit()

#start = time.time()

# Kept here for archival purposes. Not recommended to run this on its own.
def __main__():
    database_location = "G:\\Programming\\Python\\fuser_song_manager\\tests\\db\\songs.sqlite"
    pak_directory = "E:\\Steam\\SteamApps\\common\\Fuser\\Fuser\\Content\\Paks\\custom_songs"
    disabled_directory = pak_directory + "\\disabled_songs"
    db_connection = init_database(database_location, pak_directory, disabled_directory, False)


#__main__()
#print(f"Files in {pak_directory}:")
#print(pak_files)

#get_song_info("Gummibar_ImAGummyBear_P.pak", pak_directory, True)
#get_song_info("ush_yeah_P.pak", pak_directory, True)

# songs_test = execute_db_read_query(db_connection, "SELECT * from songs")
# all_songs = []
# for song_item in songs_test:
#     #print(song_item)
#     song = Song.from_db(song_item)
#     all_songs.append(song)
#     #song.print()

#end = time.time()
#print(f"Time elapsed: {end - start}")

# what we're looking for:
# in the BS asset: UEXP > Title > song title
# in the regular asset: UEXP > Artist > artist name, UEXP > Genre > translate this to genre text, UEXP > Year > year as int

# TODO:
# use the info collected from the songs to create a database (perhaps SQL or NoSQL?) (done)
# save that database (done)
# check on startup if files with newer dates exist compared to database (done)
# if so, rebuild database (done without rebuilding)
# otherwise, load database and add/remove to it as necessary (done)
# also add tags to each song to allow for it to be enabled/disabled (done)
# prompt user for a file location to store "disabled" songs
# when a song is disabled or enabled, check if customSongsUnlocked_P.pak and .sig exist. if so, delete them so they'll be rebuilt as necessary on launch

