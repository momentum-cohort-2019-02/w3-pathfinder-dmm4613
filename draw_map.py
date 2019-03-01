import random
import os
from PIL import ImageColor, ImageDraw, Image

class Map:
    """
    This class will take care of all the important values for the map 
    """
    def __init__(self, filename):
        """
        Given a file will set values for the list elevations, and find the max_elevation and min_elevation
        """
        self.elevations = []
        with open(filename) as file:
            for line in file:
                self.elevations.append([int(e) for e in line.strip().split(" ")])

        self.max_elevation = max([max(row) for row in self.elevations])
        self.min_elevation = min([min(row) for row in self.elevations])

    def get_elevation(self, x, y):
        return self.elevations[y][x]
    
    def get_intensity(self, x, y):
        # return (self.get_eleveation(x y) / self.max_elevation) * 255
        return int((self.get_elevation(x, y) - self.min_elevation) / (self.max_elevation - self.min_elevation) * 255)

class Cartographer:
    """
    This class will call the Map class to draw and save the image.
    """
    def __init__(self, map):
        self.map = map
        self.im = Image.new('RGBA', (len(self.map.elevations[0]), len(self.map.elevations)))

    def draw_the_map(self):
        for x in range(len(self.map.elevations[0])):
            for y in range(len(self.map.elevations)):
                self.im.putpixel((x, y), (self.map.get_intensity(x, y), self.map.get_intensity(x, y), self.map.get_intensity(x, y)))        
        self.im.save('elevation_map_find01.png')

class Pathfinder:
    
    def __init__(self, map, filename, x=0, y=0):
        self.map = map
        self.im = Image.open(filename)
        self.current_position = (x,y)
    def get_elevation_difference (self, x):
        """
        by providing the current x coordinate, this method will find the difference in the three movement choices. 
        """
        y = self.current_position[1]
        if y-1 < 0:
            y = 0
        current_elevation = self.map.get_elevation(x, y)
        top_path = self.map.get_elevation((x+1),(y-1))
        middle_path = self.map.get_elevation((x+1),y)
        if y+1 > len(self.map.elevations):
            y = len(self.map.elevations)-1
        bottom_path = self.map.get_elevation((x+1),(y+1))

        self.top_diff = abs(current_elevation - top_path)
        self.middle_diff = abs(current_elevation - middle_path)
        self.bottom_diff = abs(current_elevation - bottom_path)
        self.choices = [self.top_diff, self.middle_diff, self.bottom_diff]
        self.min_diff = min(self.choices)

        # ###should probably split this part below into another method###
      
        if self.top_diff == self.min_diff and self.top_diff == self.bottom_diff and self.top_diff != self.middle_diff:
            if random.randint(0,1) == 0:
                y -= 1
            else:
                y += 1
        elif self.top_diff == self.min_diff and self.top_diff != self.middle_diff:
            y -= 1
        elif self.bottom_diff == self.min_diff and self.bottom_diff != self.middle_diff:
            y += 1
        x =+ 1
        self.current_position = (x,y)

        return y
        
    def mark_my_trail(self):
        """
        The hiker will place a marker (pixel) on the current location by putpixel() on the drawn map.
        """
        y = self.current_position[1]
        for x in range(len(self.map.elevations[0])-1):
            self.im.putpixel((x,y), (0, 255, 0))
            y = self.get_elevation_difference(x)
        self.im.save('elevation_map_find01.png')

if __name__ == "__main__":
   
    smallMap = Map('elevation_small.txt')
    drawer = Cartographer(smallMap)
    drawer.draw_the_map()
    hiker = Pathfinder(smallMap, 'elevation_map_find01.png', y=280)
    hiker.mark_my_trail()
