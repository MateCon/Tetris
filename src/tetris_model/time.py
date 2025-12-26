class Time:
    def __init__(self, someMilliseconds, someSeconds, someMinutes, someHours, someDays):
        self.milliseconds = someMilliseconds
        self.seconds = self.milliseconds // 1000 + someSeconds
        self.minutes = self.seconds // 60 + someMinutes
        self.hours = self.minutes // 60 + someHours
        self.days = self.hours // 24 + someDays
        self.milliseconds %= 1000
        self.seconds %= 60
        self.minutes %= 60
        self.hours %= 24

    @staticmethod
    def fromMilliseconds(someMilliseconds):
        return Time(someMilliseconds, 0, 0, 0, 0)

    def getMilliseconds(self):
        return self.milliseconds

    def getSeconds(self):
        return self.seconds

    def getMinutes(self):
        return self.minutes

    def getHours(self):
        return self.hours

    def getDays(self):
        return self.days

    def __lt__(self, anotherTime):
        compareOrder = [
            (self.getDays(), anotherTime.getDays()),
            (self.getHours(), anotherTime.getHours()),
            (self.getMinutes(), anotherTime.getMinutes()),
            (self.getSeconds(), anotherTime.getSeconds()),
            (self.getMilliseconds(), anotherTime.getMilliseconds()),
        ]
        for (myValue, otherValue) in compareOrder:
            if myValue != otherValue:
                return myValue < otherValue
        return False

    def twoDigits(self, aValue):
        if aValue < 10:
            return "0" + str(aValue)
        return str(aValue)

    def __add__(self, anotherTime):
        return Time(
            self.getMilliseconds() + anotherTime.getMilliseconds(),
            self.getSeconds() + anotherTime.getSeconds(),
            self.getMinutes() + anotherTime.getMinutes(),
            self.getHours() + anotherTime.getHours(),
            self.getDays() + anotherTime.getDays(),
        )

    def asString(self):
        if self < Time(0, 1, 0, 0, 0):
            return "00s"

        secondsString = self.twoDigits(self.seconds)
        if self < Time(0, 0, 1, 0, 0):
            return f"{secondsString}s"

        minutesString = self.twoDigits(self.minutes)
        if self < Time(0, 0, 0, 1, 0):
            return f"{minutesString}:{secondsString}"

        hoursString = self.twoDigits(self.hours)
        if self < Time(0, 0, 0, 0, 1):
            return f"{hoursString}:{minutesString}:{secondsString}"

        return f"{self.days}:{hoursString}:{minutesString}:{secondsString}"

    def totalMilliseconds(self):
        totalMilliseconds = self.days
        totalMilliseconds = totalMilliseconds * 24 + self.hours
        totalMilliseconds = totalMilliseconds * 60 + self.minutes
        totalMilliseconds = totalMilliseconds * 60 + self.seconds
        return totalMilliseconds * 1000 + self.milliseconds
