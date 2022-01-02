import json

from intelligent_lights.cells.device import Device
from intelligent_lights.cells.empty import Empty
from intelligent_lights.cells.exit import Exit
from intelligent_lights.cells.room import Room
from intelligent_lights.cells.sector import Sector
from intelligent_lights.cells.wall import Wall
from intelligent_lights.cells.window import Window
from intelligent_lights.light import Light


class Parser:
    def __init__(self, file: str):
        with open(file) as f:
            data = json.load(f)
        self.lights = {}
        self.grids = {}
        self.devices = {}
        self.sensors = {}
        self.rooms = {}
        self.sectors = {}
        self.cameras = {}
        self.cell_sizes = {}
        self.exits = {}
        self.windows = {}
        self.sun_power = {}
        self.sun_position = {}
        self.sun_distance = {}
        self.detection_points = {}
        for floor in data["floors"]:
            label = floor['label']
            self.lights[label] = {Light(light[0], light[1]) for light in floor['lights']}
            self.devices[label] = {(device[0], device[1]) for device in floor['devices']}
            self.sensors[label] = {(sensor[0], sensor[1]) for sensor in floor['sensors']}
            self.cameras[label] = {(camera[0], camera[1]) for camera in floor['cameras']}
            self.exits[label] = {Exit(ex) for ex in floor['exits']}
            self.windows[label] = {Window(w) for w in floor['windows']}
            self.sun_power[label] = floor['sun_power']
            self.sun_position[label] = floor['sun_position']
            self.sun_distance[label] = floor['sun_distance']
            self.detection_points[label] = {(dp[0], dp[1]) for dp in floor["detection_points"]}

            width, height = floor['width'], floor['height']
            self.cell_sizes[label] = floor['cell_size']

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

            self.rooms[label] = [Room(room, label) for room, label in zip(floor['rooms'], floor["room_labels"])]
            self.sectors[label] = [Sector(sector) for sector in floor['sectors']]

            self.grids[label] = grid
