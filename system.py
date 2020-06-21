import bob
import alice
import eve

class System:
    def __init__(self, numberOfSteps=8, eavesdropper=False):
        self.b = bob.Bob()
        self.a = alice.Alice()
        self.eavesdropper = eavesdropper
        if eavesdropper:
            self.e = eve.Eve()
        self.numberOfSteps = numberOfSteps
        self.mainprocess()
        self.postprecessing()

    def mainprocess(self):
        for i in range(self.numberOfSteps):
            qubit = self.a.one_step()
            if eavesdropper:
                qubit = self.e.one_step(qubit)
            self.b.one_step(qubit)

    def postprocessing(self):
        pass



