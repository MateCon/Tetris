from model.time import Time


class TestTime:
    def test01_TimeIsGivenAsMilliseconds(self):
        time = Time.fromMilliseconds(500)

        assert time.getMilliseconds() == 500
        assert time.getSeconds() == 0
        assert time.getMinutes() == 0
        assert time.getHours() == 0
        assert time.getDays() == 0

    def test02_MillisecondsCarryToSeconds(self):
        time = Time.fromMilliseconds(1000)

        assert time.getMilliseconds() == 0
        assert time.getSeconds() == 1

    def test03_SecondsCarryToMinutes(self):
        time = Time.fromMilliseconds(500 + 1000 * 60)

        assert time.getMilliseconds() == 500
        assert time.getSeconds() == 0
        assert time.getMinutes() == 1

    def test04_MinutesCarryToHours(self):
        time = Time.fromMilliseconds(1000 * 60 * 60)

        assert time.getMilliseconds() == 0
        assert time.getSeconds() == 0
        assert time.getMinutes() == 0
        assert time.getHours() == 1

    def test05_HoursCarryToDays(self):
        time = Time.fromMilliseconds(1000 * 60 * 60 * 24)

        assert time.getMilliseconds() == 0
        assert time.getSeconds() == 0
        assert time.getMinutes() == 0
        assert time.getHours() == 0
        assert time.getDays() == 1

    def test06_TimeStringUpToASecondsShowsCeroSeconds(self):
        time = Time(500, 0, 0, 0, 0)

        assert time.asString() == "00s"

    def test07_TimeStringUpToAMinuteOnlyShowsSeconds(self):
        time = Time(500, 22, 0, 0, 0)

        assert time.asString() == "22s"

    def test08_TimeStringSecondsAreAlwaysTwoDigits(self):
        time = Time(0, 3, 0, 0, 0)

        assert time.asString() == "03s"

    def test09_TimeStringUpToHoursShowsSecondsAndMinutes(self):
        time = Time(0, 10, 8, 0, 0)

        assert time.asString() == "08:10"

    def test10_TimeStringUpToDaysShowsSecondsMinutesAndHours(self):
        time = Time(0, 10, 8, 3, 0)

        assert time.asString() == "03:08:10"

    def test11_TimeStringFromDaysShowsEverythingButMilliseconds(self):
        time = Time(0, 10, 8, 3, 4)

        assert time.asString() == "4:03:08:10"

    def test12_TimesCanBeAdded(self):
        time1 = Time(100, 45, 30, 12, 1)
        time2 = Time(910, 15, 29, 11, 0)

        time = time1 + time2

        assert time.asString() == "2:00:00:01"
