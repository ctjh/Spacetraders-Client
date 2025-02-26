import requests
from contract import Contract, ProcurementContract
class Player():
    def __init__(self):
        self.symbol = 'Ctjh'
        self.auth = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiQ1RKSCIsInZlcnNpb24iOiJ2Mi4yLjAiLCJyZXNldF9kYXRlIjoiMjAyNC0wOC0xMSIsImlhdCI6MTcyMzQzMTU2Nywic3ViIjoiYWdlbnQtdG9rZW4ifQ.QtXxkPdZn5ERCAo_9jJCa3BAW2Y2SYGThPXIk9Pjy0BJKO_q54FEEnTYJvpYk-qWg0oece0elWJT5fyguk7GcBfNZmjst5-6Odkkkw_nWPXRUO0uis-p9WDogygdKcmkvwB8Cj7q4vTXfFjOmE5NMMjGWxZgQZ01G2mTrPvJyBgNUcQF7N1gGqionROrqBZ0bGnvqTxtOmvuAVsroeqwsQfs9YgnHD38UeQ_Fcvi-MF0qimaqzvP64tl3ZZp-WyYcXowLiYU4TgGbP7_YXDOsrgw7o80po9Yv3LVyQPIjQ4r-E4BdTG-CX2ZSnhLrH0R5BJ-5TUJn8aI-mspw4L-_Q'
        self.headers = {
            'Authorization':f'Bearer {self.auth}'
        }
    def register(self):
        data = {
            'header':'Content-Type: application/json',
            'symbol':'Ctjh',
            'faction' : 'COSMIC'
        }
        response = requests.post('https://api.spacetraders.io/v2/register', json=data)
        print("JSON Response ", response.json())
    def getPlayerInfo(self):
        response = requests.get('https://api.spacetraders.io/v2/my/agent', headers=self.headers)   
        return response.json()['data']
    def getAvailableContracts(self):
        result = []
        response = requests.get('https://api.spacetraders.io/v2/my/contracts', headers=self.headers).json()['data']
        for contract in response:
            if contract['type'] == 'PROCUREMENT':
                result.append(ProcurementContract(**contract))
        return result
    def acceptContract(self,contract): #contract Object
        contractID = contract.id
        response = requests.post(f'https://api.spacetraders.io/v2/my/contracts/{contractID}/accept',headers=self.headers)
    def listOwnedShips(self):
        result = []
        page = 1
        response = requests.get(f'https://api.spacetraders.io/v2/my/ships?page={page}',headers=self.headers).json()
        total = response['meta']['total']
        pages = - (total // -10)
        for i in range(pages):
            response = requests.get(f'https://api.spacetraders.io/v2/my/ships?page={i+1}',headers=self.headers).json()['data']
            # for ship in response:
                # result.append(ship)
            result.extend(response)
        return result
    def purhchaseShip(self,shipType,waypoint):
        data = {"shipType": shipType,
        "waypointSymbol": waypoint}
        response = requests.post('https://api.spacetraders.io/v2/my/ships',headers=self.headers,json=data).json()
        if response.get('data'):
            print('ship purchased')
        else:
            print(response)
