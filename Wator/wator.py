from core import *


class Fishes(Agent):
    def __init__(self, posX, posY):
        Agent.__init__(self, posX, posY)
        self.FishBreedTime = FishBreedTime
        self.countBreed = 0
        self.isNew = False

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

    def doIt(self):
        #creation de la liste des carrés autour de l'agent
        possibleSquareList = [(self.posX - 1, self.posY), (self.posX, self.posY + 1), (self.posX + 1, self.posY), (self.posX, self.posY - 1)]

        # Si thorus = 1, on se déplace
        if (thorus):
            possibleSquareList = map(lambda e : (e[0] % gridSizeX, e[1] % gridSizeY), possibleSquareList)

        # Si thorus = 0, on supprime les case au bord
        else:
            possibleSquareList = [e for e in possibleSquareList if not( e[0] < 0 or e[0] >= gridSizeX or e[1] < 0 or e[1] >= gridSizeY) ]

        #on garde seulement les cases libre
        freeSquareList = [ e for e in possibleSquareList if not(Environnement.grille[e[1]][e[0]] != 0) ]
        # Si aucune casse disponible, on reste sur place, countBreed + 1
        if(len(freeSquareList) == 0):
            self.countBreed += 1
            if(self.countBreed == self.FishBreedTime):
                self.countBreed -= 1 #je pense que c'est de faire -- que 0,parait plus logique/naturel
            self.isNew = False;
        # Si la case destination est libre, on se déplace, countBreed + 1
        else:
            # Récupération position actuelle
            posXC = self.posX
            posYC = self.posY

            # choice of the new position
            newSquare =random.choice(freeSquareList);

            # Calul de la position après le déplacement
            posXF = newSquare[0]
            posYF = newSquare[1]
            # il se reproduit
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

    def getColor(self):
        if (self.isNew):
            return "green"
        else: return "blue"


class Sharks(Agent):
    def __init__(self, posX, posY):
        Agent.__init__(self, posX, posY)
        self.SharkBreedTime = SharkBreedTime
        self.SharkStarveTime = SharkStarveTime
        self.countBreed = 0
        self.countStarve = 0
        self.isNew = False

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

    def doIt(self):
        #creation de la liste des carrés autour de l'agent
        possibleSquareList = [(self.posX - 1, self.posY), (self.posX, self.posY + 1), (self.posX + 1, self.posY), (self.posX, self.posY - 1)]

        # Récupération position actuelle
        posXC = self.posX
        posYC = self.posY
        movement = False
        eat = False
        newSquare = None
        #for e in possibleSquareList:
        #    print(e[0], e[1])
        # Si thorus = 1, on se déplace
        if (thorus):
            #possibleSquareList = map(lambda e : (e[0] % gridSizeX, e[1] % gridSizeY), possibleSquareList)
            possibleSquareList2 = [];
            for e in possibleSquareList:
                possibleSquareList2.append((e[0] % gridSizeX, e[1] % gridSizeY));
            possibleSquareList = possibleSquareList2;


        # Si thorus = 0, on supprime les case au bord
        else:
            possibleSquareList = [e for e in possibleSquareList if not( e[0] < 0 or e[0] >= gridSizeX or e[1] < 0 or e[1] >= gridSizeY) ]


        #on gade seulement les cases occupe par des poissons
        fishSquareList = [ e for e in possibleSquareList if (Environnement.grille[e[1]][e[0]] != 0 and Environnement.grille[e[1]][e[0]].__class__.__name__ == "Fishes") ]
        if(len(fishSquareList) == 0):
            freeSquareList = [ e for e in possibleSquareList if not(Environnement.grille[e[1]][e[0]] != 0) ]
            # Si aucune casse disponible, on reste sur place, countBreed + 1
            if(len(freeSquareList) == 0):
                self.countBreed += 1
                if(self.countBreed == self.SharkBreedTime):
                    self.countBreed -= 1 #je pense que c'est de faire -- que 0,parait plus logique/naturel
                self.isNew = False;
            # Si la case destination est libre, on se déplace, countBreed + 1
            else:
                # choice of the new position
                newSquare =random.choice(freeSquareList)
                movement = True
        else:
            # choice of the new position
            newSquare =random.choice(fishSquareList)
            movement = True
            eat = True
        if (movement):
            # Calul de la position après le déplacement
            posXF = newSquare[0]
            posYF = newSquare[1]

            if (eat):
                self.countStarve = 0
                agents.remove(Environnement.grille[posYF][posXF])
            # il se reproduit
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

        if(self.countStarve == self.SharkStarveTime):
            Environnement.grille[self.posY][self.posX] = 0
            agents.remove(self)


        # Observation du voisinnage en fonction de la position
        # pass

    def getColor(self):
        if (self.isNew):
            return "pink"
        else: return "red"


def createAgents():
    Fishes.createAgents(nbFishes)
    Sharks.createAgents(nbSharks)

SMA.run(createAgents())
