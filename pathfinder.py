from __future__ import division
import pygame, random, time, sys, math, decimal
from config import Config
from grid import Grid
from pygame.locals import *
pygame.init()

# Click to set start, then finish, then walls
# Spacebar to solve
# Debugging:
# Ctrl+Click to highlight, Alt+Click to toggle text

DKGREY    = (50,50,50)

class Game():

        def __init__(self):

                config = Config()
                config.load('config.yaml')

                self.cellfont = pygame.font.SysFont('arial',10)

                self.SCREENWIDTH, self.SCREENHEIGHT = (config.grid_width * config.cell_width, config.grid_height * config.cell_height)
                self.surface = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT))
                pygame.display.set_caption('Pathfinder')
                self.grid = Grid(config.grid_width, config.grid_height, config.cell_width, config.cell_height, self.surface, self)
                self.fpsClock = pygame.time.Clock()
                self.fps = config.fps

                self.solving = 0
                self.openList = []
                self.closedList = []

                print 'filling surface'
                self.surface.fill(DKGREY)
                print 'drawing grid'
                self.grid.draw()

        def reset(self):
                keys = pygame.key.get_pressed()
                self.solving = 0
                self.openList = []
                self.closedList = []
                if keys[K_LSHIFT]:
                        self.grid = Grid(self.grid.width, self.grid.height, self.grid.cell_width, self.grid.cell_heigtht, self.surface, self)
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
                print 'starting game loop'
                while True:
                        for event in pygame.event.get(QUIT): # get all the QUIT events
                                print 'quit'
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

                        pygame.display.update()
                        self.fpsClock.tick(self.fps)

        def solve(self):
                if self.grid.startSet and self.grid.targetSet:
                        print 'Solving'
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
                                        print 'found path!'
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
                                                pygame.time.delay(125)
                                                pygame.display.update()
                                        break

                                self.closedList.append(current)

                                found = 0
                                for cell in current.neighbours:
                                        if cell in self.closedList:
                                                print 'closed'
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
                                        pygame.time.delay(300)
                                print len(self.openList)
                                pygame.display.update()
                                current.current = 0
                                current.draw()
                        else:
                                print 'Failure'
                        self.solving = 0
                else:
                        print 'Error: I need a start and finish!'

        def nextStep(self):
                self.openList.sort(key=lambda x: x.f, reverse=True)
                cell = self.openList.pop()
                cell.getNeighbours()
                return cell

                '''_cell.getNeighbours()
                # Step 1 - put start in closed list and get adjacent
                for cell in _cell.neighbours:
                        self.openList.append(cell)

                for cell in self.openList:
                        cell.g = self.solving
                        cell.h = cell.calcH()
                        cell.f = cell.calcF()
                        cell.updateText()
                        cell.drawText = 1
                        cell.highlight = 1
                        cell.draw()


                print cell.f
                if cell == self.grid.target:
                        print 'found target!'
                        self.solving = 0
                        return
                self.closedList.append(cell)

                self.nextStep(cell)
        #walls = ((3,9),(7,9),(5,7), (3,6),(7,6),(3,5),(4,5),(5,5),(6,5),(7,5))
        #for coords in walls:
                #x, y = coords
                #theGrid.cell(x, y).wall = 1

        #theGrid.cell(1, 1).start = 1    
        #theGrid.cell(10,10).target = 1

        #for x in theGrid.cell(5, 7).neighbours:
                #x.highlight = 1
                #x.draw()       '''


def main():
    game = Game()
    game.start()

if __name__ == '__main__':
    main()
