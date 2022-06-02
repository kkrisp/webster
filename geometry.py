import math

MIN_LIM = 0.00001 # since tangents can be really small, a value smaller than this counts as 0

class Angle:
    def __init__(self, deg=0.0, sin=0.0, cos=1.0):
        self.deg = deg
        self.sin = sin
        self.cos = cos
        self.set_degree(deg)

    def set_degree(self, new_deg):
        self.deg = new_deg
        self.sin = math.sin(new_deg)
        self.cos = math.cos(new_deg)

    def set_sine(self, new_sin):
        self.deg = math.asin(new_sin)
        self.sin = new_sin
        self.cos = math.cos(self.deg)

    def set_cosine(self, new_cos):
        self.deg = math.acos(new_cos)
        self.sin = math.sin(self.deg)
        self.cos = new_cos


class Point:
    def __init__(self, x_init=0, y_init=0):
        self.x = x_init
        self.y = y_init


class Line:
    def __init__(self, start_point=None, end_point=None):
        self.start_point = Point()
        self.end_point = Point()
        if start_point is not None:
            self.start_point.x = start_point.x
            self.start_point.y = start_point.y
        if end_point is not None:
            self.end_point.x = end_point.x
            self.end_point.y = end_point.y
        self.projection_length_x, self.projection_length_y = self.calculate_x_y_projection_length()
        self.length = self.calculate_length()
        
        self.sin = 0.0
        self.cos = 1.0
        self.tan = 0.0
        self.ctan = 1000.0
        self.recalculate_all()

    def calculate_x_y_projection_length(self):
        projection_length_x = float(self.end_point.x - self.start_point.x)
        projection_length_y = float(self.end_point.y - self.start_point.y)
        return projection_length_x, projection_length_y

    def calculate_length(self):
        return math.sqrt(math.pow(self.projection_length_x, 2) + pow(self.projection_length_y, 2))

    def set_new_start_point(self, new_start_point):
        self.start_point.x = new_start_point.x
        self.start_point.y = new_start_point.y
        self.recalculate_all()

    def set_new_end_point(self, new_end_point):
        self.end_point.x = new_end_point.x
        self.end_point.y = new_end_point.y
        self.recalculate_all()

    def recalculate_all(self):
        self.projection_length_x, self.projection_length_y = self.calculate_x_y_projection_length()
        self.length = self.calculate_length()

        if MIN_LIM > self.length > -MIN_LIM:
            self.sin = 0.0
            self.cos = 1.0
        else:
            self.sin = self.projection_length_x / self.length
            self.cos = self.projection_length_y / self.length

        if -MIN_LIM < self.projection_length_x < MIN_LIM:
            self.tan = 1000.0
        else:
            self.tan = self.projection_length_y / self.projection_length_x

        if MIN_LIM > self.projection_length_y > -MIN_LIM:
            self.ctan = 1000.0
        else:
            self.ctan = self.projection_length_x / self.projection_length_y

    def y_value_at_given_x(self, x):
        if self.start_point.x <= x <= self.end_point.x or self.start_point.x >= x >= self.end_point.x:
            y = (x-self.start_point.x) * self.tan
            return y + self.start_point.y
        else:
            return None

    def x_value_at_given_y(self, y):
        if self.start_point.y <= y <= self.end_point.y or self.start_point.y >= y >= self.end_point.y:
            x = (y-self.start_point.y) * self.ctan
            return x + self.start_point.x
        else:
            return None
    
    def slice_coordinates(self, slice_length):
        if (abs(slice_length * self.sin) > MIN_LIM):
            slice_x = -slice_length * self.sin
        else:
            slice_x = 0
        
        if (abs(slice_length * self.cos) > MIN_LIM):
            slice_y = slice_length * self.cos
        else:
            slice_y = 0

        return slice_x, slice_y


def is_point_near_a_line(current_point, current_line, threshold):
    #using the larger projection to calculate the position more precisely
    #TODO: selecting larger projection might bz told from the angle
    if abs(current_line.projection_length_x) > abs(current_line.projection_length_y):
        y_calculated = current_line.y_value_at_given_x(current_point.x)
        if y_calculated is None:
            return False
        min_y = y_calculated - threshold
        max_y = y_calculated + threshold
        if min_y <= current_point.y <= max_y or min_y >= current_point.y >= max_y:
            return True
        else:
            return False
    else:
        x_calculated = current_line.x_value_at_given_y(current_point.y)
        if x_calculated is None:
            return False
        min_y = x_calculated - threshold
        max_y = x_calculated + threshold
        if min_y <= current_point.x <= max_y or min_y >= current_point.x >= max_y:
            return True
        else:
            return False