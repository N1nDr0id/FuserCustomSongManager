# From https://stackoverflow.com/questions/1966929/tk-treeview-column-sort

# NOTE: This script is part of the Fuser Custom Song Manager program. Its contents are here for both reference and for use within that program.

import tkinter as tk
import tkinter.ttk as ttk
from functools import partial
import list_ops

class MyTreeview(ttk.Treeview):
    def heading(self, column, sort_by=None, **kwargs):
        if sort_by and not hasattr(kwargs, 'command'):
            func = getattr(self, f"_sort_by_{sort_by}", None)
            if func:
                kwargs['command'] = partial(func, column, False)
        return super().heading(column, **kwargs)

    def _sort(self, column, reverse, data_type, callback):
        # Handles case where "The " and "A " should be ignored from the title of a song or artist name, similar to how Fuser itself handles sorting by song or artist name.
        if (data_type == "remove_the_a"):   
            # songs that start with "the"
            songs_the = [(self.set(k, column).casefold().replace('the ', '', 1), k) for k in self.get_children('') if self.set(k, column).casefold().startswith("the ")]
            # songs that start with "a"
            songs_a = [(self.set(k, column).casefold().replace('a ', '', 1), k) for k in self.get_children('') if self.set(k, column).casefold().startswith("a ")]
            # songs that simultaneously don't start with the and a
            songs_not_the_a =[(self.set(k, column).casefold(), k) for k in self.get_children('') if (not self.set(k, column).casefold().startswith("a ") and not self.set(k, column).casefold().startswith("the "))]
            # all songs, with the first occurances of "the " and "a " removed from their starts, depending on which one comes first
            l = list_ops.union(list_ops.union(songs_a, songs_the), songs_not_the_a)
            data_type = str.casefold
        else:
            l = [(self.set(k, column), k) for k in self.get_children('')]
        
        #print(l)
        l.sort(key=lambda t: data_type(t[0]), reverse=reverse)
        #print("SORT")
        for index, (_, k) in enumerate(l):
            #print(_, k)
            self.move(k, '', index)
        self.heading(column, command=partial(callback, column, not reverse))

    def _sort_by_num(self, column, reverse):
        self._sort(column, reverse, int, self._sort_by_num)

    def _sort_by_name(self, column, reverse):
        self._sort(column, reverse, str.casefold, self._sort_by_name)

    def _sort_by_name_ignore_words(self, column, reverse):
        self._sort(column, reverse, "remove_the_a", self._sort_by_name_ignore_words)