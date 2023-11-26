# NOTE: This script is part of the Fuser Custom Song Manager program. Its contents are here for both reference and for use within that program.

# from GeeksForGeeks:
def intersection(list1, list2):
    list3 = [value for value in list1 if value in list2]
    return list3

def union(list1, list2):
    return list(set(list1) | set(list2))

def difference(list1, list2):
    list3 = [value for value in list1 if value not in list2]
    return list3