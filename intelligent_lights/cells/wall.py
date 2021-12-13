from intelligent_lights.cells.cell import Cell
from intelligent_lights.cells.cell_type import CellType


class Wall(Cell):
    def __init__(self):
        super(Wall, self).__init__()
        self.cell_type = CellType.Wall
