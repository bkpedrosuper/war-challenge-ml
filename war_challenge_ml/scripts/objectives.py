from war_challenge_computer_vision.regions.regions import RegionData, ContinentData, Continent, Region
from army import Army,ArmyData
from enum import Enum


class ConquerData:
    idx = 0

    def __init__(self):
        self.idx = ContinentData.idx
        ConquerData.idx += 1

class Conquer(Enum):
    CONTINENT  = ConquerData()
    CONTINENT_PLUS_ONE = ConquerData()
    TERRITORY = ConquerData()
    TERRITORY_AND_OCCUPATION = ConquerData()
    ARMY = ConquerData()


class ObjectiveData():
    idx = 0

    continents:list[ContinentData]
    regions:list[RegionData]
    army: ArmyData

    def __init__(self,
                 conquertype:ConquerData,
                 continents=[],
                 regions=[],
                 army = None,
                 territory_count=0,
                 troops_per_territory=1):
        
        self.idx = RegionData.idx
        ObjectiveData.idx +=1
        
        self.conquertype = conquertype
        self.continents = continents
        self.regions = regions
        self.army = army
        self.territory_count = territory_count
        self.troops_per_territory = troops_per_territory

    def generate_base_weights(self,factors=[0.1,0.2,0.4,0.6,0.8,1.0]):
        weights = [0 for _ in range(len(Continent))]
        match self.conquertype:
            case Conquer.CONTINENT:
            #     for region in Region:
            #         if region.value.continent in self.continents:

            #             weights[Region.idx] = factors[-1]
            #         elif region.value.
                pass
 
            case Conquer.CONTINENT_PLUS_ONE:
                pass

            case Conquer.TERRITORY:
                pass

            case Conquer.ARMY:
                pass
            
            case _:
                pass


class Objective(Enum):
    Conquer_EU_OCEANIA = ObjectiveData(Conquer.CONTINENT,continents=[Continent.EU,Continent.OCEANIA])
    Conquer_ASIA_SA = ObjectiveData(Conquer.CONTINENT,continents=[Continent.ASIA,Continent.SA])
    Conquer_EU_SA_PLUS_ONE = ObjectiveData(Conquer.CONTINENT_PLUS_ONE,continents=[Continent.EU, Continent.SA])
    Conquer_18_territories_2_troops = ObjectiveData(Conquer.TERRITORY,territory_count=18,troops_per_territory=2)
    Conquer_ASIA_AFRICA = ObjectiveData(Conquer.CONTINENT,continents=[Continent.ASIA, Continent.AFRICA])
    Conquer_24_territories = ObjectiveData(Conquer.TERRITORY,territory_count=24)
    ConquerBlue = ObjectiveData(Conquer.ARMY,army=Army.BLUE)
    ConquerYellow = ObjectiveData(Conquer.ARMY,army=Army.YELLOW)
    ConquerRed = ObjectiveData(Conquer.ARMY,army=Army.RED)
    ConquerBlack = ObjectiveData(Conquer.ARMY,army=Army.BLACK)
    ConquerWhite = ObjectiveData(Conquer.ARMY,army=Army.WHITE)
    ConquerGreen = ObjectiveData(Conquer.ARMY,army=Army.GREEN)