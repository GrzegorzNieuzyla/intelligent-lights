from intelligent_lights.cells.cell import Cell
from intelligent_lights.cells.cell_type import CellType


class Device(Cell):
    def __init__(self):
        super(Device, self).__init__()
        self.cell_type = CellType.Device
