from scripts.objectives import Objective,ObjectiveData, Conquer, ConquerData, generate_base_weights
from scripts.army import Army,ArmyData, armydict
from war_challenge_computer_vision.regions.regions import Region,RegionData,Continent
from scripts.state import WorldState, RegionState



class Player:
    army:ArmyData
    def __init__(self,army, my_objective:ObjectiveData) -> None:
        self.worldState = WorldState()
        self.army = army
        self.my_objective = my_objective
        #self.TerCOntdi
        #generate_base_weights(my_objective.value)
    
    def divide_and_conquer(self, data):
        self.worldState.update(data[0])
        conquer = []
        flag = 0
        Generate_weights = generate_base_weights(self.my_objective)
        Weights = list(zip(Region,Generate_weights))
        
        #generate_base_weights(my_objective.value)
        for Search_Ally in self.worldState.getRegionState():

            #print(flag)
            #print(Search_Ally.army.tag,'',self.army.tag)
            if Search_Ally.army.tag == self.army.tag and Search_Ally.troops > 1: #Possivel
                #print(Search_Ally.name)
                Ally_power: float = 0.0
                for search_Ally_Ally in self.worldState.getRegionState()[flag].borders:  # noqa: E501
                    if search_Ally_Ally.army.tag == self.army:
                        #print("Entrou 3")
                        Ally_power += search_Ally_Ally.troops
                        


                for search_Enemy in self.worldState.getRegionState()[flag].borders:
                    print('####Enemy ', search_Enemy.name)
                    if search_Enemy.army.tag != self.army.tag:
                        #print("Entrou 4")
                        Enemy_power: float = 0.0
                        Weight_flag = 0
                        for Enemy in self.worldState.getRegionState()[search_Enemy.idx].borders:  # noqa: E501
                            if Enemy.army.tag == self.army.tag:
                                Weight_flag +=1
                                continue
                            Enemy_power += Enemy.troops
                            Weight_flag += 1
                            #print(Enemy_power)
                        math = (Ally_power + Search_Ally.troops)*0.5 - ((Enemy_power + search_Enemy.troops)*0.5)/Weights[Weight_flag][1]             # noqa: E501
                        conquer.append(math) # type: ignore # noqa: E501
                        print(Search_Ally.name,'ataca',search_Enemy.name, 'fit: ',math)   # noqa: E501
                        print('Enemy Power ',Enemy_power)
            flag += 1
        return conquer
#teste