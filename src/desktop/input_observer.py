class InputObserver:
    def __init__(self):
        self.keyupHandlers = dict()
        self.keydownHandlers = dict()

    def keydown(self, aKey):
        if aKey in self.keydownHandlers:
            for handler in self.keydownHandlers[aKey]:
                handler()

    def keyup(self, aKey):
        if aKey in self.keyupHandlers:
            for handler in self.keyupHandlers[aKey]:
                handler()

    def addKeyupObserver(self, aKey, aHandler):
        if aKey in self.keyupHandlers:
            self.keyupHandlers[aKey].append(aHandler)
        else:
            self.keyupHandlers[aKey] = [aHandler]

    def addKeydownObserver(self, aKey, aHandler):
        if aKey in self.keyupHandlers:
            self.keydownHandlers[aKey].append(aHandler)
        else:
            self.keydownHandlers[aKey] = [aHandler]
