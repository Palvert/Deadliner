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

win_size: str = "" # Do not reassign directly
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
            timers[n].grid()
            # Add an improvised separator
            # frame_x = int(re.split('x', self.winfo_geometry())[0])
            if timers_quantity != timers_to_add: # prevents addign a separator under the bottom timer
                separator = tk.Frame(self, bg=DGRAY, height=4, width=200)
                separator.grid()
 

class Timer(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master, background=GRAY, padx=1, pady=1)

        global timers_quantity        
        global timers
        self.widgets = [
            # Title entry      # 0
            # Reset button     # 1
            # Date entry       # 2
            # Hours entry      # 3
            # : label          # 4
            # Minutes entry    # 5
            # Time left label  # 6
            # Separator(frame) # 7
        ]

            
        self.widgets.append(tk.Entry(self, 
                        bg=LGRAY, fg=BLACK, width=25, cursor="xterm", font=(font_1 + font_1_size), relief="flat"))
        self.widgets.append(tk.Button(self, 
                        text='ク', command=self.reset_timer, width=2,
                        bg=RED, fg=BLACK, cursor="hand2", font=(font_2 + font_1_size + "bold")))
        self.widgets.append(tkc.DateEntry(self, 
                        mindate=datetime.date.today(), date_pattern="dd.mm.yyyy", font=(font_1 + font_1_size)))
        self.widgets.append(tk.Entry(self,
                        bg="white", fg=BLACK, width=2, cursor="xterm", font=(font_1 + font_1_size)))
        self.widgets.append(tk.Label(self,
                        text=":", bg=GRAY, fg=BLACK, font=(font_1 + font_1_size)))
        self.widgets.append(tk.Entry(self,
                        bg="white", fg=BLACK, width=2, cursor="xterm", font=(font_1 + font_1_size)))
        self.widgets.append(tk.Label(self, 
                        text="0000 | 00:00", bg=GRAY, fg=BLACK, font=(font_1 + font_1_size + "bold")))
        # Add an improvised separator
        # frame_x = int(re.split('x', self.winfo_geometry())[0])
        # self.widgets.append(tk.Frame(self, bg=DGRAY, height=3, width=290))
        

        # place the widgets
        self.widgets[0].grid(row=0, column=0, padx=pdx+4, pady=pdy, columnspan=6, sticky='w')
        self.widgets[1].grid(row=0, column=7, padx=pdx+6, pady=pdy, columnspan=3)
        self.widgets[2].grid(row=1, column=0, padx=pdx)
        self.widgets[3].grid(row=1, column=1)
        self.widgets[4].grid(row=1, column=2)
        self.widgets[5].grid(row=1, column=3)
        self.widgets[6].grid(row=1, column=4, padx=pdx, pady=pdy, columnspan=6)
        # if timers_quantity + 1 != timers_to_add: # prevents addign a separator under the bottom timer
        #     self.widgets[7].grid(row=2, columnspan = 8, padx=5, pady=3)

        # get the size of the frame to set the apropriate size of the window
        # win_size = re.split(r"[\+\-]", frame.winfo_geometry())[0]

        timers_quantity += 1

    
    def reset_timer(self) -> None:
        # print("Reset")
        self.widgets[0].delete(0, tk.END)
        # self.widgets[1]
        self.widgets[2].set_date(datetime.date.today())
        self.widgets[3].delete(0, tk.END)
        # self.widgets[4]
        self.widgets[5].delete(0, tk.END)
        # self.widgets[6]
        # self.widgets[7]


def terminate_program(e):
    if e.keysym == "Escape":
        sys.exit()


root = tk.Tk()
# root.resizable(False, False)
root.title('Deadliner pre-alpha')
root.iconbitmap("deadliner.ico")
app = Application()
root.geometry(win_size.join("+500+500"))
app.config(padx=5, pady=5, bg=DGRAY)
# key events
root.bind("<KeyRelease>", terminate_program) # NOTE:SHOULD BE COMMENTED OUT IN THE RELEASE VERSION!

app.mainloop()
