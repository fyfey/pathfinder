from __future__ import division
import pygame, random, sys, math, decimal
from config import Config
from grid import Grid
from file import File
from pygame.locals import *
pygame.init()

DKGREY = (50,50,50)

class Game():

    def __init__(self):
        self.config = Config()
        self.config.load('config.yaml')
        self.cellfont = pygame.font.SysFont('arial',10)
        self.file = File()
        self.fpsClock = pygame.time.Clock()
        self.load()

    def setupCell(self, cell, char):
        if char == "S":
            cell.setStart()
            self.grid.startSet = 1
        elif char == "F":
            cell.setTarget()
            self.grid.targetSet = 1
        elif char == "#":
            cell.wall = 1

    def reset(self):
        keys = pygame.key.get_pressed()
        self.solving = 0
        self.openList = []
        self.closedList = []
        if keys[K_LSHIFT]:
            self.grid = Grid(
                self.grid.width,
                self.grid.height,
                self.grid.cell_width,
                self.grid.cell_height,
                self.surface,
                self
            )
        else:
            for cell in self.grid.cells:
                cell.path = 0
                cell.highlight = 0
                cell.current = 0
                cell.f, cell.g, cell.h = (0, 0, 0)
                cell.neighbours = []
                cell.drawText = 0
        self.grid.draw()

    def start(self):
            print('starting game loop')
            while True:
                for event in pygame.event.get(QUIT): # get all the QUIT events
                    print('quit')
                    pygame.quit()
                    sys.exit()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.grid.handleClick(event)
                    if event.type == pygame.KEYUP:
                        if event.key == K_SPACE:
                            if not self.solving:
                                self.solve()
                        if event.key == K_ESCAPE:
                            self.reset()
                        if event.key == K_s:
                            self.save()
                        if event.key == K_l:
                            self.surface = None
                            self.load()

                pygame.display.update()
                self.fpsClock.tick(self.fps)

    def solve(self):
            if self.grid.startSet and self.grid.targetSet:
                print('Solving')
                self.reset()
                # Reset lists
                self.openList = []
                self.closedList = []
                current = False
                # Add our start to the closed list and begin
                self.openList.append(self.grid.start)

                while len(self.openList)>0:
                    current = self.nextStep()
                    current.current = 1
                    current.draw()
                    if current == self.grid.target:
                        print('found path!')
                        solving = 0
                        cell = self.grid.target
                        current.current = 0
                        current.draw()
                        path = []
                        while cell.parent:
                            path.append(cell)
                            cell = cell.parent
                        path = reversed(path)
                        for cell in path:
                            cell.path=1
                            cell.highlight=0
                            cell.draw()
                            pygame.time.delay(self.config.found_delay)
                            pygame.display.update()
                        break

                    self.closedList.append(current)

                    found = 0
                    for cell in current.neighbours:
                        if cell in self.closedList:
                            print('closed')
                            continue
                        if cell not in self.openList or current.g + 1 <= cell.parent.g + 2:
                            cell.highlight = 1
                            cell.drawText = 1
                            cell.parent = current
                            cell.g = cell.parent.g + 1
                            cell.h = cell.calcH()
                            cell.f = cell.calcF()
                            self.openList.append(cell)
                            cell.draw()
                            found = 1
                    if found:
                        pygame.time.delay(self.config.search_delay)
                    print(len(self.openList))
                    pygame.display.update()
                    current.current = 0
                    current.draw()
                else:
                    print('Failure')
                self.solving = 0
            else:
                print('Error: I need a start and finish!')

    def save(self):
        self.file.save()

    def load(self):
        self.fps = self.config.fps
        grid = self.file.load()

        if grid:
            self.config.grid_width, self.config.grid_height = (len(grid[0]), len(grid))

        self.SCREENWIDTH, self.SCREENHEIGHT = (self.config.grid_width * self.config.cell_width, self.config.grid_height * self.config.cell_height)
        self.surface = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT))
        pygame.display.set_caption('Pathfinder')
        self.grid = Grid(self.config.grid_width, self.config.grid_height, self.config.cell_width, self.config.cell_height, self.surface, self)
        self.file.setGrid(self.grid)
        self.surface.fill(DKGREY)

        if grid:
            for i in range(0, len(grid)):
                for j in range(0, len(grid[i])):
                    self.setupCell(self.grid.cell(j+1, i+1), grid[i][j])
        self.reset()

    def nextStep(self):
        self.openList.sort(key=lambda x: x.f, reverse=True)
        cell = self.openList.pop()
        cell.getNeighbours()
        return cell

def main():
    game = Game()
    game.start()
    gtk.main()

if __name__ == '__main__':
    main()
