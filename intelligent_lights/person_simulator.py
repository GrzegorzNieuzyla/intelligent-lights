class PersonSimulator:
    def __init__(self, persons):
        self.persons = persons

    def process(self, grid, cameras):
        for person in self.persons:
            person.move(grid)
            person.update_camera_visibility(grid, cameras)

    def get_persons_positions(self):
        visible = []
        not_visible = []
        for person in self.persons:
            if person.visible:
                visible.append(person.position)
            else:
                not_visible.append(person.position)

        return set(visible), set(not_visible)
