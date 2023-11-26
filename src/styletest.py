from tkinter import *
from tkinter import ttk

# NOTE: This script is part of the Fuser Custom Song Manager program. Its contents are here for reference and archival purposes.

top=Tk() 

style = ttk.Style()
style.configure("BW.TLabel", foreground="black", background="white")
style.configure("BW.TFrame", foreground="red", background="blue")

frame = Frame(top, background="blue")

l1 = ttk.Label(frame, text="Test", style="BW.TLabel")
l1.grid()

style.configure('TEntry', background='#00ff00')
ent=ttk.Entry(frame)
ent.grid(row=2)

style.configure("TButton", background="orange")
l2 = ttk.Button(frame, text="Test Button", command=top.quit)
l2.grid(row=10)
frame.pack()

top.mainloop()