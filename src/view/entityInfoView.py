"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget,  QVBoxLayout, QLabel, QProgressBar, QPushButton
from controller.gridController import GridController
from model.entities.entity import Entity
from model.entities.animal import Animal

from parameters import ViewText, EntityParameters, ViewParameters


class EntityInfoView:
    def __init__(self):
        self.infoLabel = QLabel()
        self.entity = None

    def controlEntity(self):
        GridController.getInstance().controlEntity(self.entity.getTile())

    def setEntity(self, entity: Entity):
        self.entity = entity

    def __updateText(self, entity: Entity):
        """Shows information about an entity"""
        self.entity = entity

        if entity.isDead():
            self.showDeadEntity()

    def updateOnStep(self):
        """Update the view at each time step of the simulation"""
        if self.entity is not None:
            self.__updateText(self.entity)


    def deselectEntity(self):
        self._hideSelectedEntityPart(ViewText.ENTITY_NOT_SELECTED)

    def showDeadEntity(self):
        """When the entity dies, the progress bar shows that the entity is dead"""
        self._hideSelectedEntityPart(ViewText.ENTITY_DEAD_MESSAGE)

    def _hideSelectedEntityPart(self, text):
        """Hides all the information about the entity"""
        self.entity = None