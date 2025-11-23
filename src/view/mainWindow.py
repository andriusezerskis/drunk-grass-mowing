"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

import time
from PyQt6.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QMessageBox, QLabel, QVBoxLayout,QProgressBar
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtGui import QMovie, QFont
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect

from parameters import ViewParameters, ViewText
from utils import Point, getTerminalSubclassesOfClass

from model.entities.entity import Entity
from model.simulation import Simulation
from model.gridexporter import GridExporter
from model.drawable import ParametrizedDrawable
from model.player.player import Player
from parameter.genericparameters import GenericParameters

from view.commandsWindow import CommandWindow
from view.graphicalGrid import GraphicalGrid

from controller.gridController import GridController
from controller.mainWindowController import MainWindowController


class Window(QMainWindow):
    def __init__(self, gridSize: Point, simulation: Simulation):
        super().__init__()
        self.setWindowIcon(QIcon(ViewParameters.COW_TEXTURE_PATH))
        self.setWindowTitle(ViewText.MAIN_WINDOW_TITLE)
        self.renderingMonitor = simulation.getRenderMonitor()
        self.simulation = simulation

        self.view = GraphicalGrid(
            gridSize, simulation.getGrid(), simulation, self.renderingMonitor)
        self.gridController = GridController(
            self.view, simulation, self.renderingMonitor)
        self.mainWindowController = MainWindowController(
            self.view, simulation, self)

        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.addStretch(0)
        self.drawButtons()
        



        self.setCentralWidget(self.view)
        self.totalTime = 0

        self.fastF = False
        self.paused = False

        self.drawButtons2()
        self.oldHamsterKilled =0
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addLayout(self.layout)
        self.animationLabel = QLabel()
        self.animationLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.animationLabel.setPixmap(QPixmap("text_gifs/blood.png"))
        self.animationLabel.setScaledContents(True)
        self.animationLabel.setStyleSheet("background: transparent;")
        self.animationLabel.setHidden(False)

        self.music = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.startSound = QSoundEffect()
        self.startSound.setSource(QUrl.fromLocalFile("sound_effects/chainsaw_start_01.wav"))
        self.startSound.play()
        self.music.setSource(QUrl.fromLocalFile("sound_effects/chainsaw_idle_lp_01.wav"))
        self.music.setLoops(-1)
        self.music.setAudioOutput(self.audioOutput)
        self.audioOutput.setVolume(0.2)
        self.music.play()
       
        self.verticalLayout.addWidget(self.animationLabel, alignment=Qt.AlignmentFlag.AlignCenter)

        self.view.setLayout(self.verticalLayout)

        self.initTimer()

        self.commands = CommandWindow(self)

    def initTimer(self):
        self.timer = QTimer()
        self.timer.setInterval(ViewParameters.STEP_TIME)
        self.timer.timeout.connect(self.recurringTimer)
        self.timer.start()
        self.recurringTimer()

    def pauseTimer(self):
        if self.paused:
            self.paused = False
            self.timer.start()

        else:
            self.timer.stop()
            self.paused = True

    def recurringTimer(self):
        self.totalTime += 1
        self.simulation.step()
        self.updateGrid()
        self.updateMentalHealth(self.simulation.getPlayer().alcoholismLevel)
        self.updateMoney(self.simulation.getPlayer().rewardGained)
        self.activateBlood()
        if self.simulation.getPlayer().alcoholismLevel > 0.6:
            self.timer.setInterval(ViewParameters.STEP_TIME // 2)
        else:
            self.timer.setInterval(ViewParameters.STEP_TIME)

        #self.showTime()

    """
    def showTime(self):
        
        Display the time passed, one step is one hour
        
        nb_days = self.totalTime // 24 + 1
        hour = self.totalTime % 24
        if int(hour) == ViewParameters.NIGHT_MODE_START:
            self.timebutton.setIcon(QIcon(ViewParameters.MOON_ICON))
        elif int(hour) == ViewParameters.NIGHT_MODE_FINISH:
            self.timebutton.setIcon(QIcon(ViewParameters.SUN_ICON))
        if hour < 10:
            self.timebutton.setText(f"Jour {nb_days} - 0{hour}h")
        else:
            self.timebutton.setText(f"Jour {nb_days} - {hour}h")
        #self.view.nightMode(int(hour))
    """
    def fastForward(self):
        if self.fastF:
            self.timer.setInterval(ViewParameters.STEP_TIME)
            self.fastF = False

        else:
            self.timer.setInterval(ViewParameters.STEP_TIME // 2)
            self.fastF = True

    def changeTileRenderer(self):
        if not self.simulation.hasPlayer():
            self.view.changeTileRenderer()
            self.view.chosenEntity = None
            self.view.updateHighlighted()
    """
    def saveGrid(self):
        GridExporter.exportToMap(self.getGraphicalGrid().simulation.getGrid())
    """
    def getGraphicalGrid(self):
        return self.view

    def updateGrid(self):
        """
        Update the grid with the tiles that has been updated by the simulation
        """
        start = time.time()
        self.view.updateGrid(self.simulation.getUpdatedTiles())

    def commandsCallback(self):
        self.commands.show()

    def activateBlood(self):
        if (self.simulation.getPlayer().hamstersKilled > self.oldHamsterKilled):
            self.oldHamsterKilled = self.simulation.getPlayer().hamstersKilled
            self.animationLabel.setHidden(False)
        else:
            self.animationLabel.setHidden(True)


    @staticmethod
    def reloadConfigs():
        GenericParameters.reloadAllDicts()
        ParametrizedDrawable.reloadAllDicts()

    def drawButtons(self):
        
        self.pauseButton = QPushButton("⏸︎")
        self.pauseButton.setCheckable(True)
        self.pauseButton.clicked.connect(self.pauseTimer)
        self.layout.addWidget(self.pauseButton)

        self.upgradeStrengthBtn = QPushButton("Upgrade Strength")
        self.upgradeStrengthBtn.clicked.connect(self.upgradeStrength)
        self.layout.addWidget(self.upgradeStrengthBtn)


        """
        self.fastFbutton = QPushButton("⏩")
        self.fastFbutton.setCheckable(True)
        self.fastFbutton.clicked.connect(self.fastForward)

        self.timebutton = QPushButton("00:00:00")
        self.timebutton.setIcon(QIcon(ViewParameters.MOON_ICON))


        self.changeTileRendererButton = QPushButton("Changer de rendu")
        self.changeTileRendererButton.clicked.connect(self.changeTileRenderer)

        self.saveGridButton = QPushButton("Sauvegarder")
        self.saveGridButton.clicked.connect(self.saveGrid)
        """

        self.currencyLabel = QLabel("0")
        self.currencyLabel.setFont(QFont("Arial",18))
        self.currencyLabel.setFixedWidth(200)
        self.layout.addWidget(self.currencyLabel)

        self.mentalHealthBar = QProgressBar()
        self.mentalHealthBar.setRange(0, 100)
        self.mentalHealthBar.setValue(100)

        self.layout.addWidget(
            self.mentalHealthBar, alignment=Qt.AlignmentFlag.AlignTop  | Qt.AlignmentFlag.AlignRight )

    def upgradeStrength(self):
        if (self.simulation.getPlayer().rewardGained >= 1000):
            self.simulation.getPlayer().strength+=1
            self.simulation.getPlayer().rewardGained -= 1000
            self.upgradeStrengthBtn.setText("UPGRADED")


    def update_health(self, health):
        """Updates the health bar and changes color based on health."""
        self.setValue(health)

    def updateMoney(self, money):
        self.currencyLabel.setText(str(money))
        

    def updateMentalHealth(self,alcoholismLevel):
        mentalhealth = 100 - alcoholismLevel
        self.mentalHealthBar.setValue(int(mentalhealth))

        if mentalhealth > 60:
            self.mentalHealthBar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid black;
                    text-align: center;
                    color: white;
                }
                QProgressBar::chunk {
                    background-color: green;
                }
            """)
        elif mentalhealth > 30:
            self.mentalHealthBar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid black;
                    text-align: center;
                    color: white;
                }
                QProgressBar::chunk {
                    background-color: orange;
                }
            """)
        else:
            self.mentalHealthBar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid black;
                    text-align: center;
                    color: white;
                }
                QProgressBar::chunk {
                    background-color: red;
                }
            """)


    def drawButtons2(self):
        self.zoomInButton = QPushButton("+")
        self.zoomInButton.clicked.connect(self.gridController.zoomIn)
        self.zoomOutButton = QPushButton("-")
        self.zoomOutButton.clicked.connect(self.gridController.zoomOut)
        MainWindowController.getInstance().onZoomIn()
        MainWindowController.getInstance().onZoomOut()

    def closeEvent(self, event):
        self.pauseTimer()
        result = QMessageBox.question(
            self, "Confirmer la fermeture...", "Êtes-vous sûr de retourner au menu?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        event.ignore()

        if result == QMessageBox.StandardButton.Yes:
            event.accept()
            self.close()
        else:
            self.pauseTimer()
            event.ignore()
