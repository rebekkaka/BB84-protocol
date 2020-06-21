import numpy as np
import random
from person import Person

class Measurer(Person):
    def __init__(self):
        super().__init__()

    def measure(self,rho):
        basis = super().choose_basis()
        self.basis_array.append(basis)
        A = super().get_operator(basis)
        value = np.trace(np.matmul(rho, A))
        r = random.random()
        if r<value:
            result = 1
        else:
            result = 0
        self.bit_array.append(result)
        return result, basis

