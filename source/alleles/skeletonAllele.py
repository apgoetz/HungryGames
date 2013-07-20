class Allele:
    def __init__(self, w = 1):
        self.weight = w
        
    def get_fitness(self, round_number, current_food,
                    current_reputation, m, player_reputations):
        return 1

    def update(self, food_earnings, award, m, number_cooperators):
        pass
