import tkinter as tk
from tkinter import ttk
# from tkinter.constants import *
import tkcalendar as tkc
# from tkcalendar import Calendar, DateEntry
import re
import datetime


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
# timer_selected :int = -1
date_selected = ""

class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg=DGRAY)
        
        self.grid()
        self.createWidgets()
        

    def createWidgets(self):
        
        
        font_1, font_1_size = "Arial\ Nova", " 12 "
        font_2, font_2_size = "Arial", " 9 "
        pdx, pdy = 3, 3
        
        # SET WIDGETS
        # Timer 1
        frame = tk.Frame(self, background=GRAY)
        ent_timer = tk.Entry(frame, bg=GRAY, fg=BLACK, width=20, cursor="xterm", font=(font_1 + font_1_size), relief="solid")
        btn_reset     = tk.Button(frame, 
                                  text='ク', command=self.reset_timer, width=2,
                                  bg=RED, fg=BLACK, cursor="hand2", font=(font_2 + font_1_size + "bold"))
        date_ent = tkc.DateEntry(frame, mindate=datetime.date.today(), 
                                date_pattern="dd.mm.yyyy", font=(font_1 + font_1_size))
        lbl_time_left = tk.Label(frame, text="0000 | 00:00", bg=GRAY, fg=BLACK, font=(font_1 + font_1_size + "bold")) 

        # place the widgets
        frame.grid(row=0, column=0, ipadx=1)
        ent_timer.grid(row=0, column=0, padx=pdx, pady=pdy, columnspan=2)
        btn_reset.grid(row=0, column=2, padx=pdx, pady=pdy)
        date_ent.grid(row=2, column=0, padx=pdx)
        lbl_time_left.grid(row=2, column=1, padx=pdx, pady=pdy, columnspan=2)

        # get the size of the frame to set the apropriate size of the window
        win_size = re.split(r"[\+\-]", frame.winfo_geometry())[0]

    
    def reset_timer(self) -> None:
        print("Reset to do...")
        

 
root = tk.Tk()
root.resizable(False, False)
root.title('Deadliner pre-alpha')
root.iconbitmap("deadliner.ico")
app = Application()
root.geometry(win_size.join("+500+500"))
app.config(padx=5, pady=5, bg=DGRAY)
app.mainloop()