from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectFrame

class FormationUiElement():
    
    def __init__(self):
        buttonSize = (-4, 4, -.2, .8)
        buttonDistance = 0.15

        frame = DirectFrame(frameColor=(.2, .2, .2, 1), frameSize=(-.5, .5, -.7, .1), pos=(-.9, 0, -.6), scale=.5)

        self.buttonStartLand = DirectButton(text = "Start", scale=.1, frameSize=buttonSize, command=self.startLandAll)
        self.buttonStartLand.reparentTo(frame)

        self.buttonRandomTargets = DirectButton(text = "Random Target", scale=.1, frameSize=buttonSize, command=self.setRandomTargets)
        self.buttonRandomTargets.reparentTo(frame)
        self.buttonRandomTargets.setPos(Vec3(0,0,-1*buttonDistance))

        self.buttonStop = DirectButton(text = "Stop", scale=.1, frameSize=buttonSize, command=self.stopAll)
        self.buttonStop.reparentTo(frame)
        self.buttonStop.setPos(Vec3(0,0,-2*buttonDistance))

        self.buttonReturn = DirectButton(text = "Return", scale=.1, frameSize=buttonSize, command=self.returnToWaitingPosition)
        self.buttonReturn.reparentTo(frame)
        self.buttonReturn.setPos(Vec3(0,0,-3*buttonDistance))

        self.buttonToggleConnection = DirectButton(text = "Connect", scale=.1, frameSize=buttonSize, command=self.toggleConnections)
        self.buttonToggleConnection.reparentTo(frame)
        self.buttonToggleConnection.setPos(Vec3(0,0,-4*buttonDistance))