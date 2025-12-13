class HeldCommandRepeater:
    def __init__(self, anActionToPerform, theFirstWaitTime, otherWaitTimes):
        self.actionToPerform = anActionToPerform
        self.isActive = False
        self.timePassed = 0
        self.firstWaitTime = theFirstWaitTime
        self.otherWaitTimes = otherWaitTimes

    def start(self):
        self.actionToPerform()
        self.isActive = True
        self.timePassed = 0
        self.isFirstWait = True

    def stop(self):
        self.isActive = False

    def update(self, millisecondsSinceLastUpdate):
        self.timePassed += millisecondsSinceLastUpdate
        if self.isActive:
            if self.isFirstWait and self.timePassed >= self.firstWaitTime:
                self.actionToPerform()
                self.timePassed -= self.firstWaitTime
                self.isFirstWait = False
            if not self.isFirstWait and self.timePassed >= self.otherWaitTimes:
                self.actionToPerform()
                self.timePassed -= self.otherWaitTimes
                self.isFirstWait = False
