from model.event_notifier import EventNotifier


class TetrisEventNotifier:
    def __init__(self):
        self.rowClear = EventNotifier()
        self.doubleRowClear = EventNotifier()
        self.tripleRowClear = EventNotifier()
        self.quadrupleRowClear = EventNotifier()
        self.placedPiece = EventNotifier()

    def attachRowClearEvent(self, event):
        self.rowClear.attach(event)

    def notifyRowClear(self):
        self.rowClear.notify()

    def attachDoubleRowClearEvent(self, event):
        self.doubleRowClear.attach(event)

    def notifyDoubleRowClear(self):
        self.doubleRowClear.notify()

    def attachTripleRowClearEvent(self, event):
        self.tripleRowClear.attach(event)

    def notifyTripleRowClear(self):
        self.tripleRowClear.notify()

    def attachQuadrupleRowClearEvent(self, event):
        self.quadrupleRowClear.attach(event)

    def notifyQuadrupleRowClear(self):
        self.quadrupleRowClear.notify()

    def attachPlacedPieceEvent(self, event):
        self.placedPiece.attach(event)

    def notifyPlacedPiece(self):
        self.placedPiece.notify()
