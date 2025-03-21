#!/usr/bin/env python
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.constants import *
from tkcalendar import Calendar


#Color palette
BLACK = "#0a0a0a"
WHITE = "#cccccc"
RED   = "#f08080"
GRAY  = "#b4b4b4"
LGRAY = "#e3e3e3"


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, padx=5, pady=5, bg=GRAY)
        
        self.grid()
        self.createWidgets()
        # self.resizable(self, width=0, height=0) # TODO: figure out how to disable resizing

    def createWidgets(self):
        
        
        # SET WIDGETS
        # TODO: don't copypaste more timers, make it modulus with a function
        # Timer 1
        txt_1 = tk.Text()
        ent_1 = tk.Entry(self, bg=LGRAY, fg=BLACK, width=40)
        btn_1 = tk.Button(self, text='○', command=self.calendar_popup, bg=RED, fg=BLACK, width=2, cursor="hand2")
        calen = Calendar(self, selectmode="day")
        lbl_1 = tk.Label(self, text="0|00:00", fg=BLACK, width=20)
        sep_1 = ttk.Separator(self, orient=HORIZONTAL)

        ent_1.grid(row=0, column=0, padx=5, pady=10, columnspan=2)
        btn_1.grid(row=0, column=3, padx=5, pady=10)
        calen.grid(row=1, column=0, padx=5, pady=10)
        lbl_1.grid(row=1, column=1, padx=5, pady=10)
        sep_1.grid(row=2, column=0)

        # Timer 2

    def calendar_popup(self) -> None:
        popup_win = Toplevel(self)
        popup_win.title("Calendar")
        popup_win.geometry(f"100x100+{self.winfo_pointerx() - 100}+{self.winfo_pointery() - 100}")
        popup_win.resizable(width=0, height=0)
        calen = Calendar(popup_win, selectmode="day")
        calen.grid(row=1, column=0, padx=5, pady=10)

 
app = Application()
app.master.title('Deadliner')
# app.config(padx = 5, pady = 5)
app.mainloop()