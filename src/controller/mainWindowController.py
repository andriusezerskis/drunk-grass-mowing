"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from utils import Point, getPointsAdjacentTo

from model.terrains.tile import Tile


from parameters import ViewParameters

from model.terrains.tiles import Water

from controller.gridController import GridController
from controller.entityInfoController import EntityInfoController
from model.entities.human import Human


class MainWindowController:
    """Singleton"""
    instance = None

    def __new__(cls, graphicalGrid, simulation, mainWindow):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
            cls.graphicalGrid = graphicalGrid
            cls.mainWindow = mainWindow
            cls.simulation = simulation
            cls.entityController = EntityInfoController()
            # cls.gridController = GridController.getInstance()

            tile = cls.getClickedTile(cls, Point(10,10))
            tile.addNewEntity(Human, 1)

            cls.entityController.setEntity(tile.getEntity())
            cls.graphicalGrid.chosenEntity = tile.getEntity()
            GridController.getInstance().controlEntity(tile)
            cls.entityController.update()
            cls.graphicalGrid.updateHighlighted()

            cls.graphicalGrid.redraw(tile)

        return cls.instance

    @staticmethod
    def getInstance():
        if MainWindowController.instance is None:
            raise TypeError
        return MainWindowController.instance

    def getClickedTile(self, point: Point) -> Tile | bool:
        """return false if there is no tile at (x, y) coord"""
        board_point = point // self.graphicalGrid.textureSize
        if self.simulation.getGrid().isInGrid(board_point):
            return self.simulation.getGrid().getTile(board_point)
        return False

    def mousePressEvent(self, event):
        """Handles the mouse press event

        Args:
            event (Event): the mouse press event
        """
        if not self.graphicalGrid.isDefaultTileRenderer():
            return
        scenePos = self.graphicalGrid.mapToScene(event.pos())
        tile = self.getClickedTile(Point(scenePos.x(), scenePos.y()))



        if tile:

            if not self.simulation.hasPlayer():
                self.entityController.setEntity(tile.getEntity())
                self.graphicalGrid.chosenEntity = tile.getEntity()
                GridController.getInstance().controlEntity(tile)

                self.entityController.update()
                self.graphicalGrid.updateHighlighted()

            if not tile.hasEntity() and not self.simulation.hasPlayer():
                self.graphicalGrid.chosenEntity = None
                self.graphicalGrid.updateHighlighted()


    def EntityMonitorPressEvent(self, event):
        ...

    def playerControll(self, tile):
        if tile.hasEntity() and tile.getPos() in getPointsAdjacentTo(self.simulation.getPlayer().getPos()):
            entity = tile.getEntity()
            self.simulation.player.addInInventory(entity.loot())

            tile.removeEntity()
            entity.kill()
            self.graphicalGrid.redraw(tile)

            self.graphicalGrid.updateHighlighted()



    def onEntityControl(self):
        self.mainWindow.zoomInButton.setStyleSheet(ViewParameters.LOCKED_BUTTON)
        self.mainWindow.zoomOutButton.setStyleSheet(ViewParameters.LOCKED_BUTTON)
        self.mainWindow.changeTileRendererButton.setStyleSheet(ViewParameters.LOCKED_BUTTON)

    def onEntityLage(self):
        self.mainWindow.zoomInButton.setStyleSheet(None)
        self.mainWindow.zoomOutButton.setStyleSheet(None)
        self.mainWindow.changeTileRendererButton.setStyleSheet(None)

    def onZoomIn(self):
        if self.simulation.renderMonitor.isMaximumZoomIndex():
            self.mainWindow.zoomInButton.setStyleSheet(ViewParameters.LOCKED_BUTTON)
        else:
            self.mainWindow.zoomOutButton.setStyleSheet(None)

    def onZoomOut(self):
        if self.simulation.renderMonitor.isMinimumZoomIndex():
            self.mainWindow.zoomOutButton.setStyleSheet(ViewParameters.LOCKED_BUTTON)
        else:
            self.mainWindow.zoomInButton.setStyleSheet(None)