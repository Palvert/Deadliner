# TODO: timers appear on by one - need to fix somehow
# TODO: after fixing the problem of timers appearing one by one, make the window appears on the center of the screen
#       (had some struggles with getting the correct windows size, becauses of the first problem)
# TODO: when data will be loaded from the file, timers, that has a character which is used as delimiter will break the program
#       make validation for a timer title entry to make the character invalid

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
# from tkinter.constants import *
import tkcalendar as tkc
# from tkcalendar import Calendar, DateEntry
import re
import datetime as dt
from datetime import datetime
import sys
import os

#--------------------------------------------------
# VARIABLES AND CONSTANTS
#--------------------------------------------------

# Color palette
BLACK   = "#0a0a0a"
WHITE   = "#cccccc"
RED     = "#f08080"
DGRAY   = "#808080"
GRAY    = "#b4b4b4"
LGRAY   = "#e3e3e3"
GREEN   = "#94d692"
TESTCLR = "#ff9900" # for debugging

WIN_TITLE = "Deadliner"
FILE_PATH = "timers.dat"
DFILE_DELIM = '-'
TIME_LEFT_DEFAULT = "--- | -- : --  "
SEC_IN_DAY  = 86400
SEC_IN_HOUR = 3600
SEC_IN_MIN  = 60
COLOR_SECTOR_LOW  = 24 # Less than (Hours)
COLOR_SECTOR_CRIT = 1  # Less than (Hours)
COLOR_SECTOR_OVER = 0  # Less than (Minutes)
CALC_DELAY = 60000 # ms
CHECK_CHANGE_DELAY = 300 # ms

# Style
font_1, font_1_size = "Arial\ Nova", " 12 "
font_2, font_2_size = "Arial", " 9 "
pdx, pdy = 3, 3

date_selected = ""
timers_quantity = 0
timers = []
prev_data = []

# Read CLI user arugment
timers_to_add = 3
if len(sys.argv) > 1 and len(sys.argv) <= 10:
    timers_to_add = int(sys.argv[1])

loaded_data: list = []

#--------------------------------------------------
# FUNCTIONS
#--------------------------------------------------
def load_data_file():
    global loaded_data

    # Read the data file
    if (os.path.exists(FILE_PATH)):
        data_file = open(FILE_PATH, "rt")
    else: return None

    # Load the file as 2D array(list)
    for line in data_file:
        loaded_data.append(line.split(DFILE_DELIM))

    data_file.close()

    # Set the loaded data into the fields
    for i, line in enumerate(loaded_data):
        # prevent loading data for more timers than needed
        if i > (len(timers) - 1): break
        else:
            timers[i].title.set(line[0])
            timers[i].widgets["date"].set_date(datetime.strptime(f"{line[3]}-{line[2]}-{line[1]}", "%d-%m-%Y"))
            timers[i].hrs.set(line[4])
            timers[i].min.set(line[5].strip()) # strip removing \n


def save_data_file():
    data_to_save: str = ""

    # Get data from timers
    for n in range(len(timers)):
        timer_data: str = ( timers[n].widgets["title"].get()
            + DFILE_DELIM + str(timers[n].widgets["date"].get_date())
            + DFILE_DELIM + timers[n].widgets["time_hrs"].get()
            + DFILE_DELIM + timers[n].widgets["time_min"].get() )
        data_to_save += timer_data + "\n"

    # Save the aquired data to the file
    data_file = open(FILE_PATH, "wt")
    data_file.write(data_to_save)
    data_file.close()


def calculate_deadline():
    for n in range(len(timers)):
        if (timers[n].widgets["date"].get_date() and
            timers[n].hrs.get() and
            timers[n].min.get() ):
            d = timers[n].widgets["date"].get_date()
            h = timers[n].hrs.get()
            m = timers[n].min.get()

            parsed_date = datetime.strptime(f"{d}-{h}-{m}", "%Y-%m-%d-%H-%M")
            time_difference = parsed_date - datetime.now()
            date_in_sec = time_difference.total_seconds()

            # Convert from seconds to YMDhm tuple
            days_left    = int(date_in_sec / SEC_IN_DAY)
            date_in_sec -= days_left * SEC_IN_DAY
            hrs_left     = int(date_in_sec / SEC_IN_HOUR)
            date_in_sec -= hrs_left * SEC_IN_HOUR
            min_left     = int(date_in_sec / SEC_IN_MIN)
            date_in_sec -= min_left * SEC_IN_MIN

            time_left_str = str(str(abs(days_left)) +" | "+ 
                                str(abs(hrs_left)).rjust(2, '0') +":"+ 
                                str(abs(min_left)).rjust(2, '0') + "  ")

            # Add minus sign if time is negative
            if (date_in_sec < 0): time_left_str = "- " + time_left_str

            # Set result to the label
            timers[n].time_left.set(time_left_str)

            # Change foreground color accordingly
            # Red Overdue
            if (date_in_sec < 0):
                timers[n].widgets["time_tracker"].config(fg="red")
            else:
                # Yellow Almost
                if (days_left == 0 and hrs_left < COLOR_SECTOR_CRIT):
                    timers[n].widgets["time_tracker"].config(fg="yellow")
                # Blue Hurry up
                elif (days_left == 0 and hrs_left < COLOR_SECTOR_LOW):
                    timers[n].widgets["time_tracker"].config(fg="blue")
                # Black Having time
                else: timers[n].widgets["time_tracker"].config(fg=BLACK)
        else:
            timers[n].time_left.set(TIME_LEFT_DEFAULT)
            timers[n].widgets["time_tracker"].config(fg=DGRAY)

    # Save currient state of the entry fields to compare later when they are changed
    global prev_data
    prev_data = []
    for i in range(len(timers)):
        timer_data = []
        timer_data.append(timers[i].title.get())
        timer_data.append(timers[i].widgets["date"].get_date())
        timer_data.append(timers[i].hrs.get())
        timer_data.append(timers[i].min.get())

        prev_data.append(timer_data)
    # --------------------------------------------------

    root.after(CALC_DELAY, calculate_deadline)


def check_for_changes():
    for i in range(len(timers)):
        curr_data = []
        curr_data.append(timers[i].title.get())
        curr_data.append(timers[i].widgets["date"].get_date())
        curr_data.append(timers[i].hrs.get())
        curr_data.append(timers[i].min.get())

        # An entry field was changed
        if str(prev_data[i]) != str(curr_data):
            calculate_deadline()
            save_data_file()

    root.after(CHECK_CHANGE_DELAY, check_for_changes)


def callback_key_release(event):
    pass
    # if event.keysym == "Escape":  # NOTE:SHOULD BE COMMENTED OUT IN THE RELEASE VERSION!
    #     sys.exit()

    # if event.keysym=="F1": 
    #     save_data_file()
    #
    if event.keysym=="F2":
        calculate_deadline()


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        save_data_file()
        root.destroy()

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

        # Class properties
        self.title = tk.StringVar()
        self.hrs = tk.StringVar()
        self.min = tk.StringVar()
        self.time_left = tk.StringVar()

        self.time_left.set(TIME_LEFT_DEFAULT)

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
                            bg=LGRAY, fg=BLACK, width=30, cursor="xterm", 
                            font=(font_1 + font_1_size), relief="ridge",
                            textvariable=self.title),
            # ----------------------------------------------------------------------
            "btn_reset":    tk.Button(self, 
                            text='ク', command=self.reset_timer, width=2,
                            bg=RED, fg=BLACK, cursor="hand2", 
                            font=(font_2 + font_1_size + "bold")),
            # ----------------------------------------------------------------------
            "date":         tkc.DateEntry(self, 
                            date_pattern="dd.mm.yyyy", font=(font_1 + font_1_size)),
            # ----------------------------------------------------------------------
            "time_hrs":     tk.Entry(self,
                            bg="white", fg=BLACK, width=2, cursor="xterm",
                            font=(font_1 + font_1_size),
                            validate="key",  # Validate on each key press
                            validatecommand=(validate_cmd_hrs, '%P'), # %P = new text
                            textvariable=self.hrs),
            # ----------------------------------------------------------------------
            "time_colon":   tk.Label(self,
                            text=":", bg=GRAY, fg=BLACK, font=(font_1 + font_1_size + "bold"), 
                            anchor="center", width=1),
            # ----------------------------------------------------------------------
            "time_min":     tk.Entry(self,
                            bg="white", fg=BLACK, width=2, cursor="xterm", 
                            font=(font_1 + font_1_size),
                            validate="key",  # Validate on each key press
                            validatecommand=(validate_cmd_min, '%P'),  # %P = new text
                            textvariable=self.min),
            # ----------------------------------------------------------------------
            "time_tracker": tk.Label(self, 
                            text="0000 | 00:00", bg=GRAY, fg=DGRAY, width=12, anchor="ne",
                            font=(font_1 + font_1_size + "bold"), 
                            textvariable=self.time_left, relief="groove") 
            # ----------------------------------------------------------------------
        }


        # PLACING THE WIDGETS
        self.widgets["title"].grid(row=0, column=0, padx=pdx+4, pady=pdy, columnspan=6, sticky='w')
        self.widgets["btn_reset"].grid(row=0, column=7, padx=pdx+6, pady=pdy, columnspan=3, sticky='w')
        self.widgets["date"].grid(row=1, column=0, padx=pdx, sticky='w')
        self.widgets["time_hrs"].grid(row=1, column=1, sticky='w')
        self.widgets["time_colon"].grid(row=1, column=2)
        self.widgets["time_min"].grid(row=1, column=3, sticky='w')
        self.widgets["time_tracker"].grid(row=1, column=4, padx=pdx, pady=pdy, columnspan=6, sticky='e')

        timers_quantity += 1

    
    def reset_timer(self) -> None:
        # self.widgets["title"].delete(0, tk.END)
        # self.widgets["date"].set_date(dt.date.today())
        # self.widgets["time_hrs"].delete(0, tk.END)
        # self.widgets["time_min"].delete(0, tk.END)

        self.title.set("")
        self.widgets["date"].set_date(dt.date.today())
        self.hrs.set("")
        self.min.set("")
        self.time_left.set(TIME_LEFT_DEFAULT)
        self.widgets["time_tracker"].config(fg=DGRAY)


#--------------------------------------------------
# MAIN PROCESS
#--------------------------------------------------

root = tk.Tk()
root.resizable(False, False)
root.title(WIN_TITLE)
root.iconbitmap("deadliner.ico")
app = Application()
app.config(padx=5, pady=5, bg=DGRAY)

# Window closing event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Key press events
root.bind("<KeyRelease>", callback_key_release)

calculate_deadline()
check_for_changes()
root.mainloop()
