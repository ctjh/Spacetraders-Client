import requests, math, time
from dijkstar import Graph, find_path

class System():
    def __init__(self,symbol):
        self.symbol = symbol
        self.auth = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiQ1RKSCIsInZlcnNpb24iOiJ2Mi4yLjAiLCJyZXNldF9kYXRlIjoiMjAyNC0wOC0xMSIsImlhdCI6MTcyMzQzMTU2Nywic3ViIjoiYWdlbnQtdG9rZW4ifQ.QtXxkPdZn5ERCAo_9jJCa3BAW2Y2SYGThPXIk9Pjy0BJKO_q54FEEnTYJvpYk-qWg0oece0elWJT5fyguk7GcBfNZmjst5-6Odkkkw_nWPXRUO0uis-p9WDogygdKcmkvwB8Cj7q4vTXfFjOmE5NMMjGWxZgQZ01G2mTrPvJyBgNUcQF7N1gGqionROrqBZ0bGnvqTxtOmvuAVsroeqwsQfs9YgnHD38UeQ_Fcvi-MF0qimaqzvP64tl3ZZp-WyYcXowLiYU4TgGbP7_YXDOsrgw7o80po9Yv3LVyQPIjQ4r-E4BdTG-CX2ZSnhLrH0R5BJ-5TUJn8aI-mspw4L-_Q'
        self.headers = {
            'Authorization':f'Bearer {self.auth}'
        }
        self.marketplaces = []
        self.fuelStations = []
        self.jumpGate = []
        self.waypoints = self.getSystemWaypoints()
    def findWaypointByType(self, _type):
        result = []
        for waypoint in self.waypoints:
            if waypoint.type == _type:
                result.append(waypoint)
        return result
    def findWaypointByTrait(self, trait):
        result = []
        for waypoint in self.waypoints:
            for waypointTrait in waypoint.traits:
                if waypointTrait['symbol'] == trait:
                    result.append(waypoint)
        return result
    def getSystemWaypoints(self):
        result = []
        page = 1
        response = requests.get(f'https://api.spacetraders.io/v2/systems/{self.symbol}/waypoints?limit=20&page={page}').json()
        # print(response)
        total = response['meta']['total']
        pages = - (total // -20)
        for i in range(pages):
            time.sleep(0.5)
            response = requests.get(f'https://api.spacetraders.io/v2/systems/{self.symbol}/waypoints?limit=20&page={i+1}').json()
            if response.get('data'):
                response = response.get('data')
            else:
                print(response)
            for waypoint in response:
                isMarket = False
                if waypoint['type'] == 'FUEL_STATION':
                    fuel_station = FuelStation(**waypoint)
                    result.append(fuel_station)
                    self.fuelStations.append(fuel_station)
                    continue
                elif waypoint['type'] == 'JUMP_GATE':
                    result.append(JumpGate(**waypoint))
                    self.jumpGate.append(JumpGate(**waypoint))
                traits = waypoint['traits']
                for trait in traits:
                    if trait['symbol'] == 'MARKETPLACE' and waypoint['type'] != 'FUEL_STATION':
                        isMarket = True
                        marketplace = Marketplace(**waypoint)
                        result.append(marketplace)
                        self.marketplaces.append(marketplace)
                        break
                if not isMarket:
                    result.append(Waypoint(**waypoint))
        return result
    def createWaypoint(self,waypoint):
        response = requests.get(f'https://api.spacetraders.io/v2/systems/{self.symbol}/waypoints/{waypoint}').json()
        if response.get('data'):
            waypoint = response.get('data')
            return Waypoint(**waypoint)
        elif response.get('error')['code'] == 429:
            time.sleep(0.5)
            return self.createWaypoint(waypoint)
        else:
            print(response)
    def getWaypointDetails(self,waypoint):
        response = requests.get(f'https://api.spacetraders.io/v2/systems/{self.symbol}/waypoints/{waypoint}')
        return response.json()['data']
    def marketplaceDetails(self,marketplace):
        response = requests.get(f'https://api.spacetraders.io/v2/systems/{self.symbol}/waypoints/{marketplace}/market', headers=self.headers).json()
        if response.get('data'):
            return response['data']
        else:
            time.sleep(0.5)
            return self.marketplaceDetails(marketplace)
    def findMarketplaceByImport(self, good):
        result = []
        for marketplace in self.marketplaces:
            if marketplace.imports != []:
                for _import in marketplace.imports:
                    if good == _import['symbol']:
                        result.append(marketplace)
                # for exchange in marketplace.exchange:
                #     if good == exchange['symbol']:
                        # result.append(marketplace)
        return result #return a bunch of marketplace objects
        # print(marketplace['symbol'], import_lst,exchange_lst, marketplace['x'],marketplace['y'])
    def findMarketplaceByExport(self,good):
        result = []
        for marketplace in self.marketplaces:
            if marketplace.exports != []:
                for export in marketplace.exports:
                    if good == export['symbol']:
                        result.append(marketplace)
                # for exchange in marketplace.exchange:
                #     if good == exchange['symbol']:
                        # result.append(marketplace)
        return result #return a bunch of marketplaces
    def shipyardDetails(self,shipyard):
        response = requests.get(f'https://api.spacetraders.io/v2/systems/{self.symbol}/waypoints/{shipyard}/shipyard',headers=self.headers).json()
        if response.get('data'):
            return response['data']
    def createMarketplaceGraph(self):
        graph = Graph()
        marketplaces = self.marketplaces
        #need two loops to add edges
        for node, marketplaceObj in enumerate(marketplaces):
            for node_2,comparison in enumerate(marketplaces):
                if node != node_2:
                    distance = marketplaceObj.distanceFrom(comparison)
                    if distance <= 400:
                        graph.add_edge(node, node_2)
        return graph
    def findRoute(self,start,end,fuel = 400): #these should be two waypoint Objects
        graph = Graph()
        nodes = [start]
        nodes += self.marketplaces
        nodes += self.fuelStations
        nodes.append(end)
        highest = (len(self.marketplaces) + 1 )
        for marketplaceObj in nodes:
            for comparison in nodes:
                if marketplaceObj.symbol != comparison.symbol:
                    distance = marketplaceObj.distanceFrom(comparison)
                    if distance <= fuel:
                        graph.add_edge(marketplaceObj.symbol, comparison.symbol, distance)
        path = find_path(graph,start.symbol,end.symbol)
        return path
    def jumpgateDetails(self,jumpgate):
        response = requests.get(f'https://api.spacetraders.io/v2/systems/{self.symbol}/waypoints/{jumpgate}/construction').json()
        return response['data']
    def compareGoodPrices(self,good, importMarket, exportMarket, multiplier = 1):
        importDetails = self.marketplaceDetails(importMarket.symbol)
        while importDetails == None:   
            time.sleep(0.5)             
            importDetails = self.marketplaceDetails(importMarket.symbol)
        importGoods = importDetails.get('tradeGoods')
        if not importGoods:
            return True
        # exportMarket = self.system.findMarketplaceByExport(good.name)[0]
        time.sleep(0.5)
        exportDetails = self.marketplaceDetails(exportMarket.symbol)
        while exportDetails == None:   
            time.sleep(0.5)             
            exportDetails = self.marketplaceDetails(exportMarket.symbol)
        exportGoods = exportDetails.get('tradeGoods')
        if not exportGoods:
            print('no details')
            return True
        # exportMarket = self.system.findMarketplaceByExpo
        importPrice = 0
        exportPrice = 0
        for _import in importGoods:
            if _import['symbol'] == good:
                importPrice = _import['sellPrice']
        for _export in exportGoods:
            if _export['symbol'] == good:
                exportPrice = _export['purchasePrice']
        # print(importPrice, exportPrice)
        if importPrice > exportPrice * multiplier:
            return True #import price is greater by X amount
        else:
            return False
    def getMarketplaceGoods(self):
        exportSet = set()
        importSet = set()
        for market in self.marketplaces:
            for export in market.exports:
                exportSet.add(export.get('symbol'))
            for _import in market.imports:
                importSet.add(_import.get('symbol'))
        goodsSet = exportSet & importSet
        return goodsSet
class Waypoint():
    def __init__(self, **args):
        self.systemSymbol = args.get('systemSymbol')
        self.symbol = args.get('symbol')
        self.type = args.get('type')
        self.x = args.get('x')
        self.y = args.get('y')
        self.orbitals = args.get('orbitals')
        self.traits = args.get('traits')
        self.modifiers = args.get('modifiers')
        self.chart = args.get('chart')
        self.faction = args.get('faction')
        self.isUnderConstruction = args.get('isUnderConstruction')
    def distanceFrom(self,waypoint):
        return math.sqrt((self.x - waypoint.x) ** 2 + (self.y - waypoint.y) ** 2)


class Marketplace(Waypoint):
    def __init__(self, **args):
        super().__init__(**args)
        details = requests.get(f'https://api.spacetraders.io/v2/systems/{self.systemSymbol}/waypoints/{self.symbol}/market').json()
        while not details.get('data'):
            time.sleep(0.5)
            details = requests.get(f'https://api.spacetraders.io/v2/systems/{self.systemSymbol}/waypoints/{self.symbol}/market').json()
        self.details = details['data']
        self.exports = self.details['exports']
        self.imports = self.details['imports']
        self.exchange = self.details['exchange']
        self.tradeGoods = self.details.get('tradeGoods') #should be none unless there is a ship monitoring the station

class Shipyard(Waypoint):
    def __init__(self, systemSymbol, symbol, type, x, y, orbitals, traits, modifiers, chart, faction, isUnderConstruction):
        super().__init__(systemSymbol, symbol, type, x, y, orbitals, traits, modifiers, chart, faction, isUnderConstruction)
        self.details = requests.get(f'https://api.spacetraders.io/v2/systems/{self.systemSymbol}/waypoints/{self.symbol}/shipyard').json()['data']
        self.shipTypes = self.details['shipTypes'] #list of type name pairs
        self.modificationFee = self.details['modificationsFee'] #integer cost to do modifications

class FuelStation(Waypoint):
    def __init__(self, **args):
        super().__init__(**args)

class JumpGate(Waypoint):
    def __init__(self, **args):
        super().__init__(**args)
        self.materials = [] 
        self.isComplete = None
        self.connections = None
        self.updateProgress()
        self.updateDetails()
    def updateProgress(self):
        response = requests.get(f'https://api.spacetraders.io/v2/systems/{self.systemSymbol}/waypoints/{self.symbol}/construction').json()
        if response.get('data'):
            details = response['data']
            self.materials = details['materials'] #list of dictionaries
            self.isComplete = details['isComplete']
    def getProgress(self):
        self.updateProgress()
        result = {}
        for material in self.materials:
            print(material['required'], material['fulfilled'], material['tradeSymbol'])
            result[material['tradeSymbol']] = round(material['fulfilled']/ material['required'] *100,1)
        return result
    def updateDetails(self):
        response = requests.get(f'https://api.spacetraders.io/v2/systems/{self.systemSymbol}/waypoints/{self.symbol}/jump-gate').json()
        if response.get('data'):
            self.connections = response['data']['connections']
    def getDetails(self):
        return self.connections 