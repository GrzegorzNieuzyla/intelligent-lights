from intelligent_lights.cells.cell import Cell
from intelligent_lights.cells.cell_type import CellType


class Empty(Cell):
    def __init__(self):
        super(Empty, self).__init__()
        self.cell_type = CellType.Empty

