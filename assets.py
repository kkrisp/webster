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
    def __init__(self, p_root_canvas, p_size=30, p_speed_pixlel_per_tick=10, p_surface=None):
        Asset.__init__(self, p_root_canvas)
        self.surface = p_surface # surface, the player stands on

        self.size = p_size
        self.speed_pixel_per_tick = p_speed_pixlel_per_tick
        
        self.position = geometry.Point(20, 20)

        self.status_move = "stop"
        self.direction = "right"

    def step(self):
        if (self.surface is None):
            self.free_step()
        else:
            self.surface_step()

    def free_step(self):
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
        self.root_canvas.create_circle(math.ceil(self.position.x), math.ceil(self.position.y), self.size)

    def surface_step(self):
        if (self.status_move != "stop"):
            x_step, y_step = self.surface.line.slice_coordinates(self.speed_pixel_per_tick)
            next_position = geometry.Point(self.position.x, self.position.y)

            if (self.direction == "up" and y_step != 0):
                if (self.surface.line.cos < 0):
                    next_position.move(-x_step, +y_step)
                else:
                    next_position.move(+x_step, -y_step)
            elif (self.direction == "down" and y_step != 0):
                if (self.surface.line.cos < 0):
                    next_position.move(+x_step, -y_step)
                else:
                    next_position.move(-x_step, +y_step)
            elif (self.direction == "left" and x_step != 0):
                next_position.move(+x_step, -y_step)
            elif (self.direction == "right" and x_step != 0):
                next_position.move(-x_step, +y_step)

            if (    self.surface.line.x_value_valid(next_position.x)
                and self.surface.line.y_value_valid(next_position.y) ):
                self.position.x = next_position.x
                self.position.y = next_position.y
    
    #TODO: if no surface given, use self.surface
    #TODO: currently moves the player in y (vertical) distance only, maybe do shortest distance
    def put_on_surface(self, p_surface = None):
        """Changes the player position to the closest point on the surface"""
        if (p_surface == None): p_surface = self.surface

        y_calculated = p_surface.line.y_value_at_given_x(self.position.x)
        if (y_calculated != None):
            self.position.y = y_calculated
            self.surface = p_surface
        else:
            print("Player is not over the line {} >> {} << {}".format(p_surface.line.start_point.x, self.position.x, p_surface.line.end_point.x))
    
    def select_and_put_on_surface(self, p_surfaces):
        """Changes the player position to the closest point on the surface"""

        for i in range(p_surfaces.next_asset_id-1):
            surface = p_surfaces.next()
            if (geometry.is_point_near_a_line(self.position, surface.line, 10)):
                self.put_on_surface(surface)
                break


class Surface(Asset):
    def __init__(self, p_id, p_root_canvas, point_A=None, point_B=None):
        Asset.__init__(self, p_root_canvas)
        self.id = p_id

        self.line = geometry.Line()

        self.fill = "#aaaaaa"
        self.line_with = 3

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
    
    def draw(self, p_fill=None, p_width=None):
        if p_fill: fill = p_fill
        else: fill = self.fill

        if p_width: line_with = p_width
        else: line_with = self.line_with

        if (self.point_A_exists and self.point_B_exists):
            self.root_canvas.create_line(
                math.ceil(self.line.start_point.x),
                math.ceil(self.line.start_point.y),
                math.ceil(self.line.end_point.x),
                math.ceil(self.line.end_point.y),
                fill=fill, width=line_with)

    def add_start_point(self, point_A):
        self.line.set_new_start_point(point_A)
        self.point_A_exists = True

    def add_end_point(self, point_B):
        self.line.set_new_end_point(point_B)
        self.point_B_exists = True

    def draw_with_endpoint(self, point_B):
        if (self.point_A_exists):
            self.root_canvas.create_line(
                self.line.start_point.x,
                self.line.start_point.y,
                point_B.x,
                point_B.y,
                fill="#75aebd", width=3)

class Asset_group():
    def __init__(self):
        self.asset_list = []
        self.next_asset_id = 0
        self.selected_asset_id = 0

    def add(self, p_asset):
        self.asset_list.append(p_asset)
        self.next_asset_id += 1

    def next(self, step = 1):
        next_id = self.selected_asset_id + step
        if (next_id >= self.next_asset_id):
            next_id -= self.next_asset_id #not set to next_id=0, in case we want the 2nd or 3rd next

        self.selected_asset_id = next_id
        return self.asset_list[self.selected_asset_id]

    def draw(self):
        for asset in self.asset_list:
            asset.draw()

