# Wator

The aim of this project is to understand the basis of multi-agent systems
In this project all the objects shown in the window are different kind of agents.

The application was developed with Python and Tkinter as graphical interface.

I developed a predators and preys simulation based on the ecosystem of sharks and fishes.
When the simulation is running, we can observe the dynamics of the populations.

### The rules are:
* For Fishes
  * At each tick, a fish  moves randomly to one adjacent square (based on the moore neighborhood). If there is no free square, the fish doesn't move.
  * If a fish has survived a certain number of ticks, it can reproduce if a movement is possible. The new born fish take the old position of the fish.

* For sharks
  * At each tick, a shark  moves randomly to one adjacent square (based on the moore neighborhood) occupied by a fish. If there is no fish, the shark moves randomly to one adjacent square. If there is no free square, the shark doesn't move.
  * At each tick, a shark looses a point of energy
  * If the energy of a shark reaches 0, the shark dies.
  * If a shark moves to a position occupied by a fish, he eats it and gain a certain amount of energy.
  * If a shark has survived a certain number of ticks, it can reproduce if a movement is possible. The new born shark take the old position of the shark.

### Observations
For an initial grid of 90x90 squares, with a fish population of 700 and a shark population of 700, we can observe that the sharks eat almost all the fishes but when there is not enough fishes left, almost all the sharks die and the fish population rise again. Then the simulation loop indefinitly.

### Files
The different files of this project are:
* core.py: the core of the application
* wator.py: all the classes for the wator simulation
* config: configuration file for the simulation
