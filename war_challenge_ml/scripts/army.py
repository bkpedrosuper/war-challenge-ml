from enum import Enum


class ArmyData():
    idx = 0
    def __init__(self) -> None:
        self.idx= ArmyData.idx
        ArmyData.idx +=1 


class Army(Enum):
    BLUE = ArmyData()
    YELLOW = ArmyData()
    RED = ArmyData()
    GRAY = ArmyData()
    WHITE = ArmyData()
    GREEN = ArmyData()
