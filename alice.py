
import creator
class Alice(creator.Creator):
    def __init__(self):
        super().__init__()
    def one_step(self):
        return super().create_qubit()