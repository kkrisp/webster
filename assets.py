import sys
import math
import random
import geometry
import tkinter as tk


SPRITE_ID_LIST = [
            "idle_right_0",
            "idle_right_1",
            "move_right_0",
            "move_right_1",
            "move_right_2",
            "move_right_3",
            "idle_left_0",
            "idle_left_1",
            "move_left_0",
            "move_left_1",
            "move_left_2",
            "move_left_3"
            ]

SPRITE_ID_DICTIONARY = {
            "idle_right_0" : "sprites/placeholder_idle_right_0.png",
            "idle_right_1" : "sprites/placeholder_idle_right_1.png",
            "move_right_0" : "sprites/placeholder_right_0.png",
            "move_right_1" : "sprites/placeholder_right_1.png",
            "move_right_2" : "sprites/placeholder_right_2.png",
            "move_right_3" : "sprites/placeholder_right_3.png",
             "idle_left_0" : "sprites/placeholder_idle_left_0.png",
             "idle_left_1" : "sprites/placeholder_idle_left_1.png",
             "move_left_0" : "sprites/placeholder_left_0.png",
             "move_left_1" : "sprites/placeholder_left_1.png",
             "move_left_2" : "sprites/placeholder_left_2.png",
             "move_left_3" : "sprites/placeholder_left_3.png"
}

def _create_circle(self, x, y, r, **kwargs):
    """Simplifies the oval creating method, when the wanted object is a circle. 
    Snippet from stackoverflow:
    https://stackoverflow.com/questions/17985216/draw-circle-in-tkinter-python"""
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

class Asset():
    def __init__(self, p_root_canvas):
        self.root_canvas = p_root_canvas
    
    def draw(self):
        print("The Asset parent class can not be drawn. Redefine the 'draw' method in the child classes")


class Player(Asset):
    def __init__(self, p_root_canvas, p_size=30, p_speed_pixlel_per_tick=10):
        Asset.__init__(self, p_root_canvas)
        
        self.size = p_size
        self.speed_pixel_per_tick = p_speed_pixlel_per_tick
        
        self.position = geometry.Point(20, 20)

        self.status_move = "stop"
        self.direction = "right"

    def step(self):
        if (self.status_move != "stop"):
            if (self.direction == "up"):
                self.position.y -= self.speed_pixel_per_tick
            elif (self.direction == "down"):
                self.position.y += self.speed_pixel_per_tick
            elif (self.direction == "left"):
                self.position.x -= self.speed_pixel_per_tick
            elif (self.direction == "right"):
                self.position.x += self.speed_pixel_per_tick

    def draw(self):
        #return super().draw()
        self.root_canvas.create_circle(self.position.x, self.position.y, self.size)


class Surface(Asset):
    def __init__(self, p_root_canvas, point_A, point_B):
        Asset.__init__(self, p_root_canvas)
        self.line = geometry.Line()
        self.line.set_new_start_point(point_A)
        self.line.set_new_end_point(point_B)
    
    def draw(self):
        self.root_canvas.create_line(self.line.start_point.x,self.line.start_point.y,self.line.end_point.x,self.line.end_point.y, fill="#aaaaaa", width=3)
