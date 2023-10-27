#!/bin/python3

import loud_timer

def load_config():
    return (0,0,0)

def save_config(hours, minutes, seconds):
    pass

def main():
    # load the config if one exists
    (h, m, s) = load_config()

    # (h, m, s) = runGUI()
    t = loud_timer.LoudTimer(h, m, s)
    (h, m, s) = t.run_gui()
    print("oink")

    # save the config
    save_config(h, m, s)

main()