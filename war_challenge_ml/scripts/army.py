from enum import Enum


class ArmyData():
    idx = 0
    def __init__(self) -> None:
        ArmyData.idx +=1 
        self.idx= ArmyData.idx


class Army(Enum):
    BLUE = ArmyData()
    YELLOW = ArmyData()
    RED = ArmyData()
    BLACK = ArmyData()
    WHITE = ArmyData()
    GREEN = ArmyData()
