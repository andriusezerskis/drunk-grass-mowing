"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""
import time
from copy import copy
from overrides import override
from typing import Dict, Type
from overrides import override
from model.disasters.bloodsplatter import BloodSplatter

from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl


from model.terrains.tiles import MowedGrass1, MowedGrass2, MowedGrass4
from utils import Point, getTerminalSubclassesOfClass

from model.entities.entity import Entity
from model.entities.plants import Tree
from model.entities.animal import Animal
from model.entities.animals import Hamster
from model.terrains.tile import Tile
from model.movable import Movable
from model.crafting.loots import Loot

from utils import getNormalizedVector
from model.player.finance import Finance
import random

class Player(Movable):

    def __init__(self, pos: Point | None, grid: "Grid"):
        super().__init__()
        self.pos = pos
        self.grid = grid
        self.claimed_entity: Entity | None = None
        self.visitedTiles: list[Tile] = []
        self.finance = Finance()
        self.hamstersKilled = 0
        self.drunk = 0

    def isPlaying(self):
        return self.claimed_entity is not None

    def setClaimedEntity(self, tile: Tile):
        self.claimed_entity = tile.getEntity()
        self.pos = tile.getPos()
        tile.removeEntity()
        tile.setEntity(self)

    def removeClaimedEntity(self, killed=False):
        self._reset(killed)

    def isDead(self):
        """The entity chosen never dies

        Returns:
            _type_: _description_
        """
        return False

    def getTile(self):
        return self.grid.getTile(self.pos)

    def move(self, movement: Point):
        currentTile = self.grid.getTile(self.pos)
        # print("current tile type", currentTile.get_current_type())
        for i in self.pos:
            oldPosition = copy(self.pos)
            wantedPosition = self.pos + movement
            if (self.grid.isInGrid(wantedPosition) and self.isValidTileType(type(self.grid.getTile(wantedPosition)))):
                if (self.grid.getTile(wantedPosition).hasEntity() and isinstance(self.grid.getTile(wantedPosition).getEntity(), Hamster)):
                    disasterType = BloodSplatter(1)
                    disasterType.applyDisaster(self.grid.getTile(wantedPosition), 1)
                    self.hamstersKilled += 1
                    self.drunk += 10
                    self.sound = QSoundEffect()
                    self.chainsawSound = QSoundEffect()
                    self.sound.setSource(QUrl.fromLocalFile("sound_effects/hamster_death.wav"))
                    print("sound_effects/chainsaw"+str(random.randint(1, 2))+".wav")
                    self.chainsawSound.setSource(QUrl.fromLocalFile("sound_effects/crowbar"+str(random.randint(1, 2))+".wav"))
                    self.sound.setVolume(0.5)
                    self.chainsawSound.setVolume(0.5)
                    self.sound.play()
                    self.chainsawSound.play()

                if (self.grid.getTile(wantedPosition).hasEntity() and not isinstance(self.grid.getTile(wantedPosition).getEntity(), Tree)) or not self.grid.getTile(wantedPosition).hasEntity():
                    self.grid.getTile(oldPosition).removeEntity()
                    self.grid.getTile(wantedPosition).setEntity(self)
                    self.pos = wantedPosition
                
                    # mark tile as mowedgrass
                    currentTile = self.grid.getTile(wantedPosition)
                    nextTileType = currentTile.mow()
                    print("Current tile type: ", type(currentTile))
                    print("Mowed grass to type: ", nextTileType)

                    newTile = Tile.copyWithDifferentTypeOf(currentTile, nextTileType)
                    currentTile.setEntity(self)
                    newTile.no_times_mowed = currentTile.no_times_mowed
                    print("new tile type: ", type(newTile))
                    self.grid.tiles[wantedPosition.y()][wantedPosition.x()] = newTile

                return True
            return False

    def addInInventory(self, loots: Dict[str, int]):
        for loot_name in loots:
            self.inventory[loot_name] += loots[loot_name]

    def removeFromInventory(self, recipe: Dict[str, int]):
        for loot_name in recipe:
            self.inventory[loot_name] -= recipe[loot_name]

    def getInventory(self):
        return self.inventory

    @override
    def getPos(self) -> Point:
        return self.pos

    def getTexturePath(self) -> str:
        return self.claimed_entity.getTexturePath()

    def isValidTileType(self, tileType: Type[Tile]):
        return self.claimed_entity.isValidTileType(tileType)

    def kill(self):
        pass
        #PlayerDockView.lageEntity(True)

    def _reset(self, killed=False):
        if not killed:
            self.claimed_entity.setPos(self.pos)
            self.grid.getTile(self.pos).setEntity(self.claimed_entity)
        else:
            self.claimed_entity.kill()
        self.pos = None
        self.claimed_entity = None
