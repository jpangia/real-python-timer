# a class providing tkinter-based simple gui timer
# but there's a twist: this timer actually repeats the sound 
# at the end of the timer!

import threading
import time
import tkinter

# constants to make the event binding more readable
LINUX_SCROLL_UP = "<Button-4>"
LINUX_SCROLL_DOWN = "<Button-5>"

# time bounds constants
HOUR_MAX = 24
MINUTE_MAX = 60
SECOND_MAX = 60

# grid layout constants
BUTTON_ROW = 1
ENTRY_ROW = 0

class LoudTimer:
    def __init__(self, hours=0, minutes=0, seconds=0):
        
        # main window
        self.window = tkinter.Tk()
        self.window.bind_all(LINUX_SCROLL_DOWN, self.decrease_active_entry)
        self.window.bind_all(LINUX_SCROLL_UP, self.increase_active_entry)
        
        # main members
        self.hours = tkinter.IntVar(value=hours)
        self.minutes = tkinter.IntVar(value=minutes)
        self.seconds = tkinter.IntVar(value=seconds)

        # these *_cache variables are used to save/restore the time values when pausing
        self.hours_cache = hours
        self.minutes_cache = minutes
        self.seconds_cache = seconds

        self.active_var = None

        self.timer_running = False

        #hours gui elements
        #region
        hframe = tkinter.Frame()
        hframe.grid(row=ENTRY_ROW, column=0)
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

        #minutes gui elements
        #region
        mframe = tkinter.Frame()
        mframe.grid(row=ENTRY_ROW, column=1)
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
        sframe.grid(row=ENTRY_ROW, column=2)
        sframe.bind("<Enter>", self.enter_s)
        sframe.bind("<Leave>", self.leave_entry)
        sframe.bind(LINUX_SCROLL_UP, self.increase_active_entry)
        sframe.bind(LINUX_SCROLL_DOWN, self.decrease_active_entry)
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
        
        # label to hold the time the timer ends at
        self.end_time_l = tkinter.Label(master=self.window, text="")
        self.end_time_l.grid(row=ENTRY_ROW+1, column=0)

        # buttons
        #region
        self.btn_frame = tkinter.Frame()
        self.btn_frame.grid(row=2, column=1)

        self.start_btn = tkinter.Button(
            master=self.btn_frame,
            text="start",
            width=10
        )
        self.start_btn.bind("<Button-1>", self.handle_start)
        self.start_btn.grid(row=BUTTON_ROW, column=0)

        self.reset_btn = tkinter.Button(
            master=self.btn_frame,
            text="reset",
            width=10
        )
        self.reset_btn.bind("<Button-1>", self.handle_reset)
        self.reset_btn.grid(row=BUTTON_ROW, column=1)
        
        self.pause_btn = tkinter.Button(
            master=self.btn_frame,
            text="pause",
            width=10
        )
        self.pause_btn.bind("<Button-1>", self.handle_pause)
        #endregion

    def cache_active_value(self):
        """
        saves the value that was updated to be used when
        resetting the timer to its previous value
        """

        if(self.active_var is self.hours):
           self.hours_cache = self.active_var.get()
        elif(self.active_var is self.minutes):
           self.minutes_cache = self.active_var.get()
        elif(self.active_var is self.seconds):
            self.seconds_cache = self.active_var.get()
        

    def decrease_active_entry(self, event):
        """
        event handler function. Decreases the value in the 
        entry object that has been moused over
        """
        
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
        self.cache_active_value()
        print("decrease", self.active_var) # debug

    # functions to set the active entry for scrolling to change time
    #region
    def enter_h(self, event):
        """
        mouseover event handler for the hours entry.
        Sets the active variable to the hours entry.
        """

        if( not self.timer_running):
            self.active_var = self.hours
            # print(self.active_var, "is now h:", self.hours) # debug

    def enter_m(self, event):
        """
        mouseover event handler for the minutes entry.
        Sets the active variable to the minutes entry.
        """

        if(not self.timer_running):
            self.active_var = self.minutes
            # print(self.active_var, "is now m:", self.minutes) # debug

    def enter_s(self, event):
        """
        mouseover event handler for the seconds entry.
        Sets the active variable to the seconds entry
        """

        if(not self.timer_running):
            self.active_var = self.seconds
            # print(self.active_var, "is now s:", self.seconds) # debug
    
    def leave_entry(self, event):
        """
        sets the active input variable to None when the mouse leaves any entry object
        """
        if(not self.timer_running):
            print(self.active_var, "is no longer active") # debug
            self.active_var = None
    
    #active entry functions
    #endregion

    def handle_reset(self, event):
        """
        event handler for the reset button.
        stops timer by resetting the timer_running flag.
        hides the pause button and end time.
        shows the start button
        resets the time values to their cached values
        """
        # stop timer
        self.timer_running = False
        # remove pause
        self.pause_btn.grid_remove()
        # hide time end
        self.end_time_l.config(text="")
        # show start
        self.start_btn.grid(row=BUTTON_ROW, column=0)

        # reset the timer values
        self.hours.set(self.hours_cache)
        self.minutes.set(self.minutes_cache)
        self.seconds.set(self.seconds_cache)

        print("cancel") # debug

    def handle_pause(self, event):
        """
        event handler for the pause button.
        hides the ending time
        replaces the pause button with the start button
        pauses the timer by resetting the timer_running flag
        """
        # remove pause
        self.pause_btn.grid_remove()
        # hide time end
        self.end_time_l.config(text="")
        # show start
        self.start_btn.grid(row=BUTTON_ROW, column=0)

        # stop timer loop
        self.timer_running = False
        print("pause") # debug

    def handle_start(self, event):
        """
        event handler for the start button
        starts the timer by setting the timer_running flag
        replaces the start button with the resume button
        calculates how long the timer should run
        displays the end time
        launches a thread to run the timer and count down the time
        """
        # start timer
        self.timer_running = True
        # hide start
        self.start_btn.grid_remove()
        # show pause
        self.pause_btn.grid(row=BUTTON_ROW, column=0)
        # note: timer values saved in increase/decrease active_entry methods
        
        # calculate the timer duration
        time_left = int(self.hours.get())*3600 \
            + int(self.minutes.get())*60 \
            + int(self.seconds.get())
        
        # show time it ends at
        endTime = time.time() + time_left
        self.end_time_l.config(text=time.strftime("%I:%M:%S %p", time.localtime(endTime)))
        self.end_time_l.grid(row=ENTRY_ROW+1, column=0)
        # print(time.strftime("%I:%M:%S %p", time.localtime(endTime))) # debug

        # create and start the thread that runs the timer
        timer_thread = threading.Thread(target=self.run_timer, args=(time_left,), daemon=True)
        timer_thread.start()

    
    def increase_active_entry(self, event):
        """
        
        """
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
        self.cache_active_value()
        print("increase", self.active_var) # debug

    def run_gui(self):
        """
        executes the main timer loop
        returns the hours, minutes, seconds left on the timer as a triple
        """
        self.window.mainloop()
        return (self.hours.get(), self.minutes.get(), self.seconds.get())
    
    def run_timer(self, time_left):
        while(time_left > -1 and self.timer_running):
            mins, secs = divmod(time_left, SECOND_MAX)

            hrs = 0
            if mins > 60:
                hrs, mins = divmod(mins, MINUTE_MAX)
            
            self.hours.set(hrs)
            self.minutes.set(mins)
            self.seconds.set(secs)

            self.window.update()

            if(time_left == 0):
                # TODO: play sound UNTIL USER INPUT
                # stop timer
                self.timer_running = False
                # remove pause
                self.pause_btn.grid_remove()
                # hide time end
                self.end_time_l.config(text="")
                # show start
                self.start_btn.grid(row=BUTTON_ROW, column=0) 

                # reset the timer values
                self.hours.set(self.hours_cache)
                self.minutes.set(self.minutes_cache)
                self.seconds.set(self.seconds_cache)
                print("ding")
            
            time.sleep(1)
            time_left -= 1