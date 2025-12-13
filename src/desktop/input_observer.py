class InputObserver:
    def __init__(self):
        self.keyupHandlers = dict()
        self.keydownHandlers = dict()

    def notify(self, aKey, aDevice, aHandlerDict):
        keyDevicePair = (aKey, aDevice)
        if keyDevicePair in aHandlerDict:
            for _, handler in aHandlerDict[keyDevicePair]:
                handler()

    def addObserver(self, aSenderObject, aKey, aDevice, aHandler, aHandlerDict):
        keyDevicePair = (aKey, aDevice)
        if keyDevicePair in aHandlerDict:
            aHandlerDict[keyDevicePair].append((aSenderObject, aHandler))
        else:
            aHandlerDict[keyDevicePair] = [(aSenderObject, aHandler)]

    def keyup(self, aKey, aDevice):
        self.notify(aKey, aDevice, self.keyupHandlers)

    def addKeyupObserver(self, aSenderObject, aKey, aDevice, aHandler):
        self.addObserver(aSenderObject, aKey, aDevice, aHandler, self.keyupHandlers)

    def keydown(self, aKey, aDevice):
        self.notify(aKey, aDevice, self.keydownHandlers)

    def addKeydownObserver(self, aSenderObject, aKey, aDevice, aHandler):
        self.addObserver(aSenderObject, aKey, aDevice,
                         aHandler, self.keydownHandlers)

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
