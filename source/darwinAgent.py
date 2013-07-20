##Sample code from site.
# blah blah
#

import importlib
import sys
# represents a chromosome object. 
class Chromosome:
    def __init__(self, p1 = None, p2 = None):
        self.alleles = []
    
    def add_allele(self, a):
        self.alleles.append(a)

    def get_fitness(self, round_number, current_food, current_reputation, m, player_reputations):
        cross = [a.get_fitness(round_number, current_food,
                               current_reputation, m, player_reputations) * a.weight for a in
                 self.alleles]
        return 's' if reduce(lambda x, y : x+y, cross) > 0 else 'h'

    def update_alleles(self, food_earnings, award, m, number_cooperators):
        for a in self.alleles:
            a.update(food_earnings, award, m, number_cooperators)

class Player:
    # Constructor: p1 and p2 are the chromosomes of the first and second parent
    def __init__(self, p1 = None, p2 = None):
        self.xc = Chromosome(p1,p2)

    # Called when the simulator wants us to play the game
    def hunt_choices(self,round_number, current_food, current_reputation, m,
                player_reputations):
        
        hunt_decisions = list()
        for reputation in player_reputations:
            hunt_decisions.append(xc.get_fitness(round_number,
                                                 current_food,
                                                 current_reputation,
                                                 m,
                                                 player_reputations))
        return hunt_decisions
    
    # food_earnings is an array of the win loss for the last round
    def hunt_outcomes(self,food_earnings):
        pass # do nothing

    # 3 params:
    # award: amount of food won due to award
    # m: the m value for the last round
    # number_cooperators: how many players chose to cooperate last round. Maximum of P(P-1)
    def round_end(self,award, m, number_cooperators):
        pass # do nothing

    def load_allele(self, module_name, weight = 1):
        obj = None
        try:
            user_module = importlib.import_module(module_name)
            if hasattr(user_module, 'Allele'):
                try:
                    obj = user_module.Allele(weight)
                except:
                    print("\nAllele did not instantiate, make sure it is a class.\n")
                    print sys.exc_info[0]
        except:
            print ("\nCould not import %s\n" % module_name)
            raise
        return obj

