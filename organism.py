#!/usr/bin/python


import getopt, sys, random
import genome

# CLASS holds organic objects - with a genome, location, energy, age


class Organism:
    def __init__(self, mother, father, location, energy, species):
        self.data = []
        self.age = 1
        self.geno = (genome.Genome(mother,father,1)).get_geno()
        self.x = location[0]
        self.y = location[1]
        self.loc = [self.x,self.y]
        self.energy = energy
        self.energy_cost = int(.05 * energy)
        self.speed = self.getStats(1,self.energy)
        self.species = species

    def getStats(self,age,energy):
        baseline = (122-(ord(self.geno[0])) + (122-ord(self.geno[1])))
        speed = baseline - (int(age/10)) + (int(energy/10))
        return speed


    def move(self,max_size):
        r = (random.randint(1,10))
        r_dir = random.randint(1,4)
        rev = (11-r)
        rate = self.speed
        a = rate * (10/r)
        b = rate * (10/rev)
        if r_dir == 1:
            a = -a
        if r_dir == 2:
            b = -b
        self.x = self.x + int(a)
        self.y = self.y + int(b)
        if self.x > max_size[0] or self.x < 0:
            self.x -= a
        if self.y > max_size[1] or self.y < 0:
            self.y -= a
        print([self.x,self.y])
        self.energy -= self.energy_cost
        

    def age(self):
        self.age += 1
        self.getStats(self.age,self.energy)

    def eat(self,energy):
        self.energy += energy
        return self.energy

    def print_details(self):
        print('Organism: %s' % self.species)
        print('Genome: %s' % self.geno)
        print('Energy: %s' % self.energy)
        print('Speed: %s' % self.speed)
        print('Location: %s' % self.loc)

#if __name__ == "__main__":
    # execute only if run as a script
#    main()


