from bresenham import bresenham

from intelligent_lights.cells.cell_type import CellType


class CameraSimulator:
    def __init__(self, cameras):
        self.paths = {}
        self.cameras = cameras

    def process(self, grid, persons):
        for person in persons:
            person.move(grid)
            person.visible = self.check_camera_visibility(grid, person)
            person.previousPos = (person.tempPreviousPos if person.visible is True else person.previousPos)
            self.add_position_to_paths(person.id, person.previousPos, person.position)
            person.predicated_path = self.get_predicated_paths(person.id, person.previousPos, person.position)

    def check_camera_visibility(self, grid, person):
        for camera_x, camera_y in self.cameras:
            visible = True
            for check_x, check_y in list(bresenham(person.position[0], person.position[1], camera_x, camera_y)):
                if grid[check_y][check_x].cell_type == CellType.Wall:
                    visible = False
                    break

            if visible:
                return True
        return False

    def add_position_to_paths(self, uuid, prev, current):
        if prev is None or current is None:
            return

        if uuid not in self.paths.keys():
            self.paths[uuid] = [[]]
        if prev != current:
            self.paths[uuid][len(self.paths[uuid])-1].append(current)
        if prev == current and len(self.paths[uuid][len(self.paths[uuid])-1]) > 1:
            self.paths[uuid].append([current])


    def get_predicated_paths(self, uuid, prev, current):
        if prev is None or prev == current:
            return []
    
        found_paths = []
        for path in self.paths[uuid][0:len(self.paths[uuid])-1]:
            i = 0
            id_prev = -1
            for cord in path:
                if id_prev == -1 and cord[0]-3 <= prev[0] <= cord[0]+3 and cord[1]-3 <= prev[1] <= cord[1]+3:
                    id_prev = i
                elif id_prev != -1 and cord[0]-3 <= current[0] <= cord[0]+3 and cord[1]-3 <= current[1] <= cord[1]+3:
                    if path[i + 1:]:
                        found_paths.append(path[i + 1:])
                i += 1

        if len(found_paths) == 0:
            return []
        elif len(found_paths) == 1:
            return found_paths[0]

        count = 0
        for i in range(len(min(found_paths, key=len))):
            for j in range(len(found_paths) - 1):
                if found_paths[j + 1][i][0]-3 <= found_paths[j][i][0] <= found_paths[j + 1][i][0]+3 and found_paths[j + 1][i][1]-3 <= found_paths[j][i][1] <= found_paths[j + 1][i][1]+3:
                    break
                count += 1

        return found_paths[0][:count]