from desktop.desktop_component import DesktopComponent
from desktop.form_component import FormComponent, NoFormComponent, ButtonComponent
from server_model.leaderboard import Leaderboard


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
        self.leaderboardButton = ButtonComponent(anApplicationContext, "Leaderboard", self.createLeaderboardForm)
        self.removeDeviceButton = ButtonComponent(anApplicationContext, "Remove Device", self.removeDevice)
        self.exitButton = ButtonComponent(anApplicationContext, "Exit", self.applicationContext.exit)
        self.pausedButtons = [
            self.resumeButton,
            self.restartButton,
            self.leaderboardButton,
            self.removeDeviceButton,
            self.exitButton
        ]
        self.lostButtons = [
            self.resumeButton,
            self.restartButton,
            self.leaderboardButton,
            self.removeDeviceButton,
            self.exitButton
        ]
        self.gameComponent.tetrisEventNotifier.attachLostEvent(self.createLostForm)
        self.form = NoFormComponent(anApplicationContext)
        self.leaderboard = Leaderboard()
        self.hasLost = False
        self.inLeaderboard = False

    def createPausedForm(self):
        self.form.destroy()
        self.form = FormComponent(self.applicationContext, "Paused", self.pausedButtons, self.keybindMapper, self.resume)
        self.form.focus(self.resumeButton)

    def createLostForm(self):
        self.form.destroy()
        self.form = FormComponent(self.applicationContext, "Lost", self.lostButtons, self.keybindMapper, self.resume)
        self.form.focus(self.restartButton)
        self.hasLost = True

    def setLeaderboard(self, aLeaderboard):
        self.leaderboard = aLeaderboard
        if self.inLeaderboard:
            self.createLeaderboardForm()

    def createLeaderboardForm(self):
        self.leaderboardButtons = []

        for i in range(self.leaderboard.size()):
            gameResult = self.leaderboard.at(i)
            string = gameResult.user.name()[0:9]
            while len(string) < 10:
                string += " "
            string += str(gameResult.score)
            self.leaderboardButtons.append(
                ButtonComponent(self.applicationContext, string, lambda: None)
            )

        self.form.destroy()
        if len(self.leaderboardButtons) == 0:
            self.form = NoFormComponent(self.applicationContext)
        else:
            self.form = FormComponent(self.applicationContext, "Leaderboard", self.leaderboardButtons, self.keybindMapper, self.onLeaderbaordExit)
        self.inLeaderboard = True

    def onLeaderbaordExit(self):
        self.inLeaderboard = False
        if self.hasLost:
            self.createLostForm()
        else:
            self.createPausedForm()

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
