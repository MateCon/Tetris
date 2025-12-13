class InputObserver:
    def __init__(self):
        self.keyupHandlers = dict()
        self.keydownHandlers = dict()

    def notify(self, aKey, aHandlerDict):
        if aKey in aHandlerDict:
            for _, handler in aHandlerDict[aKey]:
                handler()

    def addObserver(self, aSenderObject, aKey, aHandler, aHandlerDict):
        if aKey in aHandlerDict:
            aHandlerDict[aKey].append((aSenderObject, aHandler))
        else:
            aHandlerDict[aKey] = [(aSenderObject, aHandler)]

    def keyup(self, aKey):
        self.notify(aKey, self.keyupHandlers)

    def addKeyupObserver(self, aSenderObject, aKey, aHandler):
        self.addObserver(aSenderObject, aKey, aHandler, self.keyupHandlers)

    def keydown(self, aKey):
        self.notify(aKey, self.keydownHandlers)

    def addKeydownObserver(self, aSenderObject, aKey, aHandler):
        self.addObserver(aSenderObject, aKey, aHandler, self.keydownHandlers)

    def removeFromIn(self, aSenderObject, aHandlerDict):
        for key, handlerList in aHandlerDict.items():
            newHandlerList = []
            for (anotherSenderObject, aHandler) in handlerList:
                if anotherSenderObject is not aSenderObject:
                    newHandlerList.append((anotherSenderObject, aHandler))
            aHandlerDict[key] = newHandlerList

    def removeFrom(self, aSenderObject):
        self.removeFromIn(aSenderObject, self.keyupHandlers)
        self.removeFromIn(aSenderObject, self.keydownHandlers)
