import pygame
import queue
import enum
import utils
import config as cf
from maze import Maze
from collections import deque

class Pathfinding():
    class Algorithms(enum.Enum):
        LEFT_HAND_RULE = 0
        BREADTH_FIRST_SEARCH = 1

    def __init__(self, maze, algo):
        self.__solution = deque()
        self.__examined = {}

        self.__maze = maze

        algorithms = {
            Pathfinding.Algorithms.LEFT_HAND_RULE: self.__leftHandRule,
            Pathfinding.Algorithms.BREADTH_FIRST_SEARCH: self.__breadthFirstSearch
        }

        algorithms[Pathfinding.Algorithms(algo)]()
        self.__traceSolution()

    def __leftHandRule(self):
        # 0 = N, 1 = E, 2 = S, 3 = W
        face = [
            lambda x, y: ((x - 1, y), (x, y - 1)),
            lambda x, y: ((x, y - 1), (x + 1, y)),
            lambda x, y: ((x + 1, y), (x, y + 1)),
            lambda x, y: ((x, y + 1), (x - 1, y))
        ]

        n = len(face)
        curPos = cf.startPos
        self.__maze.cells[curPos].visited = True

        dir_ = 2
        leftCell, nextCell = face[dir_](*curPos)
        utils.draw(*curPos, cf.RED, 0.02)

        self.__solution.append(curPos)
        while curPos != cf.endPos:
            if self.__maze.isPassage(leftCell):
                # rotate CCW
                dir_ = (dir_ - 1) % n
                leftCell, nextCell = face[dir_](*curPos)
            elif not self.__maze.isPassage(nextCell):
                # rotate CW
                dir_ = (dir_ + 1) % n
                leftCell, nextCell = face[dir_](*curPos)

                continue

            if self.__maze.cells[nextCell].visited:
                self.__examined[self.__solution.pop()] = None
            else:
                self.__maze.cells[nextCell].visited = True
                self.__solution.append(nextCell)

            utils.draw(*nextCell, cf.RED, 0.02, False)
            utils.draw(*curPos, cf.CYAN, 0.02)

            curPos = nextCell
            leftCell, nextCell = face[dir_](*curPos)

    def __breadthFirstSearch(self):
        qu = queue.Queue()
        qu.put(cf.startPos)

        backtrack = {}
        while not qu.empty():
            curPos = qu.get()
            self.__maze.cells[curPos].visited = True
            self.__examined[curPos] = None
            utils.draw(*curPos, cf.CYAN)

            if curPos == cf.endPos:
                break

            for neighbor in self.__maze.getNeighbors(curPos):
                if not self.__maze.cells[neighbor].visited:
                    backtrack[neighbor] = curPos
                    qu.put(neighbor)

        nextBacktrackPos = cf.endPos
        self.__examined.pop(nextBacktrackPos)
        self.__solution.appendleft(nextBacktrackPos)
        while nextBacktrackPos in backtrack:
            self.__examined.pop(backtrack[nextBacktrackPos])
            self.__solution.appendleft(backtrack[nextBacktrackPos])
            nextBacktrackPos = backtrack[nextBacktrackPos]

    def __traceSolution(self):
        for pos in self.__solution:
            if pos == cf.startPos or pos == cf.endPos:
                utils.draw(*pos, cf.RED, 0.02)
            else:
                utils.draw(*pos, cf.GREEN, 0.02)

        for pos in self.__examined:
            utils.draw(*pos, cf.WHITE)