## Imports
from core import *

## Fishes class (inherit from Agent)
class Fishes(Agent):
    # Constructor
    def __init__(self, posX, posY):
        Agent.__init__(self, posX, posY)
        self.FishBreedTime = FishBreedTime
        self.countBreed = 0
        self.isNew = False

    # Method to create a fish agent at a random position
    def createAgents(nbFishes):
        i = 0
        while(i != nbFishes):
            posX = random.randint(0, gridSizeX-1)
            posY = random.randint(0, gridSizeY-1)
            if(Environnement.grille[posY][posX] == 0):
                fish = Fishes(posX, posY)
                Environnement.grille[posY][posX] = fish
                agents.append(fish)
                i += 1

    # Method that define the behavior of a fish
    def doIt(self):
        # Creation of the list of all the ajadent squares of the agent
        possibleSquareList = [(self.posX - 1, self.posY), (self.posX, self.posY + 1), (self.posX + 1, self.posY), (self.posX, self.posY - 1)]

        # If thorus = 1, we can move
        if (thorus):
            possibleSquareList = map(lambda e : (e[0] % gridSizeX, e[1] % gridSizeY), possibleSquareList)

        # If thorus = 0, we delete the squares at the edges
        else:
            possibleSquareList = [e for e in possibleSquareList if not( e[0] < 0 or e[0] >= gridSizeX or e[1] < 0 or e[1] >= gridSizeY) ]

        # List of all the free squares
        freeSquareList = [ e for e in possibleSquareList if not(Environnement.grille[e[1]][e[0]] != 0) ]
        # If there is no free squares, we don't move and  countBreed += 1
        if(len(freeSquareList) == 0):
            self.countBreed += 1
            if(self.countBreed == self.FishBreedTime):
                self.countBreed -= 1
            self.isNew = False;

        # If the destination is free, we move and  countBreed += 1
        else:
            # Actual position
            posXC = self.posX
            posYC = self.posY

            # Choice of the new position
            newSquare =random.choice(freeSquareList);

            # Compute the position after the move
            posXF = newSquare[0]
            posYF = newSquare[1]

            # If countBreed is equal to the breed time, the fish reproduce
            if(self.countBreed == self.FishBreedTime):
                fish = Fishes(posXC, posYC)
                Environnement.grille[posYC][posXC] = fish
                agents.append(fish)
                if(trace_eve):
                    print("Fish;", posXC,";", posYC)
                self.countBreed = 0
                self.isNew = True;
            else:
                Environnement.grille[self.posY][self.posX] = 0
                self.countBreed += 1
                self.isNew = False;

            self.posX = posXF
            self.posY = posYF
            Environnement.grille[self.posY][self.posX] = self

    # Getter on the color of the fish
    def getColor(self):
        if (self.isNew):
            return "green"
        else: return "blue"


## Sharks class (inherit from Agent)
class Sharks(Agent):
    # Constructor
    def __init__(self, posX, posY):
        Agent.__init__(self, posX, posY)
        self.SharkBreedTime = SharkBreedTime
        self.SharkStarveTime = SharkStarveTime
        self.countBreed = 0
        self.countStarve = 0
        self.isNew = False

    # Method to create a shark agent at a random position
    def createAgents(nbSharks):
        i = 0
        while(i != nbSharks):
            posX = random.randint(0, gridSizeX-1)
            posY = random.randint(0, gridSizeY-1)
            if(Environnement.grille[posY][posX] == 0):
                shark = Sharks(posX, posY)
                Environnement.grille[posY][posX] = shark
                agents.append(shark)
                i += 1

    # Method that define the behavior of a shark
    def doIt(self):
        # Creation of the list of all the ajadent squares of the agent
        possibleSquareList = [(self.posX - 1, self.posY), (self.posX, self.posY + 1), (self.posX + 1, self.posY), (self.posX, self.posY - 1)]

        # Actual position
        posXC = self.posX
        posYC = self.posY
        movement = False
        eat = False
        newSquare = None

        # If thorus = 1, we can move
        if (thorus):
            possibleSquareList2 = [];
            for e in possibleSquareList:
                possibleSquareList2.append((e[0] % gridSizeX, e[1] % gridSizeY));
            possibleSquareList = possibleSquareList2;


        # If thorus = 0, we delete the squares at the edges
        else:
            possibleSquareList = [e for e in possibleSquareList if not( e[0] < 0 or e[0] >= gridSizeX or e[1] < 0 or e[1] >= gridSizeY) ]


        # List of all the squares with a fish
        fishSquareList = [ e for e in possibleSquareList if (Environnement.grille[e[1]][e[0]] != 0 and Environnement.grille[e[1]][e[0]].__class__.__name__ == "Fishes") ]
        if(len(fishSquareList) == 0):
            freeSquareList = [ e for e in possibleSquareList if not(Environnement.grille[e[1]][e[0]] != 0) ]
            # If there is no free squares, we don't move and  countBreed += 1
            if(len(freeSquareList) == 0):
                self.countBreed += 1
                if(self.countBreed == self.SharkBreedTime):
                    self.countBreed -= 1
                self.isNew = False;

            # If the destination is free, we move and  countBreed += 1
            else:
                # choice of the new position
                newSquare =random.choice(freeSquareList)
                movement = True
        else:
            # Choice of the new position
            newSquare =random.choice(fishSquareList)
            movement = True
            eat = True
        if (movement):
            # Compute the position after the move
            posXF = newSquare[0]
            posYF = newSquare[1]

            if (eat):
                self.countStarve = 0
                agents.remove(Environnement.grille[posYF][posXF])

            # If countBreed is equal to the breed time, the fish reproduce
            if(self.countBreed == self.SharkBreedTime):
                shark = Sharks(posXC, posYC)
                Environnement.grille[posYC][posXC] = shark
                agents.append(shark)
                if(trace_eve):
                    print("Shark;", posXC,";", posYC)
                self.countBreed = 0
                self.isNew = True;
            else:
                Environnement.grille[self.posY][self.posX] = 0
                self.countBreed += 1
                self.isNew = False;

            self.posX = posXF
            self.posY = posYF
            Environnement.grille[self.posY][self.posX] = self
        self.countStarve += 1

        # If a shark is straving, he dies
        if(self.countStarve == self.SharkStarveTime):
            Environnement.grille[self.posY][self.posX] = 0
            agents.remove(self)

    # Getter on the color of the shark
    def getColor(self):
        if (self.isNew):
            return "pink"
        else: return "red"


## Fonction to create all the agents of the simulation
def createAgents():
    Fishes.createAgents(nbFishes)
    Sharks.createAgents(nbSharks)

## Application start here
SMA.run(createAgents())
