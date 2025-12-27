from desktop.desktop_component import DesktopComponent
from desktop.form_component import FormComponent, NoFormComponent, ButtonComponent


class PauseComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aGameComponent, aCellSize, aRestartMethod, aDeleteMethod, aKeybindMapper):
        self.applicationContext = anApplicationContext
        self.gameComponent = aGameComponent
        self.cellSize = aCellSize
        self.restartMethod = aRestartMethod
        self.deleteMethod = aDeleteMethod
        self.keybindMapper = aKeybindMapper

        self.resumeButton = ButtonComponent(anApplicationContext, "Resume", self.resume)
        self.restartButton = ButtonComponent(anApplicationContext, "Restart", self.restart)
        self.removeDeviceButton = ButtonComponent(anApplicationContext, "Remove Device", self.removeDevice)
        self.exitButton = ButtonComponent(anApplicationContext, "Exit", self.applicationContext.exit)
        self.buttons = [
            self.resumeButton,
            self.restartButton,
            self.removeDeviceButton,
            self.exitButton
        ]
        self.gameComponent.tetrisEventNotifier.attachLostEvent(self.createLostForm)
        self.form = NoFormComponent(anApplicationContext)
        self.hasLost = False

    def createPausedForm(self):
        self.form = FormComponent(self.applicationContext, "Paused", self.buttons, self.keybindMapper, lambda: None)
        self.form.focus(self.resumeButton)

    def createLostForm(self):
        self.form = FormComponent(self.applicationContext, "Lost", self.buttons, self.keybindMapper, lambda: None)
        self.form.focus(self.restartButton)
        self.hasLost = True

    def resume(self):
        self.gameComponent.togglePause()
        self.form.destroy()
        self.form = NoFormComponent(self.applicationContext)

    def restart(self):
        self.gameComponent.togglePause()
        self.form.destroy()
        self.form = NoFormComponent(self.applicationContext)
        self.hasLost = False
        self.restartMethod()

    def removeDevice(self):
        self.form.destroy()
        self.deleteMethod()

    def lost(self):
        return self.hasLost

    def draw(self, anArea):
        self.form.draw(anArea)

    def update(self, millisecondsSinceLastUpdate):
        self.form.update(millisecondsSinceLastUpdate)
