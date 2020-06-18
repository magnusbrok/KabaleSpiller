import json

from Socket.Client_socket import Socket
from DTO.buildingTowerDTO import BuildingTowerDTO
from DTO.cardDTO import CardDTO
from DTO.SolitaireDTO import SolitaireDTO, SolitaireEncoder


data_socket = Socket('localhost', 8080)

buildingTower1 = BuildingTowerDTO(False, [CardDTO('C', 5)])
buildingTower2 = BuildingTowerDTO(False, [CardDTO('S', 10)])
buildingTower3 = BuildingTowerDTO(False, [CardDTO('H', 6)])
buildingTower4 = BuildingTowerDTO(False, [CardDTO('S', 8)])
buildingTower5 = BuildingTowerDTO(False, [CardDTO('D', 10)])
buildingTower6 = BuildingTowerDTO(False, [CardDTO('S', 4)])
buildingTower7 = BuildingTowerDTO(False, [CardDTO('C', 11)])

towers = [buildingTower1, buildingTower2, buildingTower3, buildingTower4, buildingTower5, buildingTower6, buildingTower7]

solitaire = SolitaireDTO(CardDTO('S', 13), towers, [])

data1 = json.dumps(solitaire, cls=SolitaireEncoder)

data_socket.send(data1)
received = data_socket.receive()

run = True

while run:

    data_socket.send('S')
    received = data_socket.receive()

    if received == 'Draw card!\n\r\n':
        run = False


buildingTower1 = BuildingTowerDTO(False, [CardDTO('S', 13)])
buildingTower2 = BuildingTowerDTO(False, [CardDTO('S', 10)])
buildingTower3 = BuildingTowerDTO(False, [CardDTO('C', 5)])
buildingTower4 = BuildingTowerDTO(False, [CardDTO('S', 8)])
buildingTower5 = BuildingTowerDTO(False, [])
buildingTower6 = BuildingTowerDTO(False, [CardDTO('S', 4)])
buildingTower7 = BuildingTowerDTO(False, [CardDTO('D', 10)])

towers = [buildingTower1, buildingTower2, buildingTower3, buildingTower4, buildingTower5, buildingTower6, buildingTower7]

solitaire = SolitaireDTO(CardDTO('D', 3), towers, [])

data1 = json.dumps(solitaire, cls=SolitaireEncoder)

data_socket.send(data1)
received = data_socket.receive()