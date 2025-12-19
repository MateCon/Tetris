from abc import ABC, abstractmethod
import sys


class JoystickObserver:
    def __init__(self, aJoystick, anApplicationContext):
        self.joystick = aJoystick
        self.applicationContext = anApplicationContext
        self.deadzone = 0.5
        
        if sys.platform == "linux":
            self.observers = [
                self.createAxisObserver(0, self.isLeftOfDeadzone, "JOYSTICK_LEFT_STICK_LEFT"),
                self.createAxisObserver(0, self.isRightOfDeadzone, "JOYSTICK_LEFT_STICK_RIGHT"),
                self.createAxisObserver(1, self.isLeftOfDeadzone, "JOYSTICK_LEFT_STICK_UP"),
                self.createAxisObserver(1, self.isRightOfDeadzone, "JOYSTICK_LEFT_STICK_DOWN"),
                self.createAxisObserver(3, self.isLeftOfDeadzone, "JOYSTICK_RIGHT_STICK_LEFT"),
                self.createAxisObserver(3, self.isRightOfDeadzone, "JOYSTICK_RIGHT_STICK_RIGHT"),
                self.createAxisObserver(4, self.isLeftOfDeadzone, "JOYSTICK_RIGHT_STICK_UP"),
                self.createAxisObserver(4, self.isRightOfDeadzone, "JOYSTICK_RIGHT_STICK_DOWN"),
                self.createHatObserver(lambda x, _: x == -1, "JOYSTICK_HAT_LEFT"),
                self.createHatObserver(lambda x, _: x == 1, "JOYSTICK_HAT_RIGHT"),
                self.createHatObserver(lambda _, y: y == -1, "JOYSTICK_HAT_DOWN"),
                self.createHatObserver(lambda _, y: y == 1, "JOYSTICK_HAT_UP"),
                self.createButtonObserver(0, "JOYSTICK_CROSS"),
                self.createButtonObserver(1, "JOYSTICK_CIRCLE"),
                self.createButtonObserver(2, "JOYSTICK_TRIANGLE"),
                self.createButtonObserver(3, "JOYSTICK_SQUARE"),
                self.createButtonObserver(4, "JOYSTICK_LEFT_BUMPER"),
                self.createButtonObserver(5, "JOYSTICK_RIGHT_BUMPER"),
                self.createButtonObserver(6, "JOYSTICK_LEFT_TRIGGER"),
                self.createButtonObserver(7, "JOYSTICK_RIGHT_TRIGGER"),
                self.createButtonObserver(8, "JOYSTICK_SHARE"),
                self.createButtonObserver(9, "JOYSTICK_PAUSE"),
                self.createButtonObserver(10, "JOYSTICK_HOME"),
                self.createButtonObserver(11, "JOYSTICK_LEFT_STICK_PRESSED"),
                self.createButtonObserver(12, "JOYSTICK_RIGHT_STICK_PRESSED"),
            ]
        elif sys.platform == "win32":
            self.observers = [
                self.createAxisObserver(0, self.isLeftOfDeadzone, "JOYSTICK_LEFT_STICK_LEFT"),
                self.createAxisObserver(0, self.isRightOfDeadzone, "JOYSTICK_LEFT_STICK_RIGHT"),
                self.createAxisObserver(1, self.isLeftOfDeadzone, "JOYSTICK_LEFT_STICK_UP"),
                self.createAxisObserver(1, self.isRightOfDeadzone, "JOYSTICK_LEFT_STICK_DOWN"),
                self.createAxisObserver(2, self.isLeftOfDeadzone, "JOYSTICK_RIGHT_STICK_LEFT"),
                self.createAxisObserver(2, self.isRightOfDeadzone, "JOYSTICK_RIGHT_STICK_RIGHT"),
                self.createAxisObserver(3, self.isLeftOfDeadzone, "JOYSTICK_RIGHT_STICK_UP"),
                self.createAxisObserver(3, self.isRightOfDeadzone, "JOYSTICK_RIGHT_STICK_DOWN"),
                self.createButtonObserver(0, "JOYSTICK_CROSS"),
                self.createButtonObserver(1, "JOYSTICK_CIRCLE"),
                self.createButtonObserver(2, "JOYSTICK_SQUARE"),
                self.createButtonObserver(3, "JOYSTICK_TRIANGLE"),
                self.createButtonObserver(4, "JOYSTICK_SHARE"),
                self.createButtonObserver(5, "JOYSTICK_HOME"),
                self.createButtonObserver(6, "JOYSTICK_PAUSE"),
                self.createButtonObserver(7, "JOYSTICK_LEFT_STICK_PRESSED"),
                self.createButtonObserver(8, "JOYSTICK_RIGHT_STICK_PRESSED"),
                self.createButtonObserver(9, "JOYSTICK_LEFT_BUMPER"),
                self.createButtonObserver(10, "JOYSTICK_RIGHT_BUMPER"),
                self.createButtonObserver(11, "JOYSTICK_HAT_UP"),
                self.createButtonObserver(12, "JOYSTICK_HAT_DOWN"),
                self.createButtonObserver(13, "JOYSTICK_HAT_LEFT"),
                self.createButtonObserver(14, "JOYSTICK_HAT_RIGHT"),
                self.createButtonObserver(15, "JOYSTICK_TOUCHPAD"),
            ]
        elif sys.platform == "darwin":
            self.observers = [
                self.createAxisObserver(0, self.isLeftOfDeadzone, "JOYSTICK_LEFT_STICK_LEFT"),
                self.createAxisObserver(0, self.isRightOfDeadzone, "JOYSTICK_LEFT_STICK_RIGHT"),
                self.createAxisObserver(1, self.isLeftOfDeadzone, "JOYSTICK_LEFT_STICK_UP"),
                self.createAxisObserver(1, self.isRightOfDeadzone, "JOYSTICK_LEFT_STICK_DOWN"),
                self.createAxisObserver(3, self.isLeftOfDeadzone, "JOYSTICK_RIGHT_STICK_LEFT"),
                self.createAxisObserver(3, self.isRightOfDeadzone, "JOYSTICK_RIGHT_STICK_RIGHT"),
                self.createAxisObserver(4, self.isLeftOfDeadzone, "JOYSTICK_RIGHT_STICK_UP"),
                self.createAxisObserver(4, self.isRightOfDeadzone, "JOYSTICK_RIGHT_STICK_DOWN"),
                self.createHatObserver(lambda x, _: x == -1, "JOYSTICK_HAT_LEFT"),
                self.createHatObserver(lambda x, _: x == 1, "JOYSTICK_HAT_RIGHT"),
                self.createHatObserver(lambda _, y: y == -1, "JOYSTICK_HAT_DOWN"),
                self.createHatObserver(lambda _, y: y == 1, "JOYSTICK_HAT_UP"),
                self.createButtonObserver(0, "JOYSTICK_CROSS"),
                self.createButtonObserver(1, "JOYSTICK_CIRCLE"),
                self.createButtonObserver(2, "JOYSTICK_SQUARE"),
                self.createButtonObserver(3, "JOYSTICK_TRIANGLE"),
                self.createButtonObserver(4, "JOYSTICK_LEFT_BUMPER"),
                self.createButtonObserver(5, "JOYSTICK_RIGHT_BUMPER"),
                self.createButtonObserver(6, "JOYSTICK_LEFT_TRIGGER"),
                self.createButtonObserver(7, "JOYSTICK_RIGHT_TRIGGER"),
                self.createButtonObserver(8, "JOYSTICK_SHARE"),
                self.createButtonObserver(9, "JOYSTICK_HOME"),
                self.createButtonObserver(10, "JOYSTICK_PAUSE"),
            ]


    def createAxisObserver(self, anAxis, aPressedCondition, aMessage):
        return JoystickAxisObserver(self.joystick, self.applicationContext, self.deadzone, anAxis, aPressedCondition, aMessage)

    def createHatObserver(self, aPressedCondition, aMessage):
        return JoystickHatObserver(self.joystick, self.applicationContext, aPressedCondition, aMessage)

    def createButtonObserver(self, aButtonNumber, aMessage):
        return JoystickButtonObserver(self.joystick, self.applicationContext, aButtonNumber, aMessage)

    def isLeftOfDeadzone(self, anAxisValue):
        return anAxisValue < -self.deadzone

    def isRightOfDeadzone(self, anAxisValue):
        return anAxisValue > self.deadzone

    def update(self):
        for observer in self.observers:
            observer.update()


class JoystickInputObserver(ABC):
    def __init__(self, aJoystick, anApplicationContext, aMessage):
        self.joystick = aJoystick
        self.id = self.joystick.get_instance_id()
        self.applicationContext = anApplicationContext
        self.isPressed = False
        self.message = aMessage

    @abstractmethod
    def update(self):
        pass

    def updateWith(self, isCurrentlyPressed):
        if isCurrentlyPressed and not self.isPressed:
            self.applicationContext.inputObserver.keydown(self.message, self.id)
            self.isPressed = True
        if not isCurrentlyPressed and self.isPressed:
            self.applicationContext.inputObserver.keyup(self.message, self.id)
            self.isPressed = False


class JoystickAxisObserver(JoystickInputObserver):
    def __init__(self, aJoystick, anApplicationContext, aDeadzone, anAxis, aPressedCondition, aMessage):
        super().__init__(aJoystick, anApplicationContext, aMessage)
        self.deadzone = aDeadzone
        self.axis = anAxis
        self.pressedCondition = aPressedCondition

    def update(self):
        axisValue = self.joystick.get_axis(self.axis)
        super().updateWith(self.pressedCondition(axisValue))


class JoystickHatObserver(JoystickInputObserver):
    def __init__(self, aJoystick, anApplicationContext, aPressedCondition, aMessage):
        super().__init__(aJoystick, anApplicationContext, aMessage)
        self.pressedCondition = aPressedCondition

    def update(self):
        if self.joystick.get_numhats() == 1:
            x, y = self.joystick.get_hat(0)
            super().updateWith(self.pressedCondition(x, y))


class JoystickButtonObserver(JoystickInputObserver):
    def __init__(self, aJoystick, anApplicationContext, aButtonNumber, aMessage):
        super().__init__(aJoystick, anApplicationContext, aMessage)
        self.buttonNumber = aButtonNumber

    def update(self):
        super().updateWith(self.joystick.get_button(self.buttonNumber))


class JoystickLifecycleObserver:
    def __init__(self):
        self.joystickConnectedObservers = []
        self.joystickDisconnectedObservers = []

    def onJoystickConnected(self, anObserver):
        self.joystickConnectedObservers.append(anObserver)

    def joystickConnected(self, aController):
        for observer in self.joystickConnectedObservers:
            observer(aController)

    def onJoystickDisconnected(self, anObserver):
        self.joystickDisconnectedObservers.append(anObserver)

    def joystickDisconnected(self, anInstanceId):
        for observer in self.joystickDisconnectedObservers:
            observer(anInstanceId)
