from scripts.objectives import Objective,ObjectiveData, Conquer, ConquerData
from scripts.army import Army,ArmyData, armydict
from war_challenge_computer_vision.regions.regions import Region,RegionData,Continent
from scripts.state import WorldState, RegionState

class Player:
    def __init__(self,army:ArmyData) -> None:
        self.worldState = WorldState()
        self.army = army
