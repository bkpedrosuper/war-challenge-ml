from war_challenge_computer_vision.regions.regions import (
    Region,
    Continent,
)
from scripts.army import Army
from enum import Enum


class ConquerData:
    idx = 0

    def __init__(self):
        self.idx = ConquerData.idx
        ConquerData.idx += 1


class Conquer(Enum):
    CONTINENT = ConquerData()
    CONTINENT_PLUS_ONE = ConquerData()
    TERRITORY = ConquerData()
    TERRITORY_AND_OCCUPATION = ConquerData()
    ARMY = ConquerData()


class ObjectiveData:
    idx = 0
    bridges = [
        Region.Algeria_Nigeria,
        Region.Greenland,
        Region.Mexico,
        Region.Middle_East,
        Region.Alaska,
        Region.Moscow,
        Region.Vladivostok,
        Region.India,
        Region.Sumatra,
        Region.Vietnam,
        Region.Spain_Portugal_France_Italy,
        Region.Poland_Yugoslavia,
        Region.Aral,
        Region.Egypt,
        Region.Brazil,
        Region.Colombia_Venezuela,
    ]

    def __init__(
        self,
        conquertype: Conquer,
        army: Army | None = None,
        continents: list[Continent] = [],
        regions: list[Region] = [],
        territory_count: int = 0,
        troops_per_territory: int = 1,
    ):
        self.idx = ObjectiveData.idx
        ObjectiveData.idx += 1

        self.conquertype = conquertype
        self.continents = continents
        self.regions = regions
        self.army = army
        self.territory_count = territory_count
        self.troops_per_territory = troops_per_territory


class Objective(Enum):
    CCONQUER_EU_OCEANIA = ObjectiveData(
        Conquer.CONTINENT, continents=[Continent.EU, Continent.OCEANIA]
    )
    CONQUER_ASIA_SA = ObjectiveData(
        Conquer.CONTINENT, continents=[Continent.ASIA, Continent.SA]
    )
    CONQUER_EU_SA_PLUS_ONE = ObjectiveData(
        Conquer.CONTINENT_PLUS_ONE, continents=[Continent.EU, Continent.SA]
    )
    CONQUER_18_TERRITORIES_2_TROOPS = ObjectiveData(
        Conquer.TERRITORY, territory_count=18, troops_per_territory=2
    )
    Conquer_ASIA_AFRICA = ObjectiveData(
        Conquer.CONTINENT, continents=[Continent.ASIA, Continent.AFRICA]
    )
    CONQUER_24_TERRITORIES = ObjectiveData(Conquer.TERRITORY, territory_count=24)
    CONQUER_BLUE = ObjectiveData(Conquer.ARMY, army=Army.BLUE)
    CONQUER_YELLOW = ObjectiveData(Conquer.ARMY, army=Army.YELLOW)
    CONQUER_RED = ObjectiveData(Conquer.ARMY, army=Army.RED)
    CONQUER_BLACK = ObjectiveData(Conquer.ARMY, army=Army.GRAY)
    CONQUER_PURPLE = ObjectiveData(Conquer.ARMY, army=Army.PURPLE)
    CONQUER_GREEN = ObjectiveData(Conquer.ARMY, army=Army.GREEN)


def generate_base_weights(my_objective: ObjectiveData):
    weights = [0.1 for _ in range(len(Region))]
    match my_objective.conquertype.name:
        case Conquer.CONTINENT.name:
            for region in Region:
                if region in my_objective.bridges:
                    weights[region.value.idx] += 0.2
                if region.value.continent in my_objective.continents:
                    weights[region.value.idx] += 0.7
                else:
                    for border in region.value.borders:
                        if border.value.continent in my_objective.continents:
                            weights[region.value.idx] += 0.3
                            break
        case Conquer.CONTINENT_PLUS_ONE.name:
            for region in Region:
                if region in my_objective.bridges:
                    weights[region.value.idx] += 0.2
                if region.value.continent in my_objective.continents:
                    weights[region.value.idx] += 0.8
                else:
                    for border in region.value.borders:
                        if border.value.continent in my_objective.continents:
                            weights[region.value.idx] += 0.5
                            break

        case Conquer.TERRITORY.name:
            weights = [
                0.7 if region in my_objective.bridges else 0.5 for region in Region
            ]

        case Conquer.TERRITORY_AND_OCCUPATION.name:
            weights = [
                0.7 if region in my_objective.bridges else 0.5 for region in Region
            ]

        case Conquer.ARMY.name:
            weights = [
                0.7 if region in my_objective.bridges else 0.5 for region in Region
            ]

        case _:
            pass

    return weights
