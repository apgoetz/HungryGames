import skeletonAllele

class Allele(skeletonAllele.Allele):
    def get_fitness(self, round_number, current_food,
                    current_reputation, m, player_reputations):
        num_players = len(player_reputations)
        max_hunters = num_players*(num_players-1)
        return float(m) / max_hunters - 1

    def update(self, food_earnings, award, m, number_cooperators):
        pass
