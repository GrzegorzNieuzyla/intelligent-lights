class PersonSimulator:
    def __init__(self, persons):
        self.persons = persons

    def process(self, grid):
        for person in self.persons:
            person.move(grid)

    def get_persons_localizations(self):
        localizations = []
        for person in self.persons:
            localizations.append(person.position)
        return set(localizations)
