import json

from Client_socket import Socket
from DTO.buildingTowerDTO import BuildingTowerDTO
from DTO.cardDTO import CardDTO, CardEncoder
from DTO.SolitaireDTO import SolitaireDTO, SolitaireEncoder

card = CardDTO('C', 3)
print(card)

tower = [card, CardDTO('D', 10)]
buildingTower = BuildingTowerDTO(True, tower)

towers = [buildingTower, buildingTower]

solitaire = SolitaireDTO(card, towers, {'C': card, 'D': CardDTO('D', 5)})
print(solitaire)

data1 = json.dumps(solitaire, cls=SolitaireEncoder)

data_socket = Socket('localhost', 8080)

data_socket.send(data1)
data_socket.receive()


