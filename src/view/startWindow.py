"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from model.generator.entitiesGenerator import EntitiesGenerator
from model.generator.gridGenerator import GridGenerator
from model.gridloader import GridLoader
from model.simulation import Simulation
from parameters import ViewParameters
from utils import Point
from view.mainWindow import Window


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(ViewParameters.COW_TEXTURE_PATH))
        self.setGeometry(0, 0, 400, 400)

        self.layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(self.layout)
        container.setObjectName("Transparent")

        self.setObjectName("startWindow")

        self.setCentralWidget(container)
        self.layout2 = QHBoxLayout()
        self.file = None

        # ---- input windows size ----
        self.gridSizeWidth = 40
        self.gridSizeHeight = 40




        container2 = QWidget()
        container2.setLayout(self.layout2)
        container2.setObjectName("Transparent")
        self.layout.addWidget(container2)


        self.button = QToolButton()
        self.button.setText("Démarrer")
        self.button.setFixedSize(200, 50)
        self.button.clicked.connect(self.initMainWindow)
        self.button.setObjectName("startButton")
        self.layout.addWidget(
            self.button, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)

    def loadButtonCallback(self):
        """
        Callback for the load button
        """
        self.qFileDialog = QFileDialog()
        self.qFileDialog.setNameFilter("MAP files (*.map)")
        self.qFileDialog.exec()
        self.file = self.qFileDialog.selectedFiles()
        if self.file and self.file[0].endswith(".map"):
            self.loadButton.setText("Carte chargée")
            # desactivate the button to choose the size of the map
            self.spinBoxWidth.setEnabled(False)
            self.spinBoxHeight.setEnabled(False)

    def updateSpinboxWidth(self, value: int):
        self.gridSizeWidth = value

    def updateSpinboxHeight(self, value: int):
        self.gridSizeHeight = value

    def initMainWindow(self):
        if not self.file or not self.file[0].endswith(".map"):
            self.grid = GridGenerator(Point(self.gridSizeWidth, self.gridSizeHeight), [
                                      2, 3, 4, 5, 6], 350, True).generateGrid()
            EntitiesGenerator().generateEntities(self.grid)
        else:
            self.grid = GridLoader.loadFromFile(self.file[0])

        simulation = Simulation(
            self.grid.gridSize, self.grid)
        window = Window(
            self.grid.gridSize, simulation)
        self.hide()
        window.show()
        window.showMaximized()
