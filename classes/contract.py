class Contract():
    def __init__(self,id,factionSymbol,type,terms,accepted,fulfilled,expiration,deadlineToAccept):
        self.id              = id
        self.factionSymbol   = factionSymbol
        self.type            = type
        self.terms           = terms
        self.accepted        = accepted
        self.fulfilled       = fulfilled
        self.expiration      = expiration
        self.deadlineToAccept= deadlineToAccept
    

class ProcurementContract(Contract):
    def __init__(self,id,factionSymbol,type,terms,accepted,fulfilled,expiration,deadlineToAccept):
        super().__init__(id,factionSymbol,type,terms,accepted,fulfilled,expiration,deadlineToAccept)
        self.neededMaterials = self.terms['deliver'][0]['tradeSymbol']
        self.targetDestination = self.terms['deliver'][0]['destinationSymbol']
        self.neededUnits = self.terms['deliver'][0]['unitsRequired']