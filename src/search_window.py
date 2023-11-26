import tkinter as tk
from tkinter import ttk

# NOTE: This script is part of the Fuser Custom Song Manager program. Its contents are here for reference and archival purposes.
# This script was created to get an idea of how the SearchDialog window should look.

window = tk.Tk()
tk.Label(window, text="Search by...", justify="left").pack(anchor='w')
main_frame = tk.Frame(window)
main_frame.pack()
notebook = ttk.Notebook(main_frame)
notebook.pack()

song_frame = tk.Frame(notebook)
artist_frame = tk.Frame(notebook)
year_frame = tk.Frame(notebook)
bpm_frame = tk.Frame(notebook)
genre_frame = tk.Frame(notebook)
song_frame.pack()
artist_frame.pack()
year_frame.pack()
bpm_frame.pack()
genre_frame.pack()

tk.Label(song_frame, text="Song name:").grid(row=0, column=0, sticky='w')
search_song_name_var = tk.StringVar()
search_song_name_entry = ttk.Entry(song_frame, textvariable=search_song_name_var)
search_song_name_entry.grid(row=0, column=1)

tk.Label(artist_frame, text="Artist name:").grid(row=0, column=0, sticky='w')
search_artist_name_var = tk.StringVar()
search_artist_name_entry = ttk.Entry(artist_frame, textvariable=search_artist_name_var)
search_artist_name_entry.grid(row=0, column=1)

tk.Label(year_frame, text="Released in/From:").grid(row=0, column=0, sticky='w')
tk.Label(year_frame, text="To (optional):").grid(row=1, column=0, sticky='w')
first_year_var = tk.StringVar()
second_year_var = tk.StringVar()
search_first_year_entry = ttk.Entry(year_frame, textvariable=first_year_var)
search_second_year_entry = ttk.Entry(year_frame, textvariable=second_year_var)
search_first_year_entry.grid(row=0, column=1)
search_second_year_entry.grid(row=1, column=1)

tk.Label(bpm_frame, text="From:").grid(row=0, column=0, sticky='w')
tk.Label(bpm_frame, text="To (optional):").grid(row=1, column=0, sticky='w')
first_bpm_var = tk.StringVar()
second_bpm_var = tk.StringVar()
search_first_bpm_entry = ttk.Entry(bpm_frame, textvariable=first_bpm_var)
search_second_bpm_entry = ttk.Entry(bpm_frame, textvariable=second_bpm_var)
search_first_bpm_entry.grid(row=0, column=1)
search_second_bpm_entry.grid(row=1, column=1)

tk.Label(genre_frame, text="Genre:").grid(row=0, column=0, sticky='w')
genre_var = tk.StringVar(value='Classical')
search_genre_combo = ttk.Combobox(genre_frame, state='readonly', textvariable=genre_var)
search_genre_combo['values'] = ('Classical', 'Country', 'Rock', 'LatinAndCaribbean', 'Pop', 'RnB', 'HipHop', 'Dance')
search_genre_combo.grid(row=0, column=1)

#tk.Button(artist_frame, text="OK").pack()

#(search by song name, artist name, year range, bpm range, genre type)

notebook.add(song_frame, text="Song Name")
notebook.add(artist_frame, text="Artist")
notebook.add(year_frame, text="Year")
notebook.add(bpm_frame, text="BPM Range")
notebook.add(genre_frame, text="Genre")


window.mainloop()
