'''
Wrapper to aid in managing the different players and all the variables that go along with them
Could defs use some refactoring, but fuck it, it works.
'''
class _HungryWrapper:
    def __init__(self,agent,food,agentId):
        self.agent = agent
        self.agentId = agentId
        self.name = self.formatName() + ' ' + str(agentId)
        self.currentFood = food
        self.currentRep = 0.0
        self.repList = []
        self.currentDecisions = []
        self.allDecisions = []
        self.currentFoodEarnings = []
        self.hCount = 0.0
        self.sCount = 0.0
        
    def calculateCurrentRep(self):
        self.currentRep = self.hCount / (self.hCount + self.sCount)
        
    def updateCurrentFood(self,action):
        if action == 'h':
            self.currentFood -= 6
        else: self.currentFood -= 2
        
    def formatName(self):
        splitName = str(self.agent).split()[0].split('.')[1]        
        return str(splitName)