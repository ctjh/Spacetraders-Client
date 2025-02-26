import json, os
def logMineData(asteroid,resource, qty):
    if os.path.exists(f'data/{asteroid}.json'):
        with open(f'data/{asteroid}.json', 'r') as file:
            data = json.load(file)
    else:
        data = {}
    if data.get(resource):
        data[resource].append(qty)
    else:
        data[resource] = [qty]
    with open(f'data/{asteroid}.json', 'w') as file:
        json.dump(data, file)    
# logMineData('SILICON_CRYSTALS',2)
# logMineData('TEST', 'QUARTZ_SAND', 2)