#!/usr/env python

import math
import pygame

BLACK     = (0, 0, 0)
RED       = (255, 0, 0)
GREEN     = (0, 255, 0)
CELL      = (125, 125,125)
HIGHLIGHT = (116, 129, 168)
CURRENT   = (224, 185, 27)
PATH      = (230, 230, 100)

class Cell():

        def __init__(self, coords, grid, game):
                self.x, self.y = coords
                self.grid = grid
                self.game = game

                self.width = grid.cell_width
                self.height = grid.cell_height
                self.X, self.Y = self.getCoords()
                self.clipRect = 0
                self.drawRect = 0
                self.wall = 0
                self.start = 0
                self.target = 0
                self.highlight = 0
                self.current = 0
                self.path = 0

                self.bgcolor = CELL
                self.neighbours = []
                self.drawText = 0
                self.h, self.g, self.f = (0, 0, 0)
                self.parent = 0
                self.updateText()

        def updateText(self):
                self.hText = self.game.cellfont.render(str(self.h), 1, BLACK)
                self.gText = self.game.cellfont.render(str(self.g), 1, BLACK)
                self.fText = self.game.cellfont.render(str(self.f), 1, BLACK)

        def getCoords(self):
                x = int((self.x - 1) * self.width )
                y = int(math.fabs(((self.y * self.height) - self.height) - ((self.height * self.grid.height)-self.height)))
                return (x, y)

        def getNeighbours(self):
                # Up
                if self.y < self.grid.height and (not self.grid.cell(self.x, self.y+1).wall):
                        self.neighbours.append(self.grid.cell(self.x, self.y+1))
                # Right
                if self.x < self.grid.width and (not self.grid.cell(self.x+1, self.y).wall):
                        self.neighbours.append(self.grid.cell(self.x+1, self.y))
                # Down
                if self.y > 1 and (not self.grid.cell(self.x, self.y-1).wall):
                        self.neighbours.append(self.grid.cell(self.x, self.y-1))
                # Left
                if self.x > 1 and (not self.grid.cell(self.x-1, self.y).wall):
                        self.neighbours.append(self.grid.cell(self.x-1, self.y))


        def calcH(self):
                if self.grid.targetSet:
                        xDiff = self.x - self.grid.target.x
                        yDiff = self.y - self.grid.target.y
                        return int(math.fabs(xDiff) + math.fabs(yDiff))

        def calcF(self):
                return self.g + self.h

        def setStart(self):
                self.start = 1
                self.target = 0
                self.wall = 0
                self.grid.start = self
                self.draw()
        def setTarget(self):
                self.target = 1
                self.wall = 0
                self.start = 0
                self.grid.target = self
                self.draw()
        def toggleWall(self):
                if self.wall:
                        self.wall = 0
                        self.start = 0
                        self.target = 0
                else:
                        self.wall = 1
                        self.start = 0
                        self.target = 0
                self.draw()
                print 'toggleWall [%d, %d]' % (self.x, self.y)

        def draw(self):
                if self.wall:
                        bgcolor = BLACK
                elif self.start:
                        bgcolor = GREEN
                elif self.target:
                        bgcolor = RED
                elif self.current:
                        bgcolor = CURRENT
                elif self.highlight:
                        bgcolor = HIGHLIGHT
                elif self.path:
                        bgcolor = PATH
                else:
                        bgcolor = CELL
                x, y = self.getCoords()
                print self.getCoords()
                self.clipRect = pygame.Rect(x, y, self.width, self.height)
                self.drawRect = pygame.Rect(x + 1, y + 1, self.width - 2, self.height - 2)
                pygame.draw.rect(self.grid.surface, bgcolor, self.drawRect, 0)
                if self.drawText:
                        self.updateText()
                        self.grid.surface.blit(self.hText, (x + 3, y))
                        self.grid.surface.blit(self.gText, (x + 3, y + self.height - 14))
                        self.grid.surface.blit(self.fText, (x + 41, y + 36))
