# From https://stackoverflow.com/questions/1966929/tk-treeview-column-sort

# NOTE: This script is part of the Fuser Custom Song Manager program. Its contents are here for both reference and for use within that program.

import tkinter as tk
import tkinter.ttk as ttk
from functools import partial

class MyTreeview(ttk.Treeview):
    def heading(self, column, sort_by=None, **kwargs):
        if sort_by and not hasattr(kwargs, 'command'):
            func = getattr(self, f"_sort_by_{sort_by}", None)
            if func:
                kwargs['command'] = partial(func, column, False)
        return super().heading(column, **kwargs)

    def _sort(self, column, reverse, data_type, callback):
        l = [(self.set(k, column), k) for k in self.get_children('')]
        l.sort(key=lambda t: data_type(t[0]), reverse=reverse)
        for index, (_, k) in enumerate(l):
            self.move(k, '', index)
        self.heading(column, command=partial(callback, column, not reverse))

    def _sort_by_num(self, column, reverse):
        self._sort(column, reverse, int, self._sort_by_num)

    def _sort_by_name(self, column, reverse):
        self._sort(column, reverse, str.casefold, self._sort_by_name)