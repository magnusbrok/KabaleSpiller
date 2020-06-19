from json import JSONEncoder

# Author Hella Achari
class BuildingTowerDTO:
    def __init__(self, faceDownCards, faceUpCards):
        self.faceDownCards = faceDownCards
        self.faceUpCards = faceUpCards


class BuildingTowerEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
