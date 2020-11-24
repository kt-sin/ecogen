#!/usr/bin/python

import getopt, sys, random

# CLASS holds organic objects - with a genome, location, energy, age

class Genome:
    def __init__(self, mother, father, mutation):
        parents = [mother,father]
        self.genotype = self.getGenome(parents)
        # self.phenotype = self.getPhenome(self.genotype)
    def getGenome(self, genetics):
        r = random.randint(0,10)
        mutation_rate = 1
        gen_len = len(genetics)
        c = str()
        if gen_len > 1:
            p1 = genetics[0]
            p2 = genetics[1]
            p1_len = len(p1)
            p2_len = len(p2)
            for i in range (0,p1_len):
                new_ord = 0
                p1_ord = ord(p1[i])
                p2_ord = ord(p2[i])
                if p1_ord > 90 and p2_ord < 90:
                    new_ord = p1_ord
                elif p2_ord > 90 and p1_ord < 90:
                    new_ord = p2_ord
                else:
                    prob = random.randint(1,2)
                    if prob == 1:
                        new_ord = p1_ord
                    if prob == 2:
                        new_ord = p2_ord
                m_prob = random.randint(1,100)    
                if m_prob % 10 == 0:
                    new_ord+=1
                if m_prob % 11 == 0:
                    new_ord-=1
                if m_prob == 5:
                    new_ord+=5
                if m_prob == 4:
                    new_ord-=5
                if m_prob ==1:
                    if (new_ord < 97):
                        new_ord +=32
                    else:
                        new_ord -=32
                if (new_ord < 65):
                    new_ord += 32
                if (new_ord > 122):
                    new_ord -= 32
                if ((new_ord < 97) and (new_ord > 90)):
                    new_ord = random.randint(97,122)
                new_letter = chr(new_ord)
                delete = random.randint(1,100)
                repeat = random.randint(1,100)
                if (delete == 1):
                    new_letter = ''
                if (repeat == 1):
                    new_letter += new_letter
                c += new_letter
        else:
            for g in genetics:
                g_num = ord(g)
                new_ord = g_num
                m_prob = random.randint(1,10)
                if m_prob == 1:
                    new_ord += 1
                if m_prob == 2:
                    new_prd -= 1
                if m_prob == 10:
                    runoff = random.randint(1,10)
                if runoff <= 3:
                    new_ord += (runoff + 1)
                if runoff >= 8:
                    new_ord -= ((10 - runoff) + 1)
                if (new_ord < 65):
                    new_ord += 32
                if (new_ord > 122):
                    new_ord -= 32
                if ((new_ord < 97) and (new_ord > 90)):
                    new_ord = random.randint(97,122)
                new_letter = chr(new_ord)
                delete = random.randint(1,100)
                repeat = random.randint(1,100)
                if (delete == 1):
                    new_letter = ''
                if (repeat == 1):
                    new_letter += new_letter
                c += new_letter
        return c

    def print_details(self):
        print('Genome: %s' % self.genotype)

    def get_geno(self):
        return self.genotype

#if __name__ == "__main__":
    # execute only if run as a script
 #   main()


