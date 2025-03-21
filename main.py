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
DGRAY = "#808080"
GRAY  = "#b4b4b4"
LGRAY = "#e3e3e3"


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg=DGRAY)
        
        self.grid()
        self.createWidgets()
        

    def createWidgets(self):
        
        
        # SET WIDGETS
        # TODO: don't copypaste more timers, make it modulus with a function
        # Timer 1
        frame = Frame(self, bg=GRAY)
        ent_1 = tk.Entry(frame, bg=LGRAY, fg=BLACK, width=40, cursor="xterm")
        btn_1 = tk.Button(frame, text='○', command=self.calendar_popup, bg=RED, fg=BLACK, width=2, cursor="hand2")
        calen = Calendar(frame, selectmode="day")
        lbl_1 = tk.Label(frame, text="0|00:00", bg=GRAY, fg=BLACK, width=20)
        sep_1 = ttk.Separator(frame, orient=HORIZONTAL)

        frame.grid(row=0, column=0, ipadx=10, ipady=10)
        ent_1.grid(row=0, column=0, padx=5, pady=10, columnspan=2)
        btn_1.grid(row=0, column=3, padx=5, pady=10)
        calen.grid(row=1, column=0, padx=5, pady=10)
        lbl_1.grid(row=1, column=1, padx=5, pady=10)
        sep_1.grid(row=2, column=0)

        # Timer 2

    def calendar_popup(self) -> None:
        popup_win = Toplevel(self)
        popup_win.title("Calendar")
        popup_win.geometry(f"260x200+{self.winfo_pointerx() - 100}+{self.winfo_pointery() - 100}")
        popup_win.resizable(width=0, height=0)
        calen = Calendar(popup_win, selectmode="day")
        calen.grid(row=1, column=0, padx=5, pady=10)

 
root = Tk()
# root.geometry("480x900+200+200")
root.resizable(False, False)
root.title('Deadliner pre-alpha')
app = Application()
app.config(padx=5, pady=5, bg=DGRAY)
app.mainloop()