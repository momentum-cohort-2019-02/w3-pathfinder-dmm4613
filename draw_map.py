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
        self.im.save('elevation_map02.png')

class Pathfinder:
    
    def __init__(self):
        pass


if __name__ == "__main__":
    
    smallMap = Map('elevation_large.txt')
    drawer = Cartographer(smallMap)
    drawer.draw_the_map()
  

