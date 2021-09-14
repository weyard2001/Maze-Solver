import pygame
import tkinter as tk
import utils
import config as cf

master = tk.Tk()

def onSubmit():
    try:
        mazeWidth, mazeHeight = int(mazeSizeX.get()), int(mazeSizeY.get())

        # bitwise operation included to turn even input sizes into odd sizes since maze initializes passages at every other cell.
        # i.e. with even number of cells, there'll be empty cells at the edges of the maze.
        cf.mazeWidth = mazeWidth + (not mazeWidth & 1)
        cf.mazeHeight = mazeHeight + (not mazeHeight & 1)

        cf.scrWidth = cf.mazeWidth * cf.cellSize
        cf.scrHeight = cf.mazeHeight * cf.cellSize

        cf.endPos = (cf.mazeWidth - 1, cf.mazeHeight - 1)
    except:
        pass

    master.quit()
    master.destroy()

mazeAlgorithm = 0
def setMaze(key):
    global mazeAlgorithm
    mazeAlgorithm = mazeAlgorithms[key]

pathfindingAlgorithm = 0
def setPathfinding(key):
    global pathfindingAlgorithm
    pathfindingAlgorithm = pathfindingAlgorithms[key]

mazeAlgorithms = {
    'Recursive Backtrack': 0,
    'Recursive Division': 1,
    'Randomized Kruskal': 2,
    'Randomized Prim': 3
}

pathfindingAlgorithms = {
    'Left-Hand Rule': 0,
    'Breadth-First Search': 1
}

tk.Label(master, text = "Maze Size").grid(row = 0, column = 0)
tk.Label(master, text = "Width").grid(row = 0, column = 1)
tk.Label(master, text = "Height").grid(row = 0, column = 3)
tk.Label(master, text = "Maze Generation Algorithms").grid(row = 1, column = 0)
tk.Label(master, text = "Pathfinding Algorithms").grid(row = 3, column = 0)

mazeSizeX = tk.Entry(master)
mazeSizeX.grid(row = 0, column = 2)
mazeSizeY = tk.Entry(master)
mazeSizeY.grid(row = 0, column = 4)

for i, key in enumerate(mazeAlgorithms):
    tk.Button(master, text = key, command = lambda key = key: setMaze(key)).grid(row = 2, column = i)

for i, key in enumerate(pathfindingAlgorithms):
    tk.Button(master, text = key, command = lambda key = key: setPathfinding(key)).grid(row = 4, column = i)

tk.Button(master, text = "Generate Maze", command = onSubmit).grid(columnspan = 2, row = 5)

master.update()
master.mainloop()

def main():
    from maze import Maze
    from pathfinding import Pathfinding

    pygame.init()
    cf.scr = pygame.display.set_mode((cf.scrWidth, cf.scrHeight))

    Pathfinding(Maze(mazeAlgorithm), pathfindingAlgorithm)

    while True:
        utils.checkPygameEvents()

if __name__ == '__main__':
    main()