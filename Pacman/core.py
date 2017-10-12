####################
###### PACMAN ######
####################

## Imports
import random
import tkinter as tk
import math
import time

## Opening and reading of the config file
configFile = open("config", "r")
config = configFile.read()
tabConfig = config.split( )
iTick = 0
agentTypes = None

parameters = 16
for i in range(parameters):
    code = compile((tabConfig[2 * i]) [:-1] + " = " + tabConfig[ 2 * i +1],  '<string>', 'exec')
    eval(code, globals(), globals())


agents = []
if(nbTicks == 0):
    nbTicks -= 1

def getTicks():
    return iTick

class DrawApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=boxSize*gridSizeX, height=boxSize*gridSizeY, borderwidth=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.cellwidth = self.cellheight = boxSize
        # self.cellheight = boxSize

        self.redraw(delay)

    def redraw(self, delay):
        global iTick
        global agentTypes
        start_time = time.time()
        if (iTick % refresh == 0):
            self.canvas.delete("all");
            if (grid):
                for row in range(gridSizeY):
                    x1 = 0
                    y1 = row * self.cellheight
                    x2 = (gridSizeX)*self.cellwidth
                    y2 = y1
                    self.canvas.create_line(x1,y1,x2,y2)
                for column in range(gridSizeX):
                    x1 = column*self.cellwidth
                    y1 = 0
                    x2 = x1
                    y2 = (gridSizeY) *self.cellwidth
                    self.canvas.create_line(x1,y1,x2,y2)
            for agent in agents:
                x1 = agent.posX * self.cellwidth
                y1 = agent.posY * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.canvas.create_rectangle(x1,y1,x2,y2, fill=agent.getColor(), width=0)

        if (iTick != nbTicks):
            SMA.runOnce(agents)
            if(trace):
                str1 = ""
                for agentType in agentTypes:
                    cpt = 0
                    for agent in agents:
                        if (agent.__class__.__name__ == agentType):
                            cpt+=1
                    str1 += ";"+ agentType+ "; "+str(cpt)


                print("Tick;", iTick, str1)
            iTick += 1
            elapsed_time = time.time() - start_time
            self.after(max(delay - int(elapsed_time*100),1), lambda: self.redraw(delay))

## SMA class (Scheduler)
## Main class of the application, launch all the agents
class SMA:
    def run(fcreation, drawAppClass = DrawApp):
        global agentTypes
        if (seed != 0):
            random.seed(seed)

        fcreation
        agentTypes = [ e for e in map(lambda x : x.__name__, Agent.__subclasses__()) if (e in map(lambda x : x.__class__.__name__, agents))]
        drawApp = drawAppClass()
        drawApp.mainloop()

    def runOnce(agents):
        if(sheduling == "random"):
            for i in range(nbParticles):
                agents[random.randrange(nbParticles)].doIt()
        else:
            if (sheduling == "fair" ):
                random.shuffle(agents)
            elif (not(sheduling == "sequential")):
                raise Exception("sheduling : incorrect argument")
            for agent in agents:
                agent.doIt()


## Agent class
## Define the attributes of an agent
class Agent:
    # Constructor of the class
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY

    # Setter of the position of an agent in the environment
    def setXY(self, posX, posY):
        Environment.grid[self.posY][self.posX] = 0
        self.posX = posX
        self.posY = posY
        Environment.grid[self.posY][self.posX] = self

    # Define a translation for an agent
    def translate(self, x, y):
        self.setXY((self.posX + x) % gridSizeX, (self.posY + y) % gridSizeY)


## Environment class
## Define the grid of the environment for the agents
class Environment:
    grid = [[0] * gridSizeX for _ in range(gridSizeY)]
