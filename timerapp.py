#!/bin/python3

# learning tkinter from https://realpython.com/python-gui-tkinter/
# this is also useful: https://www.geeksforgeeks.org/create-countdown-timer-using-python-tkinter/

# left off reading around: https://realpython.com/python-gui-tkinter/#using-command

import blomp_timer

def load_config():
    return (0,0,0)

def save_config(hours, minutes, seconds):
    pass

def main():
    # load the config if one exists
    (h, m, s) = load_config()

    # TODO: migrate appGUI to its own class so I don't have to mess with globals so messily
    # (h, m, s) = runGUI()
    t = blomp_timer.BlompTimer(h, m, s)
    (h, m, s) = t.run_gui()
    print("oink")

    # save the config
    save_config(h, m, s)

main()