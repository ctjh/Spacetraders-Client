import requests,math,time
from system import System
from contract import Contract, ProcurementContract
from good import Good, FinalProduct, RawGood,ShipGood
from dataCollection import logMineData
from discordBot import updateServer


class Ship():
    def __init__(self,**args):
        self.auth = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiQ1RKSCIsInZlcnNpb24iOiJ2Mi4yLjAiLCJyZXNldF9kYXRlIjoiMjAyNC0wOC0xMSIsImlhdCI6MTcyMzQzMTU2Nywic3ViIjoiYWdlbnQtdG9rZW4ifQ.QtXxkPdZn5ERCAo_9jJCa3BAW2Y2SYGThPXIk9Pjy0BJKO_q54FEEnTYJvpYk-qWg0oece0elWJT5fyguk7GcBfNZmjst5-6Odkkkw_nWPXRUO0uis-p9WDogygdKcmkvwB8Cj7q4vTXfFjOmE5NMMjGWxZgQZ01G2mTrPvJyBgNUcQF7N1gGqionROrqBZ0bGnvqTxtOmvuAVsroeqwsQfs9YgnHD38UeQ_Fcvi-MF0qimaqzvP64tl3ZZp-WyYcXowLiYU4TgGbP7_YXDOsrgw7o80po9Yv3LVyQPIjQ4r-E4BdTG-CX2ZSnhLrH0R5BJ-5TUJn8aI-mspw4L-_Q'
        self.headers = {
        'Authorization':f'Bearer {self.auth}'
        }        
        self.symbol = args.get('symbol')
        self.nav = args.get('nav')
        self.crew = args.get('crew')
        self.fuel = args.get('fuel')
        self.cooldown = args.get('cooldown')
        self.frame = args.get('frame')
        self.reactor = args.get('reactor')
        self.engine = args.get('engine')
        self.modules = args.get('modules')
        self.mounts = args.get('mounts')
        self.registration = args.get('registration')
        self.cargo = args.get('cargo')
        self.coords = [0,0]
        self.system = args.get('system')
        self.owner = args.get('owner')
        self.webhook = 'https://discord.com/api/webhooks/1259776324298604615/-Hyhp5rZUYUsLUvfJs34g0_ifguH1hnBAghori7hmB_ujT2FfIsjk5NSH_9RPetCPN5w'
        self.profits = 0
        self.cycleProfits = 0
        # self.sendServerInfo('Ship Started')
    def getFuel(self):
        response = requests.get(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}', headers=self.headers).json()
        if response.get('data'):
            fuel = response['data']['fuel']['current']
            return fuel
        elif response.get('error'):
            if response.get('error')['code'] == 429:
                time.sleep(1)
                self.getFuel()
            else:
                print(response)
    def getInventory(self):
        response = requests.get(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/cargo',headers=self.headers).json()
        while not response.get('data'):
            time.sleep(1)
            response = requests.get(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/cargo',headers=self.headers).json()
        inventory = response['data']['inventory']
        inventory_lst = []
        total = 0
        for item in inventory:
            inventory_lst.append([item['symbol'],item['units']])
            total += item['units']
        reply = {'total':total, 'inventory':inventory_lst}
        return reply
    def getLocation(self):
        response = requests.get(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}',headers=self.headers).json()
        if response.get('data'):
            response = response['data']['nav']['waypointSymbol']        
            return response
        else:
            time.sleep(0.5)
            return self.getLocation()
    def getNavStatus(self):
        response = requests.get(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/nav', headers=self.headers).json()
        if response.get('data'):
            return response['data']
        else:
            time.sleep(1.0)
            return self.getNavStatus()
    def getTransitTime(self):
        shipStatus = self.getNavStatus()
        if shipStatus['status'] == 'IN_TRANSIT': 
            response = self.orbit()
            msg = response['error']['message']
            time_left = msg[76:78]
            return time_left

            #{'error': {'message': 'Ship is currently in-transit from X1-RR47-G48 to X1-RR47-C38 and arrives in 63 seconds.', 'code': 4214, 'data': {'departureSymbol': 'X1-RR47-G48', 'destinationSymbol': 'X1-RR47-C38', 'arrival': '2024-07-08T12:11:25.230Z', 'departureTime': '2024-07-08T12:09:53.230Z', 'secondsToArrival': 63}}}

            # time_left = self.orbit()['error'][]
    def orbit(self):
        response = requests.post(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/orbit', headers=self.headers).json()
        if response.get('error'):
            if response['error']['code'] == 429:
                time.sleep(1)
                self.orbit()
            else:
                print('orbit error', response)
        return response
    def dock(self):
        response = requests.post(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/dock', headers=self.headers).json()
        if response.get('error'):
            if response['error']['code']== 429:
                time.sleep(1)
                self.dock()
            else:
                print('dock error', response)
    def changeFlightMode(self, mode):
        data = {'flightMode':mode}
        response = requests.patch(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/nav', headers=self.headers,json=data)
        print(response.json())
    def travel(self, destination): #destination is a waypoint Object
        self.orbit()
        data = {"waypointSymbol":destination}
        response = requests.post(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/navigate',headers=self.headers,json=data).json()  
        if response.get('error'):
            if response.get('error')['code'] == 429:
                time.sleep(1)
                self.travel(destination)
            elif response.get('error') == 4203:
                print(destination)
            elif response.get('error'):
                print('travelError',response)
    def effectiveTravel(self,start,end, fuelCapacity = None): #use djikstra to navigate from A to B 
        #start and end should be two waypoint objects
        self.refuel()
        if fuelCapacity == None:
            fuelCapacity =  self.frame['fuelCapacity']
        route = self.system.findRoute(start,end, fuelCapacity)
        nodes = route.nodes[1:]
        for node in nodes:
            self.travel(node)
            shipStatus = self.getNavStatus()
            while shipStatus['status'] == 'IN_TRANSIT':
                time.sleep(30)
                shipStatus = self.getNavStatus()
            self.refuel()
        print('destination reached')
        return True
    def refuel(self):
        self.dock()
        response = requests.post(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/refuel',headers=self.headers).json()
        if response.get('data'):
            self.profits -= response['data']['transaction']['totalPrice']
            self.cycleProfits -= response['data']['transaction']['totalPrice']
            # print(f'''Purchased {response['data']['transaction']['units']} units of {response['data']['transaction']['tradeSymbol']} for {response['data']['transaction']['totalPrice']}''')
            action = f'''Purchased {response['data']['transaction']['units']} units of {response['data']['transaction']['tradeSymbol']} for {response['data']['transaction']['totalPrice']}'''
            # print(action)
            # self.sendServerInfo(action)
        else:
            if response.get('error'):
                if response['error']['code'] == 429:
                    time.sleep(1)
                    self.refuel()
                else:
                    print(response)
    def mine(self):
        response = requests.post(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/extract',headers=self.headers).json()
        return response
    def mineWithSurvey(self):
        self.orbit()
        response = requests.post(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/survey',headers=self.headers).json()
        if response.get('data'):
            survey = response['data']['surveys'][0]
            print(f'Survey created of {survey['size']} size with {str(survey['deposits'])} desposits')
            action = f'Survey created of {survey['size']} size with {str(survey['deposits'])} desposits'
            self.sendServerInfo(action)
            time.sleep(90)
            body = survey
            response = requests.post(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/extract/survey',headers=self.headers,json=body).json()
            if response.get('data'):
                print(f'mined {response['data']['extraction']['yield']['units']} units of {response['data']['extraction']['yield']['symbol']}')
                action = f'mined {response['data']['extraction']['yield']['units']} units of {response['data']['extraction']['yield']['symbol']}'
                self.sendServerInfo(action)
        return response
    def mineFilter(self,targetMaterials): #list of names (copper ore, etc)
        response = self.mine()
        if response.get('data'):
            minedMaterial = response['data']['extraction']['yield']['symbol']
            if minedMaterial not in targetMaterials:
                self.jettisonGood(minedMaterial)
    def siphon(self):
        response = requests.post(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/siphon',headers=self.headers).json()
        if response.get('data'):
            print(f'siphoned {response['data']['siphon']['yield']['units']} units of {response['data']['siphon']['yield']['symbol']}')
            action = f'siphoned {response['data']['siphon']['yield']['units']} units of {response['data']['siphon']['yield']['symbol']}'
            # self.sendServerInfo(action)
        return response
    def purchase(self,good, qty):
        body = {'symbol':good,'units':qty}
        response = requests.post(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/purchase',headers=self.headers, json=body).json()
        if response.get('data'):
            self.profits -= response['data']['transaction']['totalPrice']
            self.cycleProfits -= response['data']['transaction']['totalPrice']
            action = f'''Purchased {response['data']['transaction']['units']} units of {response['data']['transaction']['tradeSymbol']} for {response['data']['transaction']['totalPrice']}'''    
            self.sendServerInfo(action)
            print(f'''Purchased {response['data']['transaction']['units']} units of {response['data']['transaction']['tradeSymbol']} for {response['data']['transaction']['totalPrice']}''')
        elif response.get('error'):
            if response['error']['code'] == 4604:
                new_qty = response['error']['data']['tradeVolume']
                self.purchase(good,new_qty)
                self.purchase(good,qty - new_qty)
            elif response['error']['code'] == 429:
                time.sleep(1)
                self.purchase(good,qty)
            elif response['error']['code'] == 4244:
                self.dock()
                self.purchase(good,qty)
            else:
                print('purchaseError', response)
    def sellGood(self, good):
        self.dock()
        data = {'symbol':good,"units": 1 }
        for item in self.getInventory()['inventory']:
            if item[0] == good:
                data = {'symbol':item[0],"units":item[1]}
                response = requests.post(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/sell',headers=self.headers,json=data).json()           
                if response.get('data'):
                    action = f'''sold {response['data']['transaction']['units']} units of {response['data']['transaction']['tradeSymbol']} for {response['data']['transaction']['totalPrice']}'''
                    print(action)
                    self.profits += response['data']['transaction']['totalPrice']
                    self.cycleProfits += response['data']['transaction']['totalPrice']
                    self.sendServerInfo(action)
                elif response.get('error'):
                    if response['error']['code'] == 4604:
                        new_qty = response['error']['data']['tradeVolume']
                        new_data =  {'symbol':item[0],"units":new_qty}
                        response = requests.post(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/sell',headers=self.headers,json=new_data).json()           
                        action = f'''sold {response['data']['transaction']['units']} units of {response['data']['transaction']['tradeSymbol']} for {response['data']['transaction']['totalPrice']}'''
                        print(action)
                        self.profits += response['data']['transaction']['totalPrice']
                        self.cycleProfits += response['data']['transaction']['totalPrice']
                        self.sendServerInfo(action)
                        self.sellGood(good)
                    elif response['error']['code'] == 429:
                        time.sleep(1)
                        self.sellGood(good)

    def sellAll(self):
        self.dock()
        if self.getInventory()['total'] == 0:
            return True
        else:
            inventory_dict = self.getInventory()
            inventory_items = inventory_dict['inventory']
            for item in inventory_items:    
                data = {'symbol':item[0],"units":item[1]}
                response = requests.post(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/sell',headers=self.headers,json=data).json()           
                if response.get('data'):
                    action = f'''sold {response['data']['transaction']['units']} units of {response['data']['transaction']['tradeSymbol']} for {response['data']['transaction']['totalPrice']}'''
                    print(action)
                    self.profits += response['data']['transaction']['totalPrice']
                    self.cycleProfits += response['data']['transaction']['totalPrice']
                    self.sendServerInfo(action)
                elif response.get('error'):
                    if response['error']['code'] == 4604:
                        time.sleep(1)
                        new_qty = response['error']['data']['tradeVolume']  
                        new_data =  {'symbol':item[0],"units":new_qty}
                        response = requests.post(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/sell',headers=self.headers,json=new_data).json()           
                        if response.get('data'):
                            action = f'''sold {response['data']['transaction']['units']} units of {response['data']['transaction']['tradeSymbol']} for {response['data']['transaction']['totalPrice']}'''
                            print(action)
                            self.profits += response['data']['transaction']['totalPrice']
                            self.cycleProfits += response['data']['transaction']['totalPrice']
                            self.sendServerInfo(action)
                        self.sellAll()
                    elif response['error']['code'] == 429:
                        time.sleep(1)
                        self.sellAll()
                    else:
                        print('sell Error', response)

                        # self.jettisonGood(item[0])
        
    def transferAll(self,targetShip):
        inventory = self.getInventory()
        for item in inventory['inventory']:
            time.sleep(0.5)
            data = {'tradeSymbol':item[0], "units":item[1], 'shipSymbol':targetShip.symbol}
            response = requests.post(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/transfer',headers=self.headers,json=data).json()
            if response.get('data'):
                action = f'Transferred {item[1]} units of {item[0]} to {targetShip.symbol}'
                print(action)
                # self.sendServerInfo(action)
            else:
                print(response)
    def jettisonAll(self):
        inventory = self.getInventory()['inventory']
        for item in inventory:
            data = {'symbol':item[0],"units":item[1]}
            response = requests.post(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/jettison',headers=self.headers,json=data).json()          
            print('Jettisoned all', response)
    def jettisonGood(self,good):
        inventory = self.getInventory()['inventory']
        for item in inventory:
            if item[0] == good:
                data = {'symbol':item[0],"units":item[1]}
                response = requests.post(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/jettison',headers=self.headers,json=data).json()         
                if response.get('error'):
                    print(response)                
    def negotiateContract(self):
        self.dock()
        response = requests.post(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/negotiate/contract',headers=self.headers).json()
        if response.get('data'):
            if response['data']['type'] == 'PROCUREMENT':
                return ProcurementContract(**response['data'])
        else:
            print(response)
    def sendServerInfo(self,action):
        loc = self.getLocation()
        status = self.getNavStatus()['status']
        updateServer(self.symbol,loc,status,self.profits,action,str(self.getInventory()),self.getFuel(),self.cycleProfits)
        
class Drone(Ship):
    def __init__(self,**args):
        super().__init__(**args)
    def mineLoop(self):
        while True:#mine until full capacity
            response = self.mine()
            if response.get('data'):
                logMineData(self.getLocation(), response['data']['extraction']['yield']['symbol'], response['data']['extraction']['yield']['units'])
                if response['data']['extraction']['yield']['symbol'] == "ICE_WATER":
                    self.jettisonGood("ICE_WATER")
                if response['data']['extraction']['yield']['symbol'] == "AMMONIA_ICE":
                    self.jettisonGood("AMMONIA_ICE")
            else:
                print(response)    
            time.sleep(90)  
            # result = self.mine()
    def mineFilterLoop(self, materials):
        while True:
            self.mineFilter(materials)
            time.sleep(90)
    def siphonLoop(self):
        while True:
            self.siphon()
            time.sleep(60)

class Probe(Ship):
    def __init__(self, **args):
        super().__init__(**args)

class TravellingShip(Ship):
    def __init__(self,**args):
        super().__init__(**args)   
    def fulfillContract(self,contract,system):
        results = system.findMarketplaceByExport(contract.neededMaterials)
        result = results[0]  #this result should be a Marketplace Object
        current_loc = self.getLocation()

        fulfilled = False
        while not fulfilled:
            response = requests.get(f'https://api.spacetraders.io/v2/my/ships/{self.symbol}/cargo',headers=self.headers)
            if self.cargo['capacity'] == response.json()['data']['units']:
                start = system.createWaypoint(current_loc)
                end = system.createWaypoint(contract.targetDestination)
                print('heading to contract destination')
                self.effectiveTravel(start,end)
            elif self.getLocation != result.symbol:
                start = system.createWaypoint(current_loc)
                end = system.createWaypoint(result.symbol)
                print('heading to marketplace')
                self.effectiveTravel(start,end)
            #after reaching marketplace
            if self.getNavStatus()['status'] == 'DOCKED':
                if contract.neededUnits > self.cargo['capacity']:
                    self.purchase(contract.neededMaterials,self.cargo['capacity'])        
                else:
                    self.purchase(contract.neededMaterials, contract.neededUnits)
                #after purchasing items, go to contract destination
                start = system.createWaypoint(self.getLocation())
                end = system.createWaypoint(contract.targetDestination)
                self.effectiveTravel(start,end)
                #after reaching the end destination
                body = {
                    "shipSymbol": self.symbol,
                    "tradeSymbol": contract.neededMaterials,
                    "units": self.cargo['capacity']
                    }
                response = requests.post(f'https://api.spacetraders.io/v2/my/contracts/{contract.id}/deliver',headers=self.headers,json=body).json()
                print(response, "Cargo Delivered")
                if response.get('data'):
                    if response['data']['contract']['terms']['deliver'][0]['unitsFulfilled'] == response['data']['contract']['terms']['deliver'][0]['unitsRequired'] :
                        fulfill_response = requests.post(f'https://api.spacetraders.io/v2/my/contracts/{contract.id}/fulfill', headers=self.headers)
                        if fulfill_response['data']['contract']['fulfilled'] == True:
                            fulfilled = True
                        else:
                            contract.neededUnits -= response['data']['contract']['terms']['deliver'][0]['unitsFulfilled']
                else:
                    # print(response)
                    break
    def contractLoop(self, player):
        while True:
            #1 Choose a contract to fulfill
            #2 Fulfill the terms of that contract
            #3 Negotiate a new contract
            contracts = player.getAvailableContracts()
            for contract in contracts:
                if not contract.accepted:
                    player.acceptContract(contract)
            contracts = player.getAvailableContracts()
            for contract in contracts:
                if not contract.fulfilled:
                    self.fulfillContract(contract,self.system)
            new_contract = self.negotiateContract()
            player.acceptContract(new_contract)
    def miningLoop(self,market,asteroid): #takes in two waypoint objects
        while True:
            shipStatus = self.getNavStatus()
            if shipStatus['status'] == 'IN_TRANSIT':
                time.sleep(30)
                print('in transit')
            elif shipStatus['waypointSymbol'] == asteroid.symbol:
                result = self.mineWithSurvey()
                # print(result)
                if result.get('data'):
                    print(result)
                    while result['data']['cargo']['capacity'] != result['data']['cargo']['units']:#not full inventory
                        time.sleep(90)
                        result = self.mineWithSurvey()
                        if result.get('error'):
                            time.sleep(10)     
                            print(result)                       
                    self.effectiveTravel(asteroid, market)
                else:
                    print(result)
                    time.sleep(80)
            elif shipStatus['waypointSymbol'] == market.symbol:
                self.refuel()
                self.sellAll()
                self.effectiveTravel(market, asteroid)
            else:
                start = self.system.createWaypoint(self.getLocation())
                #if at neither of those places
                self.effectiveTravel(start,market)
                self.refuel()
    def siphonLoop(self,market,gasGiant): #takes in two waypoint objects
        while True:
            shipStatus = self.getNavStatus()
            if shipStatus['status'] == 'IN_TRANSIT':
                time.sleep(30)
            elif shipStatus['waypointSymbol'] == gasGiant.symbol:
                result = self.siphon()
                if result.get('data'):
                    while result['data']['cargo']['capacity'] != result['data']['cargo']['units']:#not full inventory
                        time.sleep(80)
                        result = self.siphon()
                        if result.get('error'):
                            time.sleep(80)     
                    self.effectiveTravel(gasGiant, market)
                else:
                    print(result)
                    if result.get('error')['code'] == 4236:                    
                       self.orbit()
                    elif result.get('error')['code'] == 4228:
                        self.effectiveTravel(gasGiant,market)
            elif shipStatus['waypointSymbol'] == market.symbol:
                # if self.getFuel() < 300:
                # self.dock()
                self.refuel()
                self.sellAll()
                self.effectiveTravel(market, gasGiant)
            else:
                start = self.system.createWaypoint(self.getLocation())
                #if at neither of those places
                self.effectiveTravel(start,market)
 
    def transportMineCargo(self, asteroid, mineDrones): #asteroid is waypoint Object
        while True:
            while self.getNavStatus()['status'] == 'IN_TRANSIT':
                time.sleep(60)
            self.refuel()
            self.effectiveTravel(self.system.createWaypoint(self.getLocation()), asteroid, self.frame['fuelCapacity']/2) 
            print('target reached')
            self.orbit()
            for ship in mineDrones:
                ship.transferAll(self)
                time.sleep(1)
            for good in self.getInventory()['inventory']:
                start = self.system.createWaypoint(self.getLocation())
                end = self.system.findMarketplaceByImport(good[0])[0]
                self.effectiveTravel(start,end,self.frame['fuelCapacity']/2)
                self.sellGood(good[0])
    def buyandsellGood(self,good, multiplier = 1, start = None, end = None): #good is the name of a good
        print(f"{self.symbol} buying {good}")
        if start == None:
            start = self.system.findMarketplaceByExport(good)[0]
        if end == None:
            end = self.system.findMarketplaceByImport(good)[0]
        if self.system.compareGoodPrices(good, end, start, multiplier) == True:
            self.effectiveTravel(self.system.createWaypoint(self.getLocation()), start)
            self.purchase(good, self.cargo['capacity'])  
            self.effectiveTravel(start,end)
            self.sellAll()
        else:
            print(f'{good} not worth trading')
    def buyandsellLoop(self,good, multiplier = 1):
        while True:
            self.buyandsellGood(good, multiplier)
    def buyandsellGoods(self,goods, multiplier =1):
        while True:
            for good in goods:
                if good == 'JUMP_GATE':
                    gate = self.system.jumpGate[0]
                    
                else:
                    start = self.system.findMarketplaceByExport(good)[0]
                    end = self.system.findMarketplaceByImport(good)[0]
                    while self.system.compareGoodPrices(good, end, start, multiplier):
                        self.effectiveTravel(self.system.createWaypoint(self.getLocation()), start)
                        if self.system.compareGoodPrices(good,end,start,multiplier):
                            self.purchase(good, self.cargo['capacity'])  
                        self.effectiveTravel(start,end)
                        self.sellAll()
    def createGood(self,good): # pass a good object
        if isinstance(good,ShipGood):
            self.buyandsellGood('SHIP_PLATING')
            self.buyandsellGood('SHIP_PARTS')
            finalMarket = self.system.createWaypoint(good.destination)
        else:
            finalMarket = self.system.findMarketplaceByExport(good.name)[0]
        components = good.components
        for component in components: #these are each the name of a component to be purchased
            self.buyandsellGood(component, end=finalMarket)
        if isinstance(good, FinalProduct): #we then buy the good we "made", and sell it to its import area
            self.buyandsellGood(good.name)       
    def createGoods(self,goods):
        while True:
            for good in goods:
                self.createGood(good)
    def transportLoop(self,market,target,ships):
        while self.getNavStatus()['status'] == 'IN_TRANSIT':
            time.sleep(60)
        self.effectiveTravel(self.system.createWaypoint(self.getLocation()), market)
        self.refuel()
        self.effectiveTravel(self.system.createWaypoint(self.getLocation()), target)
        print('target reached')
        while True:
            self.orbit()
            for ship in ships:
                ship.transferAll(self)
            self.effectiveTravel(target,market)
            self.refuel()
            self.sellAll()
            self.effectiveTravel(market,target)

    #gate things
    def deliverGate(self,good,gate):
        self.dock()
        units = 0
        for item in self.getInventory()['inventory']:
            if item[0] == 'FAB_MATS' or item[0] == 'ADVANCED_CIRCUITRY':
                units = item[1]
                break
            else:
                print(item,good)
        body =  {
            "shipSymbol": self.symbol,
            "tradeSymbol": good,
            "units": units
        }      
        response = requests.post(f'https://api.spacetraders.io/v2/systems/{self.system.symbol}/waypoints/{gate.symbol}/construction/supply',headers=self.headers, json=body).json() 
        print(response)
        if response.get('data'):
            if good == 'FAB_MATS':
                action = f"Delivered {response['data']['construction']['materials'][0]['fulfilled']} out of {response['data']['construction']['materials'][0]['required']} {good}"
                self.sendServerInfo(action)
                print(action)
            elif good == 'ADVANCED_CIRCUITRY':
                action = f"Delivered {response['data']['construction']['materials'][1]['fulfilled']} out of {response['data']['construction']['materials'][1]['required']} {good}"
                self.sendServerInfo(action)
                print(action)
        return response
    def buildGate(self):
        while True:
            gate = self.system.findWaypointByType('JUMP_GATE')[0]
            fabMatsExportMarketplace = self.system.findMarketplaceByExport('FAB_MATS')[0]
            advancedCircuitryMarketplace = self.system.findMarketplaceByExport('ADVANCED_CIRCUITRY')[0]
            while self.getNavStatus()['status'] == "IN_TRANSIT":
                time.sleep(30)
            #check fab mats
            fabMarketGoods = self.system.marketplaceDetails(fabMatsExportMarketplace.symbol)['tradeGoods']
            advancedCircuitryGoods = self.system.marketplaceDetails(advancedCircuitryMarketplace.symbol)['tradeGoods']
            print('BUYING gate component')
            for good in fabMarketGoods:
                if good['symbol'] == 'FAB_MATS':
                    # if good['supply'] != 'SCARCE':
                    if good['purchasePrice'] <= 8000:
                        start = self.system.createWaypoint(self.getLocation())
                        self.effectiveTravel(start, fabMatsExportMarketplace)
                        self.purchase('FAB_MATS',self.cargo['capacity'])
                        self.effectiveTravel(fabMatsExportMarketplace, gate)
                        self.deliverGate('FAB_MATS',gate)
                        self.refuel()
            # for good in advancedCircuitryGoods:
            #     if good['symbol'] == 'ADVANCED_CIRCUITRY':
            #         if good['supply'] != 'SCARCE':
            #             start = self.system.createWaypoint(self.getLocation())
            #             self.effectiveTravel(start, advancedCircuitryMarketplace)
            #             self.purchase('ADVANCED_CIRCUITRY',self.cargo['capacity'])
            #             self.effectiveTravel(advancedCircuitryMarketplace, gate)
            #             self.deliverGate('ADVANCED_CIRCUITRY',gate)
            #             self.refuel()

class Frigate(TravellingShip):
    def __init__(self,**args):
        super().__init__(**args)   

class Freighter(TravellingShip):
    def __init__(self, **args):
        super().__init__(**args)
    
class Refinery(TravellingShip):
    def __init__(self, **args):
        super().__init__(**args)

class Explorer(TravellingShip):
    def __init__(self, **args):
        super().__init__(**args)
class Fleet(TravellingShip):
    def __init__(self, ships):
        self.ships = ships #this is a list of objects
    def __getattr__(self, name):
        def method(*args, **kwargs):
            for ship in self.ships:
                getattr(ship, name)(*args, **kwargs)
        return method
