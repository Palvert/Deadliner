# Deadliner  
![deadliner_gti_cover.png](./res/git_cover.png)  
#### Deadliner is a simple program for tracking your deadlines.  
#### Made with Tkinter in Python.

## Tips:  
Quantinty of time trackers can be changed by passing an argument. 3 by default. Up to 10.  
`start ./Deadliner.exe 3`  
Argument can be conviniently specified in the properties of a .lnk file.  

## Compile command:  
`pyinstaller --clean --onefile --hidden-import=babel.numbers --windowed --icon res/Deadliner.ico src/Deadliner.py`   
