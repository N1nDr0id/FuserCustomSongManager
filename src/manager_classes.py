from program_enums import Genres, SongKey, SongMode

# NOTE: This script is part of the Fuser Custom Song Manager program. Its contents are here for both reference and for use within that program.

class Song:
    def __init__(self, short_name, song_name, artist, year, genre, key, mode, bpm, is_enabled, rating, notes, author):
        self.short_name = short_name
        self.song_name = song_name
        self.artist = artist
        self.year = year
        self.genre = genre
        self.key = key
        self.mode = mode
        self.bpm = bpm
        self.is_enabled = is_enabled
        self.rating = rating
        self.notes = notes
        self.author = author
    
    @classmethod
    def from_db(cls, tuple):
        #('Aerodynamic_P', 'Aerodynamic', 'Daft Punk', 2001, 7, 7, 0, 123)
                # short_name, song name, artist, year, genre, key, mode, bpm
        # if (tuple[8] == 0):
        #     return cls(tuple[0], tuple[1], tuple[2], tuple[3], Genres(tuple[4]), SongKey(tuple[5]), SongMode(tuple[6]), tuple[7], False, tuple[9], tuple[10])
        # elif (tuple[8] == 1):
        #     return cls(tuple[0], tuple[1], tuple[2], tuple[3], Genres(tuple[4]), SongKey(tuple[5]), SongMode(tuple[6]), tuple[7], True, tuple[8], tuple[9])
        return cls(tuple[0], tuple[1], tuple[2], tuple[3], Genres(tuple[4]), SongKey(tuple[5]), SongMode(tuple[6]), tuple[7], (tuple[8] == 1), tuple[9], tuple[10], tuple[11])

    def print(self):
        print(f"Short name: {self.short_name}")
        print(f"Song: {self.song_name}, Artist: {self.artist}, Year: {self.year}, Genre: {self.genre.name}")
        print(f"Key: {self.key.name}, Mode: {self.mode.name}, BPM: {self.bpm}")
        print(f"Enabled? {self.is_enabled}, Rating: {self.rating}")
        if (len(self.notes) != 0):
            print(f"Notes: {self.notes}")
        print(f"Author: {self.author}")

class ProgramProperties:
    def __init__(self, fuser_directory, database_location, launcher_type, executable_path):
        self.fuser_directory = fuser_directory
        self.pak_directory = self.fuser_directory + "\\Fuser\\Content\\Paks"
        self.database_location = database_location
        self.launcher_type = launcher_type
        self.executable_path = executable_path
        self.enabled_directory = self.pak_directory + "\\custom_songs"
        self.disabled_directory = self.pak_directory + "\\disabled_songs"
