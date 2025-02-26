class Good():
    def __init__(self,name,components):
        self.name = name #technically symbol but ehhh
        self.components = components #this is the components that make up this good 

class RawGood(Good):
    def __init__(self,name):
        super().__init__(name,components = None)

class FinalProduct(Good):
    def __init__(self,name,components):
        super().__init__(name,components)

class ShipGood(Good):
    def __init__(self,destination):
        self.destination = destination
        self.components = ['SHIP_PLATING','SHIP_PARTS']