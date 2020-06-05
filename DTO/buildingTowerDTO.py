from json import JSONEncoder


class BuildingTowerDTO:
    def __init__(self, b, faceUp):
        self.b = b
        self.faceUp = faceUp


class BuildingTowerEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
