from typing import List


class SunSimulator:
    STEPS_CHANGE = 2
    NOON_POWER = 80
    SUN_POWER_CHANGE = 2
    FULL_CYCLE = 150
    START_SUN_POWER = 20
    START_POSITION = [60, 61, 62]

    def __init__(self, sun_power: int, sun_position: List[int]):
        self.sun_power = sun_power
        self.sun_position = sun_position
        self.change_counter = 0
        self.was_noon = False
        self.step = 0

    def process(self):
        self.step += 1
        if self.step == self.FULL_CYCLE:
            self.step = 0
            self.sun_position = self.START_POSITION
            self.sun_power = self.START_SUN_POWER

        if self.change_counter == self.STEPS_CHANGE:
            self.change_counter = 0

            # change sun state
            if self.was_noon:
                self.sun_power -= self.SUN_POWER_CHANGE
            else:
                self.sun_power += self.SUN_POWER_CHANGE
            self.sun_position = [x+1 for x in self.sun_position]

            if self.sun_power > self.NOON_POWER:
                self.was_noon = True
            if self.sun_power < self.START_SUN_POWER:
                self.was_noon = False
        else:
            self.change_counter += 1
