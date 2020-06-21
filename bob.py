
import measurer
class Bob(measurer.Measurer):
    def __init__(self):
        super().__init__()
    def one_step(self, rho):
        super().measure(rho)