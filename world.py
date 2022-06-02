import sys
import math
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

        self.objects = []
        
        self.canvas=tk.Canvas(self, width=p_width, height=p_height)
        self.canvas.pack()
        
        self.ground = assets.Surface(self.canvas, geometry.Point(100, 300), geometry.Point(650, 300))
        self.ground.color = "#476a3f"
        self.ground.width = 4

        self.player = assets.Player(self.canvas, p_size = 10, p_surface = self.ground)
        #self.player = assets.Player(self.canvas, p_size = 10)
        
        self.player.position = geometry.Point(10, 300)
        #self.player.position = geometry.Point(20, 20)

        self.line_in_progress = None

    def init(self):
        self.pack()
        self.focus_set()
        self.ticker.tick()

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
        elif (e.char == 'h'): # right
            self.create_line()
        else:
            print("{} ({}) not programmed".format(e.char, ord(e.char)))
    
    def keyup_action(self, e):
        #print("{} ({}) released".format(e.char, ord(e.char)))
        self.player.status_move = "stop"
    
    def refresh(self):
        self.clear()
        self.ground.draw()
        self.player.draw()

        if (self.line_in_progress): self.line_in_progress.draw_with_endpoint(self.player.position)
        for single_asset in self.objects:
            single_asset.draw()

    def clear(self):
        self.canvas.delete("all")

    def create_line(self):
        if (self.line_in_progress is None):
            self.line_in_progress = assets.Surface(self.canvas)
            self.line_in_progress.add_start_point(geometry.Point(self.player.position.x, self.player.position.y))
        else:
            self.line_in_progress.add_end_point(geometry.Point(self.player.position.x, self.player.position.y))
            self.objects.append(self.line_in_progress)
            self.line_in_progress = None

