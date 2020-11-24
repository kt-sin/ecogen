#!/usr/bin/python

import getopt, sys, random
import ecosystem

# CLASS holds organic objects - with a genome, location, energy, age

class Game:
    def __init__(self):
        self.height = 100
        self.width = 100
        self.round = 1
        self.population = []
        self.score = 0
        self.board = ecosystem()
#        self.board = ecosystem(height,width)
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
