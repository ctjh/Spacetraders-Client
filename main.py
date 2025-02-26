import requests,time,threading, math
# from game_classes import Player, Ship, System

from classes/player import Player
from classes/system import System
from classes/ship import Ship,Drone,Frigate,Probe,Freighter, Refinery, Explorer
from classes/contract import Contract, ProcurementContract
from classes/good import Good, RawGood, FinalProduct, ShipGood

player = Player()
systemDict = {}
ships = player.listOwnedShips()
frigateObjs = []
droneObjs = []
probeObjs = []
freighterObjs = []
refineryObjs = []
explorerObjs = []
for ship in ships:
    systemSymbol = ship.get('nav')['systemSymbol']
    if systemDict.get(systemSymbol):
        system = systemDict[systemSymbol]
    else:
        systemDict[systemSymbol] = System(systemSymbol)
        system = systemDict[systemSymbol]
    frame = ship['frame']['symbol']
    if frame == "FRAME_FRIGATE":
        frigateObjs.append(Frigate(**ship,system=system,owner = player))     
    elif frame == "FRAME_DRONE":
        droneObjs.append(Drone(**ship,system = system,owner = player))
    elif frame == "FRAME_PROBE":
        probeObjs.append(Probe(**ship,system = system,owner = player))
    elif frame == "FRAME_LIGHT_FREIGHTER":
        freighterObjs.append(Freighter(**ship,system=system,owner=player))
    elif frame == "FRAME_HEAVY_FREIGHTER":
        refineryObjs.append(Refinery(**ship,system=system,owner=player))
    elif frame == 'FRAME_EXPLORER':
        explorerObjs.append(Explorer(**ship, system=system, owner = player))
    else:
        print(ship)
# further categorize them
siphonDrones = []
miningDrones = []
for drone in droneObjs:
    key_to_check = "symbol"
    if any(d[key_to_check] == "MOUNT_GAS_SIPHON_I" for d in drone.mounts if key_to_check in d):
        siphonDrones.append(drone)
    elif any(d[key_to_check] == "MOUNT_MINING_LASER_I" for d in drone.mounts if key_to_check in d):
        miningDrones.append(drone)

frigateOne = frigateObjs[0]
freighterOne = freighterObjs[0]
refineryOne = refineryObjs[0]

allGoods = ['AMMUNITION', 'CLOTHING', 'ELECTRONICS', 'EQUIPMENT', 'FABRICS', 'FERTILIZERS', 'FOOD', 'JEWELRY', 'LAB_INSTRUMENTS', 'MACHINERY', 'MEDICINE', 'MICROPROCESSORS', 'SHIP_PARTS', 'SHIP_PLATING', 'SILVER', 'ALUMINUM', 'COPPER', 'GOLD', 'IRON', 'IRON_ORE', 'PLASTICS','DRUGS', 'ASSAULT_RIFLES', 'EXPLOSIVES','FIREARMS']
allGoods2 = ['ADVANCED_CIRCUITRY','AMMUNITION', 'ASSAULT_RIFLES', 'CLOTHING', 'DRUGS', 'ELECTRONICS', 'EQUIPMENT', 'EXPLOSIVES', 'FABRICS', 'FERTILIZERS', 'FIREARMS', 'FOOD', 'LAB_INSTRUMENTS', 'MACHINERY', 'MEDICINE',  'POLYNUCLEOTIDES',  'SHIP_PARTS', 'SHIP_PLATING', 'SILVER', 'ALUMINUM', 'ALUMINUM_ORE', 'COPPER', 'COPPER_ORE','PRECIOUS_STONES','PLASTICS', 'GOLD', 'IRON', 'IRON_ORE',]
allGoods3 = ['ADVANCED_CIRCUITRY', 'AMMUNITION', 'ASSAULT_RIFLES', 'CLOTHING','DRUGS', 'ELECTRONICS', 'EQUIPMENT', 'EXPLOSIVES', 'FABRICS', 'FERTILIZERS', 'FIREARMS', 'FOOD', 'GOLD', 'IRON', 'IRON_ORE', 'JEWELRY', 'MACHINERY', 'MEDICINE', 'MICROPROCESSORS', 'PLASTICS', 'POLYNUCLEOTIDES', 'PRECIOUS_STONES', 'SHIP_PARTS', 'SHIP_PLATING', 'SILVER']

equipment = Good('EQUIPMENT',['PLASTICS','ALUMINUM'])
shipParts = Good('SHIP_PARTS',['EQUIPMENT','ELECTRONICS'])
shipPlating = Good('SHIP_PLATING', ['MACHINERY','ALUMINUM'])
electronics = Good('ELECTRONICS', ['COPPER'])
equipment = Good('EQUIPMENT', ['ALUMINUM', 'PLASTICS'])
machinery = Good('MACHINERY', ['IRON'])
microprocessors = Good('MICROPROCESSORS', ['COPPER'])
advancedCircuitry = Good('ADVANCED_CIRCUITRY', ['ELECTRONICS', 'MICROPROCESSORS'])
shipGood = ShipGood('X1-QA42-H52')
fabrics = Good('FABRICS', ['FERTILIZERS'])
clothing = FinalProduct('CLOTHING', ['FABRICS'])
fab_mats = Good('FAB_MATS',['IRON'])
advancedCircuitry = Good('ADVANCED_CIRCUITRY', ['ELECTRONICS','MICROPROCESSORS'])
biocomposites = FinalProduct('BIOCOMPOSITES', ['FABRICS', 'POLYNUCLEOTIDES'])


# goodsToProduce = [fab_mats,electronics,microprocessors, advancedCircuitry]
goodsToProduce = [fabrics, clothing]
goodsToProduce2 = [machinery, equipment,electronics, shipPlating, shipParts, shipGood]
goodsToProduce3 = [fab_mats, electronics, microprocessors, advancedCircuitry]
goodsToProduce4 = [shipGood]

threads = []

threads.append(threading.Thread(target=freighterOne.buyandsellGoods, args=(allGoods,1.2)))


print('started')
for thread in threads:
    thread.start()  
    time.sleep(0.5)

