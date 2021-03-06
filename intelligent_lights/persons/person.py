import collections
import uuid
from operator import attrgetter
from random import randint, choice
from bresenham import bresenham

from intelligent_lights.cells.cell_type import CellType
from intelligent_lights.persons.localization import Localization


class Person:
    def __init__(self, grid, rooms):
        self.id = uuid.uuid1().int
        self.previousPos = None
        self.tempPreviousPos = None
        self.position = self.getRoom(rooms)
        self.predicated_path = []
        self.localizations = [
            Localization(self.getRoom(rooms), 40),
            Localization(self.getRoom(rooms), 10),
            Localization(self.getKitchen(rooms), 5),
            Localization(self.getToilet(rooms), 3)
        ]
        self.target = max(self.localizations, key=attrgetter('severity')).position
        self.path = self.generatePath(grid)
        self.visible = False

    def getTarget(self):
        count = 0
        for loc in self.localizations:
            count += loc.severity

        return self.getLoc(randint(0, count - 1))

    def getLoc(self, rnd):
        for loc in self.localizations:
            rnd -= loc.severity
            if (rnd <= 0):
                return loc
        return None

    def getRoom(self, rooms):
        return self.getRandomLocalizationInRoom(rooms, 'Room')

    def getKitchen(self, rooms):
        return self.getRandomLocalizationInRoom(rooms, 'Kitchen')

    def getToilet(self, rooms):
        return self.getRandomLocalizationInRoom(rooms, 'Toilet')

    def getRandomLocalizationInRoom(self, rooms, label):
        room = choice(list(x for x in rooms if x.label.startswith(label)))
        roomRect = room.rects[randint(0, len(room.rects)-1)]

        x = randint(roomRect[0] + 1, roomRect[0] + roomRect[2] - 1)
        y = randint(roomRect[1] + 1, roomRect[1] + roomRect[3] - 1)

        return (x, y)

    def move(self, grid):
        self.tempPreviousPos = self.position
        self.visible = False
        if self.path and len(self.path) > 0:
            self.position = self.path[0]
            self.path = self.path[1:]
        else:
            if self.position == max(self.localizations, key=attrgetter('severity')).position:
                targetLoc = self.getTarget()
            else:
                targetLoc = max(self.localizations, key=attrgetter('severity'))

            self.target = targetLoc.position
            self.path = self.generatePath(grid)
            for i in range(targetLoc.severity):
                self.path.append(self.target)

    def generatePath(self, grid):
        start = self.position
        end = self.target
        queue = collections.deque([[start]])
        seen = {start}
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if x == end[0] and y == end[1]:
                return path
            for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)):
                if 0 <= x2 < 100 and 0 <= y2 < 50 and grid[y2][x2].cell_type != CellType.Wall and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))
