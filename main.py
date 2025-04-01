# TODO: on start of the program timers appear on by one - it's ugly, I need to fix somehow
# TODO: when data will be loaded from the file, timers, that has a character which is used as delimiter will break the program
#       make validation for a timer title entry to make the character invalid
# TODO: I close file each time. Do I even need it?
# TODO: Understand the variable tracking

import tkinter as tk
from tkinter import ttk
# from tkinter.constants import *
import tkcalendar as tkc
# from tkcalendar import Calendar, DateEntry
import re
import datetime as dt
from datetime import datetime
import sys

#--------------------------------------------------
# VARIABLES AND CONSTANTS
#--------------------------------------------------

#Color palette
BLACK = "#0a0a0a"
WHITE = "#cccccc"
RED   = "#f08080"
DGRAY = "#808080"
GRAY  = "#b4b4b4"
LGRAY = "#e3e3e3"
GREEN = "#94d692"
TESTCLR = "#ff9900" # for debugging

FILE_PATH = "timers.dat"
DFILE_DELIM = '-'

# Style
font_1, font_1_size = "Arial\ Nova", " 12 "
font_2, font_2_size = "Arial", " 9 "
pdx, pdy = 3, 3

win_size: str = "" # Do not reassign directly
# timer_selected :int = -1
date_selected = ""
timers_quantity = 0
timers = []

# Read CLI user arugment
timers_to_add = 1
if len(sys.argv) > 1:
    timers_to_add = int(sys.argv[1])

loaded_data: list = []

#--------------------------------------------------
# FUNCTIONS
#--------------------------------------------------
def handle_events(e):
    if e.keysym == "Escape":  # NOTE:SHOULD BE COMMENTED OUT IN THE RELEASE VERSION!
        print("exiting...")
        sys.exit()

    if e.keysym=="F1": 
        save_data_file()


def load_data_file():
    global loaded_data
    data_file = open(FILE_PATH, "rt")

    # file safe-check
    if (data_file): pass
    else: data_file = open(FILE_PATH, "xt")

    # load the file as 2D array(list)
    for line in data_file:
        loaded_data.append(line.split(DFILE_DELIM))

    data_file.close()

    # Set the loaded data into the fields
    for i, line in enumerate(loaded_data):
        timers[i].widgets["title"].insert(0, line[0])
        timers[i].widgets["date"].set_date(datetime.strptime(f"{line[3]}-{line[2]}-{line[1]}", "%d-%m-%Y"))
        timers[i].widgets["time_hrs"].insert(0, line[4])
        timers[i].widgets["time_min"].insert(0, line[5].strip()) # strip removing \n


def calculate_deadline():
    pass


def save_data_file():
    data_to_save: str = ""

    # Get data from timers
    for n in range(len(timers)):
        timer_data: str = ( timers[n].widgets["title"].get()
            + DFILE_DELIM + str(timers[n].widgets["date"].get_date())
            + DFILE_DELIM + timers[n].widgets["time_hrs"].get()
            + DFILE_DELIM + timers[n].widgets["time_min"].get() )
        data_to_save.join(timer_data + "\n")

    # Save the aquired data to the file
    data_file = open(FILE_PATH, "wt")
    data_file.write(data_to_save)
    data_file.close()


#--------------------------------------------------
# CLASSES
#--------------------------------------------------
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
            if timers_quantity != timers_to_add: # if not the bottom timer
                separator = tk.Frame(self, bg=DGRAY, height=4, width=200)
                separator.grid()

        load_data_file()
 

class Timer(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master, background=GRAY, padx=1, pady=1)

        global timers_quantity        
        global timers


        # TIME(CLOCK) ENTRY INPUT VALIDATION
        def validate_input_hrs(new_text):
            if (not new_text or new_text.isdigit() and len(new_text) <= 2 
                and 0 <= int(new_text) and int(new_text) <= 23):
                return True
            else: 
                on_invalid_hrs()
                return False

        def validate_input_min(new_text):
            if (not new_text or new_text.isdigit() and len(new_text) <= 2 
                and 0 <= int(new_text) and int(new_text) <= 59):
                return True
            else: 
                on_invalid_min()
                return False

        validate_cmd_hrs = root.register(validate_input_hrs) # Register the validation command
        validate_cmd_min = root.register(validate_input_min) # Register the validation command

        def on_invalid_hrs():
            self.widgets["time_hrs"].config(bg=RED)
            root.after(1000, lambda: self.widgets["time_hrs"].config(bg="white"))

        def on_invalid_min():
            self.widgets["time_min"].config(bg=RED)
            root.after(1000, lambda: self.widgets["time_min"].config(bg="white"))


        # CREATE WIDGETS
        self.widgets = {
            # ----------------------------------------------------------------------
            "title":        tk.Entry(self, 
                            bg=LGRAY, fg=BLACK, width=25, cursor="xterm", font=(font_1 + font_1_size), relief="flat"),
            # ----------------------------------------------------------------------
            "btn_reset":    tk.Button(self, 
                            text='ク', command=self.reset_timer, width=2,
                            bg=RED, fg=BLACK, cursor="hand2", font=(font_2 + font_1_size + "bold")) ,
            # ----------------------------------------------------------------------
            "date":         tkc.DateEntry(self, 
                            mindate=dt.date.today(), date_pattern="dd.mm.yyyy", font=(font_1 + font_1_size)) ,
            # ----------------------------------------------------------------------
            "time_hrs":     tk.Entry(self,
                            bg="white", fg=BLACK, width=2, cursor="xterm", font=(font_1 + font_1_size),
                            validate="key",  # Validate on each key press
                            validatecommand=(validate_cmd_hrs, '%P')), # %P = new text
            # ----------------------------------------------------------------------
            "time_colon":   tk.Label(self,
                            text=":", bg=GRAY, fg=BLACK, font=(font_1 + font_1_size)) ,
            # ----------------------------------------------------------------------
            "time_min":     tk.Entry(self,
                            bg="white", fg=BLACK, width=2, cursor="xterm", font=(font_1 + font_1_size),
                            validate="key",  # Validate on each key press
                            validatecommand=(validate_cmd_min, '%P')),  # %P = new text
            # ----------------------------------------------------------------------
            "time_tracker": tk.Label(self, 
                            text="0000 | 00:00", bg=GRAY, fg=BLACK, font=(font_1 + font_1_size + "bold")) ,
            # ----------------------------------------------------------------------
        }


        # PLACING THE WIDGETS
        self.widgets["title"].grid(row=0, column=0, padx=pdx+4, pady=pdy, columnspan=6, sticky='w')
        self.widgets["btn_reset"].grid(row=0, column=7, padx=pdx+6, pady=pdy, columnspan=3)
        self.widgets["date"].grid(row=1, column=0, padx=pdx)
        self.widgets["time_hrs"].grid(row=1, column=1)
        self.widgets["time_colon"].grid(row=1, column=2)
        self.widgets["time_min"].grid(row=1, column=3)
        self.widgets["time_tracker"].grid(row=1, column=4, padx=pdx, pady=pdy, columnspan=6)

        timers_quantity += 1

    
    def reset_timer(self) -> None:
        self.widgets["title"].delete(0, tk.END)
        self.widgets["date"].set_date(dt.date.today())
        self.widgets["time_hrs"].delete(0, tk.END)
        self.widgets["time_min"].delete(0, tk.END)


#--------------------------------------------------
# MAIN PROCESS
#--------------------------------------------------

root = tk.Tk()
root.resizable(False, False)
root.title('Deadliner pre-alpha')
root.iconbitmap("deadliner.ico")
app = Application()
root.geometry(win_size.join("+500+500"))
app.config(padx=5, pady=5, bg=DGRAY)
# TODO: saving data every 1 minute to the file
# key events
root.bind("<KeyRelease>", handle_events)

app.mainloop()
