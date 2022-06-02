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
    def __init__(self, p_root_canvas, point_A=None, point_B=None):
        Asset.__init__(self, p_root_canvas)
        self.line = geometry.Line()
        self.point_A_exists = False
        self.point_B_exists = False
        if (point_A != None):
            self.add_start_point(point_A)
        if (point_B != None):
            self.add_end_point(point_B)
    
    def copy(self, p_surface):
        Asset.__init__(self, p_surface.root_canvas)
        self.line = geometry.Line()
        if (p_surface.point_A_exists):
            self.add_start_point(p_surface.line.start_point)
        if (p_surface.point_B_exists):
            self.add_end_point(p_surface.line.end_point)
    
    def draw(self):
        if (self.point_A_exists and self.point_B_exists):
            self.root_canvas.create_line(self.line.start_point.x,self.line.start_point.y,self.line.end_point.x,self.line.end_point.y, fill="#aaaaaa", width=2)

    def add_start_point(self, point_A):
        self.line.set_new_start_point(point_A)
        self.point_A_exists = True

    def add_end_point(self, point_B):
        self.line.set_new_end_point(point_B)
        self.point_B_exists = True

    def draw_with_endpoint(self, point_B):
        if (self.point_A_exists):
            self.root_canvas.create_line(self.line.start_point.x,self.line.start_point.y,point_B.x,point_B.y, fill="#75aebd", width=3)
