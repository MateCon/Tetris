from abc import ABC, abstractmethod


class EventNotifier(ABC):
    def __init__(self):
        self.observers = set()

    def attach(self, anObserver):
        if anObserver in self.observers:
            raise RepeatedObserver
        self.observers.add(anObserver)

    @abstractmethod
    def notify(self, *args, **kwargs):
        pass


class EventNotifierWithNoArguments(EventNotifier):
    def notify(self):
        for observer in self.observers:
            observer()


class EventNotifierWithOneArgument(EventNotifier):
    def notify(self, anArgument):
        for observer in self.observers:
            observer(anArgument)


class RepeatedObserver(Exception):
    pass
