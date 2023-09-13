from war_challenge_computer_vision.regions.regions import Region, RegionData
from scripts.army import Army, ArmyData, armydict



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


class WorldState:
    regionDict: dict[str, RegionState]

    def __init__(self) -> None:
        self.regionDict = {
            region.name: RegionState(region.name, region.value) for region in Region
        }
        self.set_borders()

    def set_borders(self):
        for regionState in self.regionDict.values():
            regionState.borders = [
                self.regionDict[border.name] for border in regionState.value.borders
            ]

    def getRegionState(self):
        return list(self.regionDict.values())

    def update(self, computer_vision_data):
        for regionState in self.getRegionState():
            for elemento in computer_vision_data:
                # print(
                #     "el[0] ",
                #     elemento[0],
                #     "st ",
                #     regionState,
                #     "regionState name ",
                #     regionState.name,
                # )
                region = elemento[0]
                # print(
                #     "regionState name ",
                #     regionState.name,
                #     "type ",
                #     type(regionState.name),
                # )
                # print("region", region, "type", type(region))
                if regionState.name == region.name:
                    troops = elemento[1]
                    color = elemento[2]
                    regionState.army = armydict[color].value
                    regionState.troops = troops
        print("(WorldState) updated")
