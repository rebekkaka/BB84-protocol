import numpy as np
import random
import person
class Creator(person.Person):
    def __init__(self):
        super().__init__()

    def create_qubit(self, bit_=None, basis_=None):
        if bit_==None or basis_==None:
            if random.random()<0.5:
                bit = 0
            else:
                bit = 1
            self.bit_array.append(bit)
            basis = super().choose_basis()
            self.basis_array.append(basis)
        else:
            bit = bit_
            basis = basis_
        return super().get_density_matrix(bit, basis)
