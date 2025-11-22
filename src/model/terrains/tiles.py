"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from model.terrains.tile import Tile


class Land(Tile):
    def __init__(self, pos, height):
        super().__init__(pos, height)
        self.time_to_regrow = self.get_initial_time_to_regrow()
        self.variations = [Land, MowedGrass1, MowedGrass2, MowedGrass3, MowedGrass4]
        self.no_times_mowed = 0

    @classmethod
    def get_initial_time_to_regrow(cls) -> int:
        return cls._getParameter("time_to_regrow")
    
    @classmethod
    def getReward(cls) -> int:
        return cls._getParameter("reward")

    def get_time_to_regrow(self) -> int:
        return self.time_to_regrow

    def decrease_time_to_regrow(self):
        self.time_to_regrow = max(0, self.time_to_regrow - 1)
    
    def mow(self):
        self.no_times_mowed = min(self.no_times_mowed + 1, len(self.variations) - 1)
        return self._get_next_type()

    def regrow(self):
        self.no_times_mowed = max(0, self.no_times_mowed - 1)
        return self._get_previous_type()

    def _get_next_type(self):
        return self.variations[(self.no_times_mowed) % len(self.variations)]
    
    def _get_previous_type(self):
        return self.variations[(self.no_times_mowed) % len(self.variations)]
    



class Mountain(Tile):
    ...


class Sand(Tile):
    ...


class Water(Tile):
    ...
    
class MowedGrass1(Land):
    ...

class MowedGrass2(Land):
    ...

class MowedGrass3(Land):
    ...
    
class MowedGrass4(Land):
    ...