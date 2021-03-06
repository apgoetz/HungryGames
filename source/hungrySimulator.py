from _HungryWrapper import _HungryWrapper
import random
import importlib
import argparse

'''
Gotta have something to simulate a game if we want to test our shit!
'''
class HungrySimulator:
    def __init__(self,listOfAgents,defcon=0):
        self.listOfPlayers = self.prepareGame(listOfAgents)                        
        self.currentRound = 1
        self.defcon = defcon
        self.M = 0
        self.hCount = 0
        self.deadLog = []
    
    #Gives out initial food and sets up all the players.    
    def prepareGame(self,listOfPlayers):
        startingFood = 300*(len(listOfPlayers)-1)
        tempList = []
        for index, player in enumerate(listOfPlayers):
            tempList.append(_HungryWrapper(player,startingFood,index)) 
        return tempList
    
    #Plays a round.        
    def playRound(self):
        self.calculateM() 
        for player in self.listOfPlayers:
            #Give each player a list consisting of all the other players' current reputations.
            repList = self.getRepList(player.agentId)   #Since I'm not randomizing the position of the players in the list
                                                        #we could probably remove the 'id' number and simplify the code a bit.
                                                        #Just don't design a strategy that relies on knowing exactly where 
                                                        #other players are.
            
            #Remove id number from tuple and only pass the reputation.
            strippedIdRepList, idList = self.splitRepIdList(repList)            
                 
            #Each player 'hunts' and returns their decisions.
            decisions = player.agent.hunt_choices(self.currentRound,player.currentFood,
                                      player.currentRep,self.M,strippedIdRepList)
            
            #Combine decisions and id numbers back together
            player.currentDecisions = zip(decisions,idList)

        #Sort id numbers
        #Only leaving in if we decide to randomizing position of players
        #for player in self.listOfPlayers:
            #player.currentDecisions = self.sortListByAgentId(player.currentDecisions)            
            
        #Calculate the outcome of each pairing of decisions and pass info to each player.
        for player in self.listOfPlayers:
            self.calculateFoodEarnings(player)
            player.agent.hunt_outcomes(player.currentFoodEarnings)
            
        #See if enough people hunted and give out award if they did.
        if self.checkEnoughHunters():
            award = self.giveTribeFood()
        else: award = 0        
        
        #Update each player's current reputation, current food, and do clean up    
        for player in self.listOfPlayers:
            player.calculateCurrentRep() 
            player.currentFood += (sum(player.currentFoodEarnings) + award)
            player.agent.round_end(award,self.M,self.hCount)
            self.debug_message(3,player.name + ' Total Food ' + str(player.currentFood) + ' Current Rep ' + '%.2f' % player.currentRep)
        
        #BRING OUT YA DEAAAAAAAAD
        self.removeDeadPlayers()
        self.currentRound += 1
    
    #Splits a list of tuples into 2! (not pythonic)    
    def splitRepIdList(self,listToSplit):
        strippedIdRepList = []
        idList = []
        for repId in listToSplit:
                strippedIdRepList.append(repId[0])
                idList.append(repId[1])
        return strippedIdRepList, idList
    
    #Exactly what it says     
    def calculateM(self):
        self.M = random.randint(0,len(self.listOfPlayers)*(len(self.listOfPlayers)-1))
    
    #Runs each decision against each other. Double for loop style.    
    def calculateFoodEarnings(self,player):
        player.currentFoodEarnings = []
        for decision in player.currentDecisions:
            player.updateCurrentFood(decision[0])
            playerDecisions = self.listOfPlayers[decision[1]].currentDecisions
            repList, idList = self.splitRepIdList(playerDecisions)
            player.currentFoodEarnings.append(self.calculatePayout(decision[0],repList[idList.index(player.agentId)]))
    
    #From the decision matrix    
    def calculatePayout(self,decision1,decision2):
        if decision1 is 'h':
            if decision2 is 'h':
                return 0
            else: return -3
        else:
            if decision2 is 'h':
                return 1
            else: return -2   
             
    #Counts every 'h' in each player's decision list. Also updates the players hCount and sCount variables.               
    def checkEnoughHunters(self):
        self.hCount = 0
        for player in self.listOfPlayers:
            for letter in self.splitRepIdList(player.currentDecisions)[0]:
                if letter is 'h':
                    player.hCount += 1
                    self.hCount += 1
                else:
                    player.sCount += 1
        if self.hCount >= self.M:
            return True
        else: return False
    
    #Gives 'bonus' food if enough people hunt.        
    def giveTribeFood(self):
        award = 2*(len(self.listOfPlayers)-1)
        for player in self.listOfPlayers:
            player.currentFood += award
        return award 
    
    #Creates a list of reputations for each player.
    def getRepList(self,idToIgnore):
        return [(player.currentRep,player.agentId) for player in self.listOfPlayers if player.agentId != idToIgnore]
    
    #Sorts list by id number (use for index). Not needed unless we start randomizing positions
    #def sortListByAgentId(self,listToSort):
        #return sorted(listToSort, key=lambda agentId: agentId[1])
    
    #Cleans up dead players.
    def removeDeadPlayers(self):
        updateFlag = False
        for index,player in enumerate(self.listOfPlayers):
            if player.currentFood <= 0:
                self.deadLog.append((str(player.name),str(self.currentRound)))
                self.listOfPlayers.pop(index)
                updateFlag = True
                
        if updateFlag:
            self.updatePlayerIds()
    
    #Gives out new id numbers after players die.
    def updatePlayerIds(self):
        for index,player in enumerate(self.listOfPlayers):
            player.agentId = index
    # 
    def debug_message(self,debugLevel,message):
        if debugLevel <= self.defcon:
            print debugLevel, message

def makeAgents(module_name, count = 1):
    objs = list()
    try:
        user_module = importlib.import_module(module_name)
        if hasattr(user_module, 'Player'):
            try:
                for i in range(0,count):
                    objs.append(user_module.Player())
            except:
                print("\nPlayer did not instantiate, make sure it is a class. "
                      "Proceeding assuming non OO code.\n")
    except:
        print ("\nCould not import %s\n" % module_name)
        raise
    return objs

def list_to_tuple(listToTuple):
    return zip(listToTuple[0::2], listToTuple[1::2])
   
def main():    
    parser = argparse.ArgumentParser(description='Inputs for the simulator')
    parser.add_argument('agents',action='store',nargs='*', help='put agents and ')
    parser.add_argument('-d','--defcon',type=int,choices=[0,1,2,3,4],nargs='?',help='setting warning level')
    
    args = parser.parse_args()    
    #agentsList = listToTuple(args.agents)
    
    player_list = []
    for agent in list_to_tuple(args.agents):
        player_list.extend(makeAgents(agent[0],int(agent[1])))    
       
    simulator = HungrySimulator(player_list,args.defcon)

    for round in range(500):
        simulator.playRound()
        
        if not simulator.listOfPlayers or len(simulator.listOfPlayers) == 1:
            break
        
    for entry in simulator.deadLog:
        print entry[0] + ' died in round ' + entry[1]

if __name__ == "__main__":
    main()
