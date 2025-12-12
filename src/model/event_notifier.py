class EventNotifier:
    def __init__(self):
        self.observers = set()

    def attach(self, anObserver):
        if anObserver in self.observers:
            raise RepeatedObserver
        self.observers.add(anObserver)

    def notify(self):
        for observer in self.observers:
            observer()


class RepeatedObserver(Exception):
    pass
