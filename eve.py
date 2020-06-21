import measurer
import creator
class Eve(measurer.Measurer, creator.Creator):
    def __init__(self):
        super().__init__()
    def one_step(self, rho):
        bit, basis = super().measure()
        return super().creator(bit,basis)
