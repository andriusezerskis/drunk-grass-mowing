from typing import TypeVar, Type
from model.entities.entity import Entity

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QFrame, QLabel

from controller.entityInfoController import EntityInfoController
from controller.mainWindowController import MainWindowController
from controller.playerDockController import PlayerDockController
from view.scrollArea import ScrollArea

from parameters import ViewParameters


class Observer:
    def updateClosure(self):
        ...




