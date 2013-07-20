##Sample code from site.
class Player:
    def __init__(self):
        self.last_played = 's'
    
    def hunt_choices(self,round_number, current_food, current_reputation, m,
                player_reputations):
        
        hunt_decisions = list()
        for reputation in player_reputations:
            self.last_played = 's' if self.last_played == 'h' else 'h'
            hunt_decisions.append(self.last_played)     
        return hunt_decisions
    
    def hunt_outcomes(self,food_earnings):
        pass # do nothing
    
    def round_end(self,award, m, number_cooperators):
        pass # do nothing
