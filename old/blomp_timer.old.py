# Author: LordBlompus
# 
# a class 

"""
next it gets messy:
per this: https://stackoverflow.com/a/32289245,
the <Enter> event is an event for the mouse entering the widget
the <Leave> event is an event for the mouse leaving the widget
and: "For mouse wheel support under Linux, use Button-4 (scroll up) and Button-5
 (scroll down)"

make the hours, minutes, seconds entry objects be global (ew)
make a global (ew) variable to hold a reference to the active entry
have enter and leave events for each field.
on enter, set the active entry to the entry entered
on leave, set the active entry to None
"""

import tkinter
import time

# constants to make the event binding more readable
LINUX_SCROLL_UP = "<Button-4>"
LINUX_SCROLL_DOWN = "<Button-5>"

# time bounds constants
HOUR_MAX = 24
MINUTE_MAX = 60
SECOND_MAX = 60

class BlompTimer:
    def __init__(self, hours=0, minutes=0, seconds=0):
        
        # main window
        self.window = tkinter.Tk()
        self.window.bind_all(LINUX_SCROLL_DOWN, self.decreaseActiveEntry)
        self.window.bind_all(LINUX_SCROLL_UP, self.increaseActiveEntry)
        
        # main members
        self.hours = tkinter.IntVar(value=hours)
        self.minutes = tkinter.IntVar(value=minutes)
        self.seconds = tkinter.IntVar(value=seconds)

        self.active_var = None

        self.timer_running = False

        #hours
        #region
        hframe = tkinter.Frame()
        hframe.grid(row=0, column=0)
        hframe.bind("<Enter>", self.enter_h)
        hframe.bind("<Leave>", self.leave_entry)

        hl = tkinter.Label(text="hours", master=hframe)
        hl.grid(row=0,column=0)
        self.hours_entry = tkinter.Entry(
            width=5, 
            master=hframe,
            textvariable=self.hours,
            name="hours"
        )
        self.hours_entry.grid(row=1, column=0)
        #endregion

        #minutes
        #region
        mframe = tkinter.Frame()
        mframe.grid(row=0, column=1)
        mframe.bind("<Enter>", self.enter_m)
        mframe.bind("<Leave>", self.leave_entry)

        ml = tkinter.Label(text="minutes", master=mframe)
        ml.grid(row=0,column=0)
        self.minutes_entry = tkinter.Entry(
            width=5,
            master=mframe,
            textvariable=self.minutes,
            name="minutes"
        )
        self.minutes_entry.grid(row=1, column=0)
        #endregion    

        #seconds
        #region
        sframe = tkinter.Frame()
        sframe.grid(row=0, column=2)
        sframe.bind("<Enter>", self.enter_s)
        sframe.bind("<Leave>", self.leave_entry)
        sframe.bind(LINUX_SCROLL_UP, self.increaseActiveEntry)
        sframe.bind(LINUX_SCROLL_DOWN, self.decreaseActiveEntry)
        sl = tkinter.Label(text="seconds", master=sframe)
        sl.grid(row=0,column=0)
        self.seconds_entry = tkinter.Entry(
            width=5, 
            master=sframe, 
            textvariable=self.seconds,
            name="seconds"
        )
        self.seconds_entry.grid(row=1,column=0)
        #endregion
        
        # buttons
        #region
        self.btnframe = tkinter.Frame()
        self.btnframe.grid(row=2, column=1)

        self.startbtn = tkinter.Button(
            master=self.btnframe,
            text="start",
            # command=self.handle_cancel,
            width=10,
            relief=tkinter.RAISED
        )
        self.startbtn.bind("<Button-1>", self.handle_start)
        self.startbtn.grid(row=0, column=0)

        self.cancelbtn = tkinter.Button(
            master=self.btnframe,
            text="cancel",
            # command=self.handle_cancel,
            width=10,
            relief=tkinter.RAISED
        )
        self.cancelbtn.bind("<Button-1>", self.handle_cancel)
        self.cancelbtn.grid(row=0, column=1)
        
        self.pausebtn = tkinter.Button(
            master=self.btnframe,
            text="pause",
            # command=self.handle_cancel,
            width=10,
            relief=tkinter.RAISED
        )
        self.pausebtn.bind("<Button-1>", self.handle_pause)
        #endregion

    def decreaseActiveEntry(self, event):
        # self.active_entry
        if(self.active_var is None or self.timer_running):
            return
        
        # filter for which entry (hours, minutes, seconds)
        if(self.active_var is self.hours):
           mod = HOUR_MAX
        elif(self.active_var is self.minutes):
           mod = MINUTE_MAX
        elif(self.active_var is self.seconds):
            mod = SECOND_MAX
        
        new_val = (int(self.active_var.get()) - 1) % mod

        self.active_var.set(str(new_val))
        print("decrease", self.active_var) # debug

    # functions to set the active entry for scrolling to change time
    #region
    def enter_h(self, event):
        if( not self.timer_running):
            self.active_var = self.hours
            # print(self.active_var, "is now h:", self.hours) # debug

    def enter_m(self, event):
        if(not self.timer_running):
            self.active_var = self.minutes
            # print(self.active_var, "is now m:", self.minutes) # debug

    def enter_s(self, event):
        if(not self.timer_running):
            self.active_var = self.seconds
            # print(self.active_var, "is now s:", self.seconds) # debug
    
    def leave_entry(self, event):
        """
        sets the active input variable to None when the mouse leaves any entry object
        """
        print(self.active_var, "is no longer active") # debug
        self.active_var = None
    
    #active entry functions
    #endregion

    def handle_cancel(self, event):
        # stop timer
        self.timer_running = False
        # remove pause
        self.pausebtn.grid_remove()
        # show start
        self.startbtn.grid(row=0, column=0)

        # reset the timer values
        self.hours.set(self.hours_cache)
        self.minutes.set(self.minutes_cache)
        self.seconds.set(self.seconds_cache)

        print("cancel") # debug

    def handle_pause(self, event):
        # remove pause
        self.pausebtn.grid_remove()
        # show start
        self.startbtn.grid(row=0, column=0)

        # stop timer loop
        self.timer_running = False
        print("pause") # debug

    def handle_start(self, event):
        # start timer
        self.timer_running = True
        # hide start
        self.startbtn.grid_remove()
        # show pause
        self.pausebtn.grid(row=0, column=0)
        # save the timer values
        self.hours_cache = self.hours.get()
        self.minutes_cache = self.minutes.get()
        self.seconds_cache = self.seconds.get()

        # calculate the timer duration
        time_left = int(self.hours.get())*3600 \
            + int(self.minutes.get())*60 \
            + int(self.seconds.get())
        
        # show time it ends at
        endTime = time.time() + time_left
        print(time.strftime("%I:%M:%S %p", time.localtime(endTime)))

        while(time_left > -1 and self.timer_running):
            mins, secs = divmod(time_left, SECOND_MAX)

            hrs = 0
            if mins > 60:
                hrs, ins = divmod(mins, MINUTE_MAX)
            
            self.hours.set(hrs)
            self.minutes.set(mins)
            self.seconds.set(secs)

            self.window.update()

            if(time_left == 0):
                # play sound UNTIL USER INPUT
                # stop timer
                self.timer_running = False
                # remove pause
                self.pausebtn.grid_remove()
                # show start
                # TODO: why does the startbtn get re-added in with the wrong relief?
                self.startbtn.grid(row=0, column=0) 
                self.startbtn.configure(relief="raised")

                # reset the timer values
                self.hours.set(self.hours_cache)
                self.minutes.set(self.minutes_cache)
                self.seconds.set(self.seconds_cache)
                print("ding")
            #TODO: this sleep allows pausing, 
            # but it's clunky: the sleep finishes before the timer stops
            time.sleep(1)
            time_left -= 1

    
    def increaseActiveEntry(self, event):
        if(self.active_var is None or self.timer_running):
            return
        
        # filter for which entry (hours, minutes, seconds)
        if(self.active_var is self.hours):
           mod = HOUR_MAX
        elif(self.active_var is self.minutes):
           mod = MINUTE_MAX
        elif(self.active_var is self.seconds):
            mod = SECOND_MAX
        
        new_val = (int(self.active_var.get()) + 1) % mod
        self.active_var.set(str(new_val))
        print("increase", self.active_var) # debug

    def run_gui(self):
        self.window.mainloop()
        return (self.hours.get(), self.minutes.get(), self.seconds.get())