import json

from Socket.Client_socket import Socket
from DTO.buildingTowerDTO import BuildingTowerDTO
from DTO.cardDTO import CardDTO
from DTO.SolitaireDTO import SolitaireDTO, SolitaireEncoder

card = CardDTO('C', 3)
print(card)

tower = [card, CardDTO('D', 10)]
buildingTower = BuildingTowerDTO(False, tower)

buildingTower1 = BuildingTowerDTO(False, [])

towers = [buildingTower, buildingTower1, buildingTower]

solitaire = SolitaireDTO(None, towers, [card, CardDTO('D', 5)])
print(solitaire)

data1 = json.dumps(solitaire, cls=SolitaireEncoder)

data_socket = Socket('localhost', 8080)

data_socket.send(data1)
data_socket.receive()

