#!/usr/bin/env python
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.constants import *
from tkcalendar import Calendar
import re


#Color palette
BLACK = "#0a0a0a"
WHITE = "#cccccc"
RED   = "#f08080"
DGRAY = "#808080"
GRAY  = "#b4b4b4"
LGRAY = "#e3e3e3"
GREEN = "#94d692"
TESTCLR = "#ff9900"

win_size: str = "" #Do not reasign directly

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
        ent_timer = tk.Entry(frame, bg=LGRAY, fg=BLACK, width=20, cursor="xterm", font=("Arial 12"))
        btn_set          = tk.Button(frame, text='<', command=self.calendar_popup, bg=GREEN, fg=BLACK, width=2, cursor="hand2", font=("Arial 9 bold"))
        #NOTE: potential problems with label's width (may move the buttons)
        lbl_time_left    = tk.Label(frame, text="0000 | 00:00", bg=GRAY, fg=BLACK, font="Arial 12 bold") 
        btn_reset        = tk.Button(frame, text='>', command=self.reset_timer, bg=RED, fg=BLACK, width=2, cursor="hand2", font=("Arial 9 bold"))
        separator        = ttk.Separator(frame, orient=HORIZONTAL)

        # get the size of the frame to set the apropriate size of the window
        win_size = re.split(r"[\+\-]", frame.winfo_geometry())[0]

        # place the widgets
        frame.grid(row=0, column=0, ipadx=1)
        ent_timer.grid(row=0, column=0, padx=5, pady=5, columnspan=3)
        btn_set.grid(row=1, column=0, padx=5, pady=5)
        lbl_time_left.grid(row=1, column=1, padx=5, pady=5)
        btn_reset.grid(row=1, column=2, padx=5, pady=5)
        separator.grid(row=2, column=0) #TODO: make the separator having the right length

    def calendar_popup(self) -> None:
        if (len(self.winfo_children()) < 2): # limit the quantity of popup windows to 1. Frame+1 topup = 2.
            popup_win = Toplevel(self)
            # popup_win.title("Calendar")
            popup_win.overrideredirect(True)
            popup_win.resizable(width=0, height=0)
            calen = Calendar(popup_win, selectmode="day")
            calen.grid(row=1, column=0, padx=0, pady=0)
            popup_win.geometry(f"250x185+{self.winfo_pointerx()-100}+{self.winfo_pointery()-100}")
    
    def reset_timer(self) -> None:
        print("Reset to do...")
        

 
root = Tk()
root.resizable(False, False)
root.title('Deadliner pre-alpha')
root.iconbitmap("deadliner.ico")
app = Application()
root.geometry(win_size.join("+500+500"))
app.config(padx=5, pady=5, bg=DGRAY)
app.mainloop()