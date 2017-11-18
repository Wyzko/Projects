## Imports
from core import *
from queue import *
import sys

## Variables initialization
gridDijskra = [[-1] * gridSizeX for _ in range(gridSizeY)]
queue = None
finish = False;
first = True

## Method to generate the queue for the Dijkstra algorithm
def dijkstragen(i,j):
    global queue
    queue = Queue(0)
    queue.put(lambda : dijkstra(i, j, 0, -2,-2))
    while(not queue.empty()):
        queue.get()()

## Method to calculate the shortest path with the Dijkstra algorithm
def dijkstra(i, j, dist, dirX, dirY):
    if (Environment.grid[j][i].__class__.__name__ != "Wall" ):
        if gridDijskra[j][i] == -1 or dist < gridDijskra[j][i]:
            gridDijskra[j][i] = dist
            if (thorus):
                if (dirX != -1 and dirY !=0):
                    queue.put(lambda : dijkstra((i + 1) % gridSizeX, j, dist + 1, 1, 0 ))
                if (dirX != 1 and dirY !=0):
                    queue.put(lambda : dijkstra((i - 1) % gridSizeX, j, dist + 1, -1, 0 ))
                if (dirX != 0 and dirY !=-1):
                    queue.put(lambda : dijkstra(i, (j+1) % gridSizeY, dist + 1, 0, 1 ))
                if (dirX != 0 and dirY !=1):
                    queue.put(lambda : dijkstra(i, (j-1) % gridSizeY, dist + 1, 0,-1 ))
            else:
                if (dirX != -1 and dirY !=0 and i+1 < gridSizeX):
                    queue.put(lambda : dijkstra((i + 1) , j, dist + 1, 1, 0 ))
                if (dirX != 1 and dirY !=0 and i-1 >= 0):
                    queue.put(lambda : dijkstra((i - 1) , j, dist + 1, -1, 0 ))
                if (dirX != 0 and dirY !=-1 and j+1 < gridSizeY):
                    queue.put(lambda : dijkstra(i, (j+1) , dist + 1, 0, 1 ))
                if (dirX != 0 and dirY !=1 and j-1 >= 0):
                    queue.put(lambda : dijkstra(i, (j-1) , dist + 1, 0,-1 ))


## Method to generate a defender or a winner according the points of the avatar
def defendergen():
    if(Avatar.current_agent.nbDefender == 1):
        print(Avatar.current_agent.nbDefender)
        Winner.createAgents()
    else:
        Defender.createAgents()


## Avatar class (inherit from Agent)
## The Avatar is a special agent controlled by the user
class Avatar(Agent):
    current_agent = None;
    # Constructor
    def __init__(self, posX, posY):
        Agent.__init__(self, posX, posY)
        Avatar.current_agent = self
        self.dirX = 0
        self.dirY = 0
        self.nbDefender = 0
        self.invincible = 0

    # Method to create the avatar at the center of the windows
    def createAgents():
        avatar = Avatar(int(gridSizeX/2), int(gridSizeY/2))
        Environment.grid[int(gridSizeY/2)][int(gridSizeX/2)]
        agents.append(avatar)

    # If the avatar moves on a special agent, we check the type of agent
    # If it's a wall, the avatar stop moving, if it's a defender, the user gain a point and the hunters will avoid the avatar for a brief moment, if it's a winner, the user wins the game, if it's a hunter, he loses the game
    def doIt(self):
        global finish
        if(getTicks() % SpeedAvatar == 0):
            posXf = self.posX + self.dirX
            posYf = self.posY + self.dirY

            if(not(thorus)):
                if(posYf < 0 or posYf >= gridSizeY or posXf < 0 or posXf >= gridSizeX):
                    self.dirX = 0
                    self.dirY = 0
                    return
            else:
                posXf = posXf % gridSizeX
                posYf = posYf % gridSizeY

            if(Environment.grid[posYf][posXf] != 0):
                if (Environment.grid[posYf][posXf].__class__.__name__ == "Hunter"):
                    Environment.grid[self.posY][self.posX] = 0
                    agents.remove(self)
                    print("You lost !")
                    finish = True
                    return
                elif(Environment.grid[posYf][posXf].__class__.__name__ == "Defender"):
                    agents.remove(Environment.grid[posYf][posXf])
                    Environment.grid[posYf][posXf] = 0
                    defendergen()
                    self.nbDefender += 1
                    self.invincible = 100

                elif(Environment.grid[posYf][posXf].__class__.__name__ == "Winner"):
                    print("You won !")
                    finish = True
                else:
                    self.dirX = 0
                    self.dirY = 0
            else:
                if self.invincible > 0:
                    self.invincible -= 1
            self.translate(self.dirX, self.dirY)


            # Dijkstra calculation
            for i in range(gridSizeY):
                for j in range(gridSizeX):
                    gridDijskra[i][j] = -1

            dijkstragen(self.posX, self.posY)

    # Getter on the color of the avatar
    def getColor(self):
        return "green"


## Wall class (inherit from Agent)
## A Wall is a special agent that does nothing
class Wall(Agent):
    # Constructor
    def __init__(self, posX, posY):
        Agent.__init__(self, posX, posY)

    # Method to create all the walls at a random position according a percentage
    def createAgents(pourcentage):
        nbWall = (gridSizeX * gridSizeY) * (pourcentage / 100)
        i = 0

        while(i != nbWall):
            posX = random.randint(0, gridSizeX-1)
            posY = random.randint(0, gridSizeY-1)

            if(Environment.grid[posY][posX] == 0 and (posX != gridSizeX/2 or posY != gridSizeY/2)):
                wall = Wall(posX, posY)
                Environment.grid[posY][posX] = wall
                agents.append(wall)
                i += 1

    # A wall does nothing
    def doIt(self):
        pass

    # Getter on the color of a wall
    def getColor(self):
        return "black"


## Hunter class (inherit from Agent)
## A hunter is a special agent who will hunt the avatar to eat him
class Hunter(Agent):
    # Constructor
    def __init__(self, posX, posY):
        Agent.__init__(self, posX, posY)

    # Method to create all the hunters at a random position
    def createAgents(nbHunters):
        i = 0

        while(i != nbHunters):
            posX = random.randint(0, gridSizeX-1)
            posY = random.randint(0, gridSizeY-1)

            if(Environment.grid[posY][posX] == 0 and (posX != gridSizeX/2 or posY != gridSizeY/2)):
                hunter = Hunter(posX, posY)
                Environment.grid[posY][posX] = hunter
                agents.append(hunter)
                i += 1

    # A hunter will hunt the avatar. A hunter will always try to go by the shortest path to eat the avatar with a Dijkstra algorithm
    def doIt(self):
        global finish
        if(getTicks() % SpeedHunter == 0):
            if not (finish):
                possibleSquareList = [(self.posX - 1, self.posY), (self.posX, self.posY + 1), (self.posX + 1, self.posY), (self.posX, self.posY - 1)]
                if (thorus):
                    possibleSquareList2 = [];
                    for e in possibleSquareList:
                        possibleSquareList2.append((e[0] % gridSizeX, e[1] % gridSizeY))
                    possibleSquareList = possibleSquareList2
                else:
                    possibleSquareList = [e for e in possibleSquareList if not( e[0] < 0 or e[0] >= gridSizeX or e[1] < 0 or e[1] >= gridSizeY) ]
                freeSquareList = [ e for e in possibleSquareList if ((Environment.grid[e[1]][e[0]] == 0) and gridDijskra[e[1]][e[0]] != -1 ) or Environment.grid[e[1]][e[0]].__class__.__name__ == "Avatar"  ]
                if len(freeSquareList) > 0:
                    l = []
                    for d in freeSquareList:
                        l.append (gridDijskra[d[1]][d[0]])
                    if Avatar.current_agent.invincible > 0:
                        indMin = l.index(max(l))
                    else: indMin = l.index(min(l))
                    if (Environment.grid[possibleSquareList[indMin][1]][freeSquareList[indMin][0]].__class__.__name__ == "Avatar"):
                        agents.remove(Environment.grid[possibleSquareList[indMin][1]][freeSquareList[indMin][0]])
                        Environment.grid[possibleSquareList[indMin][1]][freeSquareList[indMin][0]] == 0
                        print("Perdu !")
                        finish = True
                    self.setXY(freeSquareList[indMin][0], freeSquareList[indMin][1])

    # Getter on the color of a hunter
    def getColor(self):
        return "red"


## Defender class (inherit from Agent)
## A Defender is a special agent that appears randomly, if the user eats it, he gains a point. If the user has enough points, a Winner will appear
class Defender(Agent):
    # Constructor
    def __init__(self, posX, posY):
        Agent.__init__(self, posX, posY)
        self.life = 0

    # Method to create the defender at a random position
    def createAgents():
        i = 0

        while(i != 1):
            posX = random.randint(0, gridSizeX-1)
            posY = random.randint(0, gridSizeY-1)

            if(Environment.grid[posY][posX] == 0 and (posX != gridSizeX/2 or posY != gridSizeY/2)):
                defender = Defender(posX, posY)
                Environment.grid[posY][posX] = defender
                agents.append(defender)
                i += 1

    # If the defender die, a new one is created at a random position
    def doIt(self):
        if(self.life == DefenderLife):
            Environment.grid[self.posY][self.posX] = 0
            agents.remove(self)
            defendergen()
        else:
            self.life += 1

    # Getter on the color of a defender
    def getColor(self):
        return "yellow"


## Winner class (inherit from Agent)
## A Winner is a special agent that allow the user to win the game if he eats it
class Winner(Agent):
    # Constructor
    def __init__(self, posX, posY):
        Agent.__init__(self, posX, posY)

    # Method to create the winner agent at a random position
    def createAgents():
        i = 0

        while(i != 1):
            posX = random.randint(0, gridSizeX-1)
            posY = random.randint(0, gridSizeY-1)

            if(Environment.grid[posY][posX] == 0 and (posX != gridSizeX/2 or posY != gridSizeY/2)):
                winner = Winner(posX, posY)
                Environment.grid[posY][posX] = winner
                agents.append(winner)
                i += 1

    # A winner does nothing
    def doIt(self):
        pass

    # Getter on the color of the winner
    def getColor(self):
        return "blue"


## Drawing class (inherit from DrawApp)
## Allow the user to use the keyboard to interact with the avatar, the hunters and the simulation
class Drawing(DrawApp):
    def key(event):
        global SpeedHunter
        global SpeedAvatar
        global delay
        global finish
        # Move up
        if(event.keysym == "Up"):
            Avatar.current_agent.dirX = 0
            Avatar.current_agent.dirY = -1
        # Move left
        if(event.keysym == "Left"):
            Avatar.current_agent.dirX = -1
            Avatar.current_agent.dirY = 0
        # Move down
        if(event.keysym == "Down"):
            Avatar.current_agent.dirX = 0
            Avatar.current_agent.dirY = 1
        # Move right
        if(event.keysym == "Right"):
            Avatar.current_agent.dirX = 1
            Avatar.current_agent.dirY = 0
        # Repositioning of the avatar and the hunters
        if(event.keysym == "space"):
            Environment.grid[Avatar.current_agent.posY][Avatar.current_agent.posX] = 0
            Avatar.current_agent.dirX = 0
            Avatar.current_agent.dirY = 0
            Avatar.current_agent.posX = int(gridSizeX/2)
            Avatar.current_agent.posY = int(gridSizeY/2)
            Environment.grid[Avatar.current_agent.posY][Avatar.current_agent.posX] = Avatar.current_agent

            for agent in agents:
                if(agent.__class__.__name__ == "Hunter"):
                    agent.setXY(random.randint(0, gridSizeX-1), random.randint(0, gridSizeY-1))
        # Reduce the speed of the hunters
        if(event.keysym == "z"):
            SpeedHunter += 1
        # Increase the speed of the hunters
        if(event.keysym == "a"):
            if(SpeedHunter - 1 >= 1):
                SpeedHunter -= 1
        # Reduce the speed of the avatar
        if(event.keysym == "p"):
            SpeedAvatar += 1
        # Increase the speed of the avatar
        if(event.keysym == "o"):
            if(SpeedAvatar - 1 >= 1):
                SpeedAvatar -= 1
        # Slow down the simulation
        if(event.keysym == "x"):
            delay += 50
        # Speed up the simulation
        if(event.keysym == "w"):
            if(delay - 50 >= 15):
                delay -= 50

    # Constructor
    def __init__(self, *args, **kwargs):
        DrawApp.__init__(self, *args, **kwargs)
        self.canvas.bind("<Key>", Drawing.key)
        self.canvas.focus_set()
        self.canvas.pack()

    # Redraw method while the simulation is not over
    def redraw(self, delay):
        global first
        global finish
        if (not finish) :
            DrawApp.redraw(self, delay)
        else:
            if first:
                first = False
                DrawApp.redraw(self, delay)
            else :
                print("end")


## Fonction to create all the agents of the simulation
def createAgents():
    Wall.createAgents(WallPercent)
    Avatar.createAgents()
    defendergen()
    Hunter.createAgents(nbHunters)


## Application start here
SMA.run(createAgents(), Drawing)
