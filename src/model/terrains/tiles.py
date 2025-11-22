"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from model.terrains.tile import Tile


class Land(Tile):
    ...


class Mountain(Tile):
    ...


class Sand(Tile):
    ...


class Water(Tile):
    ...

class MowedGrass(Land):
    def __init__(self, pos, height):
        super().__init__(pos, height)
        self.time_to_regrow = 15 # FIXME get from config file instead of hardcoding

    @classmethod
    def get_time_to_regrow(self) -> int:
        return self.time_to_regrow

    def decrease_time_to_regrow(self):
        self.time_to_regrow -= 1
    
