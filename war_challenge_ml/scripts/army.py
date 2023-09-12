from enum import Enum


class ArmyData():
    idx = 0
    def __init__(self,tag) -> None:
        self.idx= ArmyData.idx
        self.tag = tag
        ArmyData.idx +=1 


class Army(Enum):
    BLUE = ArmyData('lightseagreen')
    YELLOW = ArmyData('goldenrod')
    RED = ArmyData('firebrick')
    GRAY = ArmyData('darkslategray')
    PURPLE = ArmyData('darkslateblue')
    GREEN = ArmyData('olivedrab')
    NONE = ArmyData('None')


armydict = {
    'lightseagreen': Army.BLUE,
    'goldenrod':Army.YELLOW,
    'firebrick':Army.RED,
    'darkslategray':Army.GRAY,
    'darkslateblue':Army.PURPLE,
    'olivedrab':Army.GREEN
}