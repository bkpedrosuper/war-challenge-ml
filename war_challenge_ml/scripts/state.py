from war_challenge_computer_vision.regions.regions import Region, RegionData, Continent, ContinentData
from scripts.army import Army, ArmyData, armydict
from scripts.objectives import Objective, ObjectiveData, Conquer, ConquerData

class RegionState:
    army: ArmyData
    region: RegionData
    borders: list["RegionState"]

    def __init__(
        self, name: str, region: RegionData, army=Army.NONE.value, troops=0, borders=[]
    ):
        self.name = name
        self.value = region
        self.idx = region.idx
        self.army = army
        self.troops = troops
        self.borders = borders
        self.default_weight = -99999.9
        self.ally_troops = 0.0
        self.enemy_troops = 0.0

    def get_fortification(self,troop_variation=0)->float:
        new_troops = self.troops + troop_variation
        ally_fortification = 0.0
        if self.enemy_troops > 0:
            ally_fortification = min(new_troops,3)*2.0 + max(new_troops-3,0) + 0.4*self.ally_troops
        else:
            ally_fortification = min(new_troops,3)+ max(new_troops-3,0) + 0.4*self.ally_troops
        fortification = ((ally_fortification - self.enemy_troops)/ally_fortification)
        fortification += self.default_weight*fortification
        return fortification



class WorldState:
    regionDict: dict[str, RegionState]
    continentConquerPercent: dict[str, float]

    def __init__(self) -> None:
        self.regionDict = {
            region.name: RegionState(region.name, region.value) for region in Region
        }
        self.set_borders()
        self.worldLen = self.regionDict.__len__()
        self.continentConquerPercent = {
            continent.name: 0.0 for continent in Continent
        }

    def set_borders(self):
        for regionState in self.regionDict.values():
            regionState.borders = [
                self.regionDict[border.name] for border in regionState.value.borders
            ]

    def set_continentConquerPercentual(self,army:ArmyData):
        print('comecoooo')
        for regionState in self.getRegionState():
            if regionState.army.tag == army.tag:
                print('entrooooo')
                self.continentConquerPercent[regionState.value.continent.name] +=1.0
        for continent in Continent:
            self.continentConquerPercent[continent.name] /= continent.value.qtd_regions
        

    def set_default_weights(self, weigths: list[float]):
        """Given a list of weights, set regionState default_weight based on idx"""
        for regionState in self.getRegionState():
            regionState.default_weight = weigths[regionState.idx]

    def getRegionState(self):
        return list(self.regionDict.values())

    def update(self, computer_vision_data):
        for regionState in self.getRegionState():
            for elemento in computer_vision_data:
                region = elemento[0]
                if regionState.name == region.name:
                    troops = elemento[1]
                    color = elemento[2]
                    regionState.army = armydict[color].value
                    regionState.troops = troops
    
        print("(WorldState) updated")
