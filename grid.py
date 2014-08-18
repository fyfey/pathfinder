#!/usr/env python

from __future__ import division
import math, pygame, hashlib
from cell import Cell
from pygame.locals import *

class Grid():

        # For clcikAction
        START = 1
        TARGET = 2
        WALL = 3

        def __init__(self, _w, _h, _cw, _ch, surface, game):
            # inital setup
            self.game = game
            self.width = _w
            self.height = _h
            self.cell_width = _cw
            self.cell_height = _ch
            self.cells = []
            self.surface = surface
            self.clickAction = 0
            self.startSet = 0 # Bool - is start set?
            self.targetSet = 0 # Bool - is target set?
            self.target = 0 # Our target cell
            self.start = 0 # Our Start cell

            print "Grid width: %d" % self.width
            print "Grid height: %d" % self.height

            # Create cells
            for i in range(1, (_w*_h)+1):
                self.cells.append(Cell(self.indexToCoord(i), self, self.game))

        def cell(self, _x, _y):
                return self.cells[self.coordToIndex(_x, _y)]

        def coordToIndex(self, _x, _y):
                return ((_y-1)*self.width)+_x - 1
        def updateClickAction(self):
                if not self.startSet:
                        print 'set START'
                        self.clickAction = Grid.START
                        self.startSet = 1
                elif not self.targetSet:
                        print 'set TARGET'
                        self.clickAction = Grid.TARGET
                        self.targetSet = 1
                else:
                        print 'set WALL'
                        self.clickAction = Grid.WALL
        def handleClick(self, event):
                print 'handClick'
                pos = pygame.mouse.get_pos()
                cell = [c for c in self.cells if c.clipRect.collidepoint(pos)]
                cell = cell[0]
                keys = pygame.key.get_pressed()
                if keys[K_LALT]:
                        print 'LEFT ALT'
                        if cell.drawText:
                                cell.drawText = 0
                        else:
                                cell.drawText = 1
                        cell.draw()
                elif keys[K_LCTRL]:
                        print 'CONTROL'
                        if not cell.start and not cell.target and not cell.wall:
                                if cell.highlight:
                                        cell.highlight = 0
                                else:
                                        cell.highlight = 1
                        cell.draw()
                else:
                        self.updateClickAction()
                        if self.clickAction == Grid.START:
                                print 'START'
                                if cell.target:
                                        self.targetSet = 0
                                cell.setStart()
                        elif self.clickAction == Grid.TARGET:
                                print 'TARGET'
                                if cell.start:
                                        self.startSet = 0
                                cell.setTarget()
                        elif self.clickAction == Grid.WALL:
                                print 'WALL'
                                if cell.start:
                                        print 'cell is start'
                                        cell.wall = 0
                                        cell.start = 0
                                        self.startSet = 0
                                        self.start = 0
                                        cell.draw()
                                        return
                                if cell.target:
                                        print 'cell is target'
                                        cell.wall = 0
                                        cell.target = 0
                                        self.targetSet = 0
                                        self.target = 0
                                        cell.draw()
                                        return
                                if not (cell.target and cell.start):
                                        print 'else'
                                        cell.toggleWall()    

        def indexToCoord(self, index):
                a = math.ceil(index/self.width)
                y = int(a)
                x = int(index - ((y-1) * self.width))
                print (x, y)
                return (x, y)

        def draw(self):
            for cell in self.cells:
                cell.draw()

        def getHash(self):
            string = ""
            for cell in self.cells:
                string += self.getAscii(cell)
            return hashlib.md5(string).hexdigest()

