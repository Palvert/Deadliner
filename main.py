# TODO: make the time entry fields only accept numbers
# TODO: on start of the program timers appear on by one - it's ugly, need to fix somehow

import tkinter as tk
from tkinter import ttk
# from tkinter.constants import *
import tkcalendar as tkc
# from tkcalendar import Calendar, DateEntry
import re
import datetime
import sys


#Color palette
BLACK = "#0a0a0a"
WHITE = "#cccccc"
RED   = "#f08080"
DGRAY = "#808080"
GRAY  = "#b4b4b4"
LGRAY = "#e3e3e3"
GREEN = "#94d692"
TESTCLR = "#ff9900" # for debugging

# Style
font_1, font_1_size = "Arial\ Nova", " 12 "
font_2, font_2_size = "Arial", " 9 "
pdx, pdy = 3, 3

win_size: str = "" #Do not reassign directly
# timer_selected :int = -1
date_selected = ""
timers_quantity = 0
timers = []

timers_to_add = 1
if len(sys.argv) > 1:
    timers_to_add = int(sys.argv[1])


class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg=DGRAY)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        for n in range(timers_to_add):
            timers.append(Timer(self))
 

class Timer(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        global timers_quantity        
        global timers
        widgets = [
            # Frame            # 0
            # Title entry      # 1
            # Reset button     # 2
            # Date entry       # 3
            # Hours entry      # 4
            # : label          # 5
            # Minutes entry    # 6
            # Time left label  # 7
            # Separator(frame) # 8
        ]

        widgets.append(tk.Frame(self, background=GRAY))
        widgets.append(tk.Entry(widgets[0], 
                        bg=LGRAY, fg=BLACK, width=25, cursor="xterm", font=(font_1 + font_1_size), relief="flat"))
        widgets.append(tk.Button(widgets[0], 
                        text='ク', command=self.reset_timer, width=2,
                        bg=RED, fg=BLACK, cursor="hand2", font=(font_2 + font_1_size + "bold")))
        widgets.append(tkc.DateEntry(widgets[0], 
                        mindate=datetime.date.today(), date_pattern="dd.mm.yyyy", font=(font_1 + font_1_size)))
        widgets.append(tk.Entry(widgets[0],
                        bg="white", fg=BLACK, width=2, cursor="xterm", font=(font_1 + font_1_size)))
        widgets.append(tk.Label(widgets[0],
                        text=":", bg=GRAY, fg=BLACK, font=(font_1 + font_1_size)))
        widgets.append(tk.Entry(widgets[0],
                        bg="white", fg=BLACK, width=2, cursor="xterm", font=(font_1 + font_1_size)))
        widgets.append(tk.Label(widgets[0], 
                        text="0000 | 00:00", bg=GRAY, fg=BLACK, font=(font_1 + font_1_size + "bold")))
        # Add an improvised separator
        frame_x = int(re.split('x', widgets[0].winfo_geometry())[0])
        widgets.append(tk.Frame(widgets[0], bg=DGRAY, height=3, width=290))
        

        # place the widgets
        widgets[0].grid(row=timers_quantity, column=0, ipadx=1, ipady=2)
        widgets[1].grid(row=0, column=0, padx=pdx+4, pady=pdy, columnspan=6, sticky='w')
        widgets[2].grid(row=0, column=7, padx=pdx+6, pady=pdy, columnspan=3)
        widgets[3].grid(row=1, column=0, padx=pdx)
        widgets[4].grid(row=1, column=1)
        widgets[5].grid(row=1, column=2)
        widgets[6].grid(row=1, column=3)
        widgets[7].grid(row=1, column=4, padx=pdx, pady=pdy, columnspan=6)
        if timers_quantity + 1 != timers_to_add: # prevents addign a separator under the bottom timer
            widgets[8].grid(row=2, columnspan = 8, padx=5, pady=3)

        # get the size of the frame to set the apropriate size of the window
        # win_size = re.split(r"[\+\-]", frame.winfo_geometry())[0]

        timers_quantity += 1

    
    def reset_timer(self) -> None:
        print("Reset")
        # widgets[0]
        self.widgets[1].delete()
        # widgets[2]
        self.widgets[3].delete()
        self.widgets[4].delete()
        # widgets[5]
        self.widgets[6].delete()
        # widgets[7]



root = tk.Tk()
# root.resizable(False, False)
root.title('Deadliner pre-alpha')
root.iconbitmap("deadliner.ico")
app = Application()
root.geometry(win_size.join("+500+500"))
app.config(padx=5, pady=5, bg=DGRAY)
app.mainloop()