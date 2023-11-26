from enum import Enum

# NOTE: This script is part of the Fuser Custom Song Manager program. Its contents are here for both reference and for use within that program.

# for future reference:
# enum_var_name.value will return the integer associated with the given enum instance
    # for example, given a QueryType variable x set to QueryType.ARTIST, x.value will return 1
# EnumType(int) will return the enum associated with said integer
    # for example, QueryType(1) will return QueryType.ARTIST
# enum_var_name.name will return the name (i.e. Classical, Major, ARTIST) for a given enum instance
    # for example, given a QueryType variable x set to QueryType.ARTIST, x.name will return ARTIST

class Genres(Enum):
    Classical = 0
    Country = 1
    Rock = 2
    LatinAndCaribbean = 3
    Pop = 4
    RnB = 5
    HipHop = 6
    Dance = 7

class SongMode(Enum):
    Major = 0
    Minor = 1
    Num = 2

class SongKey(Enum):
    C = 0
    Db = 1
    D = 2
    Eb = 3
    E = 4
    F = 5
    Gb = 6
    G = 7
    Ab = 8
    A = 9
    Bb = 10
    B = 11
    Num = 12

class LauncherType(Enum):
    Steam = 0
    Epic = 1
    Local = 2