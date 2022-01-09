class PersonSimulator:
    def __init__(self, persons):
        self.persons = persons

    def process(self, grid):
        for person in self.persons:
            person.move(grid)

    def get_persons_positions(self):
        visible = []
        not_visible = []
        predictions = []
        for person in self.persons:
            if person.visible:
                visible.append(person.position)
                prediction = person.predicated_path
                if len(prediction) >= 5:
                    predictions.append(prediction[4])

                if len(prediction) >= 10:
                    predictions.append(prediction[9])

                if len(prediction) >= 15:
                    predictions.append(prediction[14])
            else:
                not_visible.append(person.position)

        return set(visible), set(not_visible), set(predictions)
