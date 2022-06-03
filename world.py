import sys
import math
from turtle import bgcolor

import assets
import tkinter as tk
import geometry

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
        self.ticker = Ticker(p_root, self.timed_action, p_tick_length_ms, p_time_limit_sec)
        self.bind("<KeyPress>", lambda e: self.keydown_action(e))
        self.bind("<KeyRelease>", lambda e: self.keyup_action(e))

        self.climbable_objects = assets.Asset_group()
        self.next_object_id = 0
        
        self.canvas=tk.Canvas(self, width=p_width, height=p_height, bg="#c8dae7")
        self.canvas.pack()
        
        self.ground = assets.Surface(self.next_object_id, self.canvas, geometry.Point(10, 200), geometry.Point(650, 200))
        self.next_object_id += 1
        self.ground.fill = "#476a3f"
        self.ground.line_width = 4

        
        self.wall = assets.Surface(self.next_object_id, self.canvas, geometry.Point(200, 10), geometry.Point(300, 300))
        self.next_object_id += 1
        self.wall.fill = "#476a3f"
        self.wall.line_width = 4
        
        self.climbable_objects.add(self.wall)
        self.climbable_objects.add(self.ground)

        self.player = assets.Player(self.canvas, p_size = 10, p_surface = self.ground)

        self.line_in_progress = None

    def init(self):
        self.pack()
        self.focus_set()
        self.ticker.tick()
        
        self.player.put_on_surface(self.player.surface)

    def timed_action(self, counter):
        #print("Tick", counter)
        self.player.step()
        self.refresh()
    
    def keydown_action(self, e):
        #print("{} ({}) pressed".format(e.char, ord(e.char)))
        #print ("down", e.char, self.line_x1)
        if (e.char == 'w'):  # up
            self.player.status_move = "move"
            self.player.direction = "up"
        elif (e.char == 's'): # down
            self.player.status_move = "move"
            self.player.direction = "down"
        elif (e.char == 'a'): # left
            self.player.status_move = "move"
            self.player.direction = "left"
        elif (e.char == 'd'): # right
            self.player.status_move = "move"
            self.player.direction = "right"
        elif (e.char == 'k'): # right
            self.create_line()
        elif (e.char == 'l'): # right
            self.player.select_and_put_on_surface(self.climbable_objects)
        else:
            print("{} ({}) not programmed".format(e.char, ord(e.char)))
    
    def keyup_action(self, e):
        #print("{} ({}) released".format(e.char, ord(e.char)))
        self.player.status_move = "stop"
    
    def refresh(self):
        self.clear()
        self.player.surface.draw("#ffffff", 9)
        # keep drawing order in mind, objects drawn later go on the top 
        self.player.draw()
        self.climbable_objects.draw()
        
        
        if (self.line_in_progress): self.line_in_progress.draw_with_endpoint(self.player.position)

    def clear(self):
        self.canvas.delete("all")

    def create_line(self):
        if (self.line_in_progress is None):
            self.line_in_progress = assets.Surface(self.next_object_id, self.canvas)
            self.next_object_id += 1
            self.line_in_progress.add_start_point(geometry.Point(self.player.position.x, self.player.position.y))
        else:
            self.line_in_progress.add_end_point(geometry.Point(self.player.position.x, self.player.position.y))
            self.climbable_objects.add(self.line_in_progress)
            self.line_in_progress = None