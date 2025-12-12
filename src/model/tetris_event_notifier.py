from model.event_notifier import EventNotifier


class TetrisEventNotifier:
    def __init__(self):
        self.rowClear = EventNotifier()
        self.doubleRowClear = EventNotifier()

    def attachRowClearEvent(self, event):
        self.rowClear.attach(event)

    def attachDoubleRowClearEvent(self, event):
        self.doubleRowClear.attach(event)

    def notifyRowClear(self):
        self.rowClear.notify()

    def notifyDoubleRowClear(self):
        self.doubleRowClear.notify()
