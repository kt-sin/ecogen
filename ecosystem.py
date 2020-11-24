#!/usr/bin/python

import getopt, sys, random
import genome, organism

# CLASS holds organic objects - with a genome, location, energy, age

class ecosystem:
    def __init__(self,width,height):
        new_seed = str(random.random())[2:]
        self.energy = new_seed[1]
        self.nutrients = getNutrients
        self.population = []
#       
        self.board = ecosystem(height,width)
    def updatePopulation(self):
        self.population = board.getPop()

    def setScore(self,points):
        self.score = self.score + points

    def round(self):
        interactors = []
        self.round+=1
        for p in self.population:
            loc = ()
            p.age()
            new_loc = p.move(self.height,self.width)
            board.updateLocation(p, new_loc)

    def print_state(self):
        print('Game: %s | h: %s | w: %s' % ('Etherea', self.height, self.width))
        print('Round: %s' % self.round)
        print('Nutrients: %s | Energy: %s' % (self.board.getNutrients(), self.board.getEnergy()))
        print('Population: %s' % (self.population.getSize()))
