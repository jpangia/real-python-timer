#!/bin/python3

# learning tkinter from https://realpython.com/python-gui-tkinter/
# this is also useful: https://www.geeksforgeeks.org/create-countdown-timer-using-python-tkinter/

# left off reading around: https://realpython.com/python-gui-tkinter/#using-command

import tkinter

"""
next it gets messy:
per this: https://stackoverflow.com/a/32289245,
the <Enter> event is an event for the mouse entering the widget
the <Leave> event is an event for the mouse leaving the widget
and: "For mouse wheel support under Linux, use Button-4 (scroll up) and Button-5 (scroll down)"

make the hours, minutes, seconds entry objects be global (ew)
make a global (ew) variable to hold a reference to the active entry
have enter and leave events for each field.
on enter, set the active entry to the entry entered
on leave, set the active entry to None
"""

# constants to make the event binding more readable
LINUX_SCROLL_UP = "<Button-4>"
LINUX_SCROLL_DOWN = "<Button-5>"

# global variables. I don't know if there is 
# a better way to do this in a GUI app
global global_h
global global_m
global global_s

global global_active_entry

def decreaseActiveEntry(event):
    global global_active_entry
    if(global_active_entry is None):
        return
    print("decrease", global_active_entry)

# functions to set the active entry for scrolling to change time
# TODO: disable this while timer is running
#region
def enterH(event):
    global global_active_entry
    global global_h
    global_active_entry = global_h
    print(global_active_entry, "is now h:", global_h)

def enterM(event):
    global global_active_entry
    global global_m
    global_active_entry = global_m
    print(global_active_entry, "is now m:", global_m)

def enterS(event):
    global global_active_entry
    global global_s
    global_active_entry = global_s
    print(global_active_entry, "is now s:", global_s)
#endregion

def leaveEntry(event):
    """
    sets the active entry to None when the mouse leaves any entry object
    """
    global global_active_entry
    print(global_active_entry, "is no longer active")
    global_active_entry = None

def handleStart():
    # show time it ends at
    # swap start timer for pause timer
    # start timer
    #   timer updates entry values every time it ticks
    # make 
    print("start")

def handleCancel():
    print("cancel")

def increaseActiveEntry(event):
    global global_active_entry
    if(global_active_entry is None):
        return
    print("increase", global_active_entry)

def runGUI():

    window = tkinter.Tk()
    window.bind_all(LINUX_SCROLL_DOWN, decreaseActiveEntry)
    window.bind_all(LINUX_SCROLL_UP, increaseActiveEntry)
    
    #hours
    #region
    hframe = tkinter.Frame()
    hframe.grid(row=0, column=0)
    hframe.bind("<Enter>", enterH)
    hframe.bind("<Leave>", leaveEntry)

    hl = tkinter.Label(text="hours", master=hframe)
    hl.grid(row=0,column=0)
    global global_h
    global_h = tkinter.Entry(width=5, master=hframe)
    global_h.grid(row=1, column=0)
    #endregion

    #minutes
    #region
    mframe = tkinter.Frame()
    mframe.grid(row=0, column=1)
    mframe.bind("<Enter>", enterM)
    mframe.bind("<Leave>", leaveEntry)

    ml = tkinter.Label(text="minutes", master=mframe)
    ml.grid(row=0,column=0)
    global global_m
    global_m = tkinter.Entry(width=5, master=mframe)
    global_m.grid(row=1, column=0)
    #endregion    

    #seconds
    #region
    sframe = tkinter.Frame()
    sframe.grid(row=0, column=2)
    sframe.bind("<Enter>", enterS)
    sframe.bind("<Leave>", leaveEntry)
    sframe.bind(LINUX_SCROLL_UP, increaseActiveEntry)
    sframe.bind(LINUX_SCROLL_DOWN, decreaseActiveEntry)
    sl = tkinter.Label(text="seconds", master=sframe)
    sl.grid(row=0,column=0)
    global global_s
    global_s = tkinter.Entry(width=5, master=sframe)
    global_s.grid(row=1,column=0)
    #endregion
    
    # buttons
    #region
    btnframe = tkinter.Frame()
    btnframe.grid(row=2, column=1)

    startbtn = tkinter.Button(
        master=btnframe,
        text="start",
        command=handleStart,
        width=10,
        relief=tkinter.RAISED
    )
    startbtn.grid(row=0, column=0)

    cancelbtn = tkinter.Button(
        master=btnframe,
        text="cancel",
        command=handleCancel,
        width=10,
        relief=tkinter.RAISED
    )
    cancelbtn.grid(row=0, column=1)
    
    #TODO: pausebtn
    #endregion

    window.mainloop()
    hours = global_h.getint()
    minutes = global_m.getint()
    seconds = global_s.getint()
    return (hours, minutes, seconds)

def main():
    # load the config if one exists
    h = 0
    m = 0
    s = 0
    # (h, m, s) = loadConfig

    # TODO: migrate appGUI to its own class so I don't have to mess with globals so messily
    (h, m, s) = runGUI()
    # t = new BlompTimer(h, m, s)
    # (h, m, s) = t.runGUI()
    print("oink")

    # save the config
    # saveConfig(h, m, s) function

main()