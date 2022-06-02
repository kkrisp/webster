import sys
import math
import tkinter as tk

class Ticker():
    def __init__(self, p_root_world, p_tick_timed_action, p_tick_duration_ms=100, p_time_limit_sec=30):
        self.root = p_root_world
        self.tick_timed_action = p_tick_timed_action

        self.tick_duration_ms = p_tick_duration_ms
        self.time_limit_sec = p_time_limit_sec
        self.time_limit_ticks = math.ceil(self.time_limit_sec*1000/self.tick_duration_ms)
        self.tick_counter = 0

    def tick(self, tick_counter_increase=1):
        self.tick_timed_action(self.tick_counter)
        self.tick_counter += tick_counter_increase
        if self.tick_counter < self.time_limit_ticks:
            self.root.after(self.tick_duration_ms, self.tick) # call countdown again
        else:
            print("Time is over after", self.time_limit_sec, "seconds.")

class World(tk.Frame):
    #def __init__(self, *args, position_manager, **kwargs):
    def __init__(self, p_root, p_width=500, p_height=100, p_tick_length_ms = 1000, p_time_limit_sec = 10):
        tk.Frame.__init__(self, p_root, width=p_width, height=p_height)
        self.ticker = Ticker(p_root, self.Timed_action, p_tick_length_ms, p_time_limit_sec)
        self.bind("<KeyPress>", lambda e: self.Keydown_action(e))
        self.bind("<KeyRelease>", lambda e: self.Keyup_action(e))
    
    def Init(self):
        self.pack()
        self.focus_set()
        self.ticker.tick()

    def Timed_action(self, counter):
        print("Tick", counter)
    
    def Keydown_action(self, e):
        print("{} ({}) pressed".format(e.char, ord(e.char))) 
    
    def Keyup_action(self, e):
        print("{} ({}) released".format(e.char, ord(e.char))) 

