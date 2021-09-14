import pygame
import random
import union_find as uf
import enum
import utils
import config as cf

class Cell():
    def __init__(self, isPassage, visited = False):
        # self.neighbors = {}

        self.isPassage = isPassage
        self.visited = False
        # self.color = cf.WHITE

class Maze():
    getCell = {
        'UP': lambda x, y, cellCount: (x, y - 1 * cellCount),
        'RIGHT': lambda x, y, cellCount: (x + 1 * cellCount, y),
        'DOWN': lambda x, y, cellCount: (x, y + 1 * cellCount),
        'LEFT': lambda x, y, cellCount: (x - 1 * cellCount, y)
    }

    class Algorithms(enum.Enum):
        RECURSIVE_BACKTRACK = 0
        RECURSIVE_DIVISION = 1
        RANDOMIZED_KRUSKAL = 2
        RANDOMIZED_PRIM = 3

    def __init__(self, algo):
        self.cells = {}

        self.__bounds = (0, 0, cf.mazeWidth - 1, cf.mazeHeight - 1)
        self.__drawColor = cf.WHITE

        startAsPassage = False

        if Maze.Algorithms(algo) == Maze.Algorithms.RECURSIVE_DIVISION:
            self.__drawColor = cf.BLACK
            startAsPassage = True
        
        for row in range(0, cf.mazeWidth):
            for clm in range(0, cf.mazeHeight):
                self.cells[(row, clm)] = Cell(startAsPassage)

        cf.scr.fill(cf.BLACK if Maze.Algorithms(algo) != Maze.Algorithms.RECURSIVE_DIVISION else cf.WHITE)

        algorithms = {
            Maze.Algorithms.RECURSIVE_BACKTRACK: self.__recursiveBacktrack,
            Maze.Algorithms.RECURSIVE_DIVISION: self.__recursiveDivision,
            Maze.Algorithms.RANDOMIZED_KRUSKAL: self.__kruskal,
            Maze.Algorithms.RANDOMIZED_PRIM: self.__prim
        }

        algorithms[Maze.Algorithms(algo)]()

    def inBounds(self, pos):
        return pos in self.cells

    def isPassage(self, pos):
        return self.inBounds(pos) and self.cells[pos].isPassage

    def getNeighbors(self, pos, space = 1, checkIfPassage = True):
        neighbors = []

        for cell in Maze.getCell.values():
            neighbor = cell(*pos, space)

            if self.inBounds(neighbor) and (not checkIfPassage ^ self.cells[neighbor].isPassage):
                neighbors.append(neighbor)

        return neighbors

    def __recursiveBacktrack(self, x = 0, y = 0, carved = set()):
        utils.checkPygameEvents()

        self.cells[(x, y)].isPassage = True
        utils.draw(x, y, cf.RED)
        utils.draw(x, y, self.__drawColor, update = False)

        carved.add((x, y))

        paths = self.__shuffleNeighbors()
        for p in paths:
            join = Maze.getCell[p](x, y, 2)

            if self.inBounds(join) and join not in carved:
                midX, midY = Maze.getCell[p](x, y, 1)

                self.cells[(midX, midY)].isPassage = True
                utils.draw(midX, midY, cf.RED)
                utils.draw(midX, midY, self.__drawColor, update = False)

                self.__recursiveBacktrack(*join, carved)
                
                # this cell has visited all its neighbors, begin backtracking.
                utils.draw(midX, midY, cf.RED)
                utils.draw(midX, midY, self.__drawColor, update = False)
                utils.draw(x, y, cf.RED)
                utils.draw(x, y, self.__drawColor, update = False)

    def __recursiveDivision(self, x1 = 0, y1 = 0, x2 = cf.mazeWidth - 1, y2 = cf.mazeHeight - 1):
        utils.checkPygameEvents()

        if x2 - x1 <= 1 or y2 - y1 <= 1:
            return

        width, height = x2 - x1 + 1, y2 - y1 + 1
        if width > height:
            ori = self.__Orientation.VERTICAL
        elif width < height:
            ori = self.__Orientation.HORIZONTAL
        else:
            ori = self.__Orientation(random.randint(0, 1))

        drawX = x1 if ori == self.__Orientation.HORIZONTAL else random.randrange(x1 + 1, x2 + 1, 2)
        drawY = y1 if ori == self.__Orientation.VERTICAL else random.randrange(y1 + 1, y2 + 1, 2)

        holeX = drawX if ori == self.__Orientation.VERTICAL else random.randrange(x1, x2 + 1, 2)
        holeY = drawY if ori == self.__Orientation.HORIZONTAL else random.randrange(y1, y2 + 1, 2)

        if ori == self.__Orientation.HORIZONTAL:
            for curX in range(drawX, x2 + 1):
                if curX != holeX:
                    self.cells[(curX, drawY)].isPassage = False
                    utils.draw(curX, drawY, self.__drawColor)
        else:
            for curY in range(drawY, y2 + 1):
                if curY != holeY:
                    self.cells[(drawX, curY)].isPassage = False
                    utils.draw(drawX, curY, self.__drawColor)

        # generate walls for first-half of current grid.
        nX = x2 if ori == self.__Orientation.HORIZONTAL else drawX - 1
        nY = y2 if ori == self.__Orientation.VERTICAL else drawY - 1
        self.__recursiveDivision(x1, y1, nX, nY)

        # and generate walls for its second-half.
        nX = x1 if ori == self.__Orientation.HORIZONTAL else drawX + 1
        nY = y1 if ori == self.__Orientation.VERTICAL else drawY + 1
        self.__recursiveDivision(nX, nY, x2, y2)

    def __kruskal(self):
        utils.checkPygameEvents()

        edges = []

        for x in range(0, cf.mazeWidth, 2):
            for y in range(0, cf.mazeHeight, 2):
                uf.create((x, y))

                if self.inBounds((x, y + 2)):
                    edges.append((x, y + 1, self.__Orientation.HORIZONTAL))

                if self.inBounds((x + 2, y)):
                    edges.append((x + 1, y, self.__Orientation.VERTICAL))

        random.shuffle(edges)
        while edges:
            x, y, wallDir = edges.pop()

            pos1 = (x, y - 1) if wallDir == self.__Orientation.HORIZONTAL else (x - 1, y)
            pos2 = (x, y + 1) if wallDir == self.__Orientation.HORIZONTAL else (x + 1, y)

            if not uf.sameSet(pos1, pos2):
                self.cells[pos1].isPassage = self.cells[(x, y)].isPassage = self.cells[pos2].isPassage = True

                utils.draw(*pos1, self.__drawColor)
                utils.draw(x, y, self.__drawColor)
                utils.draw(*pos2, self.__drawColor)

                uf.union(pos1, pos2)

    def __prim(self):
        utils.checkPygameEvents()

        frontier = set()

        initCell = (random.randrange(0, cf.mazeWidth, 2), random.randrange(0, cf.mazeHeight, 2))
        self.cells[initCell].isPassage = True

        for neighbor in self.getNeighbors(initCell, 2, False):
            frontier.add(neighbor)
            utils.draw(*neighbor, cf.RED)

        while frontier:
            curFront = frontier.pop()

            utils.draw(*curFront, self.__drawColor)

            paths = self.__shuffleNeighbors()
            for p in paths:
                join = Maze.getCell[p](*curFront, 2)
                if self.inBounds(join) and self.cells[join].isPassage:
                    mid = (curFront[0] + (join[0] - curFront[0]) // 2, curFront[1] + (join[1] - curFront[1]) // 2)
                    self.cells[curFront].isPassage = self.cells[mid].isPassage = True

                    utils.draw(*mid, self.__drawColor)
                    utils.draw(*join, self.__drawColor)

                    break

            for neighbor in self.getNeighbors(curFront, 2, False):
                if neighbor not in frontier:
                    frontier.add(neighbor)
                    utils.draw(*neighbor, cf.RED)

    def __shuffleNeighbors(self):
        paths = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        random.shuffle(paths)

        return paths

    class __Orientation(enum.Enum):
        HORIZONTAL = 0
        VERTICAL = 1