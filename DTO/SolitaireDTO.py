from json import JSONEncoder


class SolitaireDTO:
    def __init__(self, currentCard, towers, baseStack):
        self.currentCard = currentCard
        self.towers = towers
        self.baseStack = baseStack


class SolitaireEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
