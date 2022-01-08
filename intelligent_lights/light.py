class Light:
    MAX_VALUE = 255

    def __init__(self, x: int, y: int, level: int = 100):
        self.x = x
        self.y = y
        self._light_level = level

    @property
    def light_level(self):
        return self._light_level

    @light_level.setter
    def light_level(self, value):
        self._light_level = max(0, min(value, self.MAX_VALUE))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"({self.x}, {self.y}): {self.light_level}"
