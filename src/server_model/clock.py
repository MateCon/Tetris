from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class AbstractClock(ABC):
    @abstractmethod
    def now(self) -> datetime:
        pass

    def aWeek(self):
        return timedelta(weeks=1)


class ClockStub(AbstractClock):
    def __init__(self, aYear, aMonth, aDay):
        self.time = datetime(aYear, aMonth, aDay)

    def now(self):
        return self.time

    def jumpForward(self, someTimeDelta):
        self.time += someTimeDelta
