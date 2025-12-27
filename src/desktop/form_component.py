from desktop.desktop_component import DesktopComponent
from desktop.virtual_keyboard_component import VirtualKeyboardComponent
from desktop.held_command_repeater import HeldCommandRepeater
from desktop.area import Area
from abc import abstractmethod


class AbstractFormComponent(DesktopComponent):
    @abstractmethod
    def focus(self, anInput):
        pass

    @abstractmethod
    def destroy(self):
        pass


class FormComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aTitle, aListOfInputs, aKeybindMapper, anExitFunction):
        assert len(aListOfInputs) > 0
        self.applicationContext = anApplicationContext
        self.title = aTitle
        self.inputs = aListOfInputs
        self.exitFunction = anExitFunction
        self.currentInputIndex = 0
        self.inputs[self.currentInputIndex].focus()
        self.virtualKeyboard = VirtualKeyboardComponent(anApplicationContext)
        self.leftCommandRepeater = HeldCommandRepeater(self.moveLeft, 250, 75)
        self.rightCommandRepeater = HeldCommandRepeater(self.moveRight, 250, 75)
        self.upCommandRepeater = HeldCommandRepeater(self.moveUp, 250, 75)
        self.downCommandRepeater = HeldCommandRepeater(self.moveDown, 250, 75)
        aKeybindMapper(self)

    def startMovingDown(self):
        self.downCommandRepeater.start()

    def stopMovingDown(self):
        self.downCommandRepeater.stop()

    def startMovingUp(self):
        self.upCommandRepeater.start()

    def stopMovingUp(self):
        self.upCommandRepeater.stop()

    def startMovingLeft(self):
        self.leftCommandRepeater.start()

    def stopMovingLeft(self):
        self.leftCommandRepeater.stop()

    def startMovingRight(self):
        self.rightCommandRepeater.start()

    def stopMovingRight(self):
        self.rightCommandRepeater.stop()

    def exit(self):
        if self.virtualKeyboard.isOpen():
            self.virtualKeyboard.close()
        else:
            self.destroy()
            self.exitFunction()

    def moveDown(self):
        if self.virtualKeyboard.isOpen():
            self.virtualKeyboard.moveDown()
        else:
            self.inputs[self.currentInputIndex].unfocus()
            self.currentInputIndex += 1
            self.currentInputIndex = self.currentInputIndex % len(self.inputs)
            self.inputs[self.currentInputIndex].focus()

    def moveUp(self):
        if self.virtualKeyboard.isOpen():
            self.virtualKeyboard.moveUp()
        else:
            self.inputs[self.currentInputIndex].unfocus()
            self.currentInputIndex -= 1
            self.currentInputIndex = self.currentInputIndex % len(self.inputs)
            self.inputs[self.currentInputIndex].focus()

    def moveLeft(self):
        if self.virtualKeyboard.isOpen():
            self.virtualKeyboard.moveLeft()

    def moveRight(self):
        if self.virtualKeyboard.isOpen():
            self.virtualKeyboard.moveRight()

    def accept(self):
        if self.virtualKeyboard.isOpen():
            self.virtualKeyboard.accept()
        else:
            self.inputs[self.currentInputIndex].accept(self)

    def focus(self, anInput):
        for input in self.inputs:
            input.unfocus()
        index = self.inputs.index(anInput)
        self.currentInputIndex = index
        self.inputs[self.currentInputIndex].focus()

    def openVirtualKeyboardWith(self, anInput):
        self.virtualKeyboard.openWith(anInput)

    def closeVirtualKeyboard(self):
        self.virtualKeyboard.close()

    def draw(self, anArea):
        totalArea = anArea.copy()
        totalArea.height = 50 + 30 * (len(self.inputs))
        totalAreaCentered = totalArea.shifted(0, (anArea.height - totalArea.height) / 2)
        self.backgroundColor = (0, 0, 0)
        self.borderColor = (255, 255, 255)
        self.borderWidth = 2
        self.applicationContext.drawArea((0, 0, 0), totalAreaCentered)
        self.drawBorderAround(totalAreaCentered)

        currentArea = totalAreaCentered.copy()
        currentArea.height = 40
        self.applicationContext.drawText(self.title, (255, 255, 255), 38, currentArea.shifted(20, 0))
        currentArea = currentArea.shifted(0, 50)
        currentArea.height = 30
        for input in self.inputs:
            input.draw(currentArea)
            currentArea = currentArea.shifted(0, 30)

        keyboardHeight = anArea.width // 10 * 4
        self.virtualKeyboard.draw(Area(anArea.x, anArea.y + anArea.height - keyboardHeight, anArea.width, keyboardHeight))

    def update(self, millisecondsSinceLastUpdate):
        self.leftCommandRepeater.update(millisecondsSinceLastUpdate)
        self.rightCommandRepeater.update(millisecondsSinceLastUpdate)
        self.upCommandRepeater.update(millisecondsSinceLastUpdate)
        self.downCommandRepeater.update(millisecondsSinceLastUpdate)

    def destroy(self):
        self.applicationContext.inputObserver.removeFrom(self)


class NoFormComponent(DesktopComponent):
    def focus(self, anInput):
        pass

    def draw(self, anArea):
        pass

    def update(self, millisecondsSinceLastUpdate):
        pass

    def destroy(self):
        pass


class InputComponent(DesktopComponent):
    @abstractmethod
    def focus(self):
        pass

    @abstractmethod
    def unfocus(self):
        pass

    @abstractmethod
    def accept(self, aForm):
        pass


class ButtonComponent(InputComponent):
    def __init__(self, anApplicationContext, aName, anAction):
        self.applicationContext = anApplicationContext
        self.name = aName
        self.action = anAction
        self.focused = False
        self.enabled = True
        self.failed = False

    def focus(self):
        self.focused = True

    def unfocus(self):
        self.focused = False

    def accept(self, aForm):
        if self.enabled:
            self.action()

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def fail(self):
        self.failed = True

    def draw(self, anArea):
        if self.focused:
            textColor = (0, 0, 0)
            rectColor = (255, 255, 255)
            if not self.enabled:
                rectColor = (100, 100, 100)
        else:
            textColor = (255, 255, 255)
            rectColor = (0, 0, 0)

        if self.failed:
            textColor = (255, 0, 0)

        self.applicationContext.drawArea(rectColor, anArea)
        self.applicationContext.drawText(self.name, textColor, 24, anArea.withPadding(20, 0))

    def update(self, millisecondsSinceLastUpdate):
        pass


class TextInputComponent(InputComponent):
    def __init__(self, anApplicationContext, aName):
        self.applicationContext = anApplicationContext
        self.name = aName
        self.focused = False
        self.borderWidth = 2
        self.text = ""
        self.editing = False

    def value(self):
        return self.text

    def focus(self):
        self.focused = True

    def unfocus(self):
        self.focused = False

    def accept(self, aForm):
        self.form = aForm
        self.form.openVirtualKeyboardWith(self)
        self.editing = True

    def delete(self):
        self.text = self.text[0:-1]

    def closeKeyboard(self):
        self.form.closeVirtualKeyboard()

    def stopEditing(self):
        self.editing = False

    def write(self, aString):
        self.text += aString

    def draw(self, anArea):
        if self.focused:
            textColor = (255, 255, 255)
            outerAreaColor = (255, 255, 255)
            innerAreaColor = (0, 0, 0)
        else:
            textColor = (0, 0, 0)
            outerAreaColor = (0, 0, 0)
            innerAreaColor = (255, 255, 255)

        self.applicationContext.drawArea(outerAreaColor, anArea)
        self.applicationContext.drawArea(innerAreaColor, anArea.withPadding(15, 3))

        text = self.text
        if self.text == "" and not self.editing:
            text = self.name
            textColor = (150, 150, 150)

        currentArea = anArea.withPadding(20, 0)
        for c in text:
            self.applicationContext.drawText(c, textColor, 24, currentArea)
            currentArea = currentArea.shifted(12, 0)

        if self.editing:
            cursor = currentArea.copy().shifted(0, 6)
            cursor.width = 10
            cursor.height = 18
            self.applicationContext.drawArea(textColor, cursor)

    def update(self, millisecondsSinceLastUpdate):
        pass
