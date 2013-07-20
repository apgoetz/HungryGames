# Random Agent
#
# Picks solution randomly
from random import choice
class Player:
    def hunt_choices(self,round_number, current_food, current_reputation, m,
                player_reputations):    
        hunt_decisions = list()
        for reputation in player_reputations:
            hunt_decisions.append(choice('sh'))
        return hunt_decisions
    
    def hunt_outcomes(self,food_earnings):
        pass # do nothing
    
    def round_end(self,award, m, number_cooperators):
        pass # do nothing
