import json

from intelligent_lights.cells.device import Device
from intelligent_lights.cells.empty import Empty
from intelligent_lights.cells.wall import Wall
from intelligent_lights.light import Light


class Parser:
    def __init__(self, file: str):
        with open(file) as f:
            data = json.load(f)
        self.lights = {}
        self.grids = {}
        self.devices = {}
        for floor in data["floors"]:
            label = floor['label']
            self.lights[label] = {Light(light[0], light[1]) for light in floor['lights']}
            self.devices[label] = {(device[0], device[1]) for device in floor['devices']}
            width, height = floor['width'], floor['height']
            grid = []
            for y in range(height):
                grid.append([])
                for x in range(width):
                    grid[-1].append(Wall())

            for space in floor['space']:
                x0, y0, w, h = space
                for x in range(w):
                    for y in range(h):
                        grid[y0 + y][x0 + x] = Device() if (x0 + x, y0 + y) in self.devices[label] else Empty()

            self.grids[label] = grid
