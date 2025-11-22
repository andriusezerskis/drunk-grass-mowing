"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from model.generator.noiseGenerator import NoiseGenerator
import matplotlib.pyplot as plt
import numpy as np

from parameters import TerrainParameters

from math import sin, pi

from utils import Point


class RegionHandler:

    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h
        self.gridSize = Point(w, h)
        self.t = 0


    def advanceTime(self):
        self.t += 1
