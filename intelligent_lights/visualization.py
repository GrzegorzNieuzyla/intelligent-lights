from intelligent_lights.cells.cell_type import CellType
from intelligent_lights.visualization_context import VisualizationContext


class Visualization:
    def __init__(self, width: int, height: int):
        self.height = height
        self.width = width

    def redraw(self, context: VisualizationContext):
        for i, line in enumerate(context.grid):
            for j, c in enumerate(line):
                if (j, i) in context.person_positions:
                    print("P", end="")
                elif c.cell_type == CellType.Wall:
                    print("#", end="")
                elif c.cell_type == CellType.Device:
                    print("D", end="")
                elif c.cell_type == CellType.Empty:
                    if c.light_level > 0:
                        print("L", end="")
                    else:
                        print(" ", end="")
            print()
