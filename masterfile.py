import random
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

class Person:
    def __init__(self):
        self.bit_array = []
        self.basis_array = []

    def choose_basis(self):
        if random.random()<0.5:
            return 0;
        else:
            return 1;

    def get_operator(self, basis):
        if basis==0:
            A = np.array([[0, 0], [0, 1]])
        else:
            A = np.array([[0.5,-0.5],[-0.5,0.5]])
        return A

    def get_density_matrix(self, bit, basis):
        if bit==0 and basis==0:
            rho = np.array([[1,0],[0,0]])
        elif bit==1 and basis==0:
            rho = np.array([[0,0],[0,1]])
        elif bit==0 and basis==1:
            rho = np.array([[0.5,0.5],[0.5,0.5]])
        else:
            rho = np.array([[0.5,-0.5],[-0.5,0.5]])
        return rho

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


class Creator(Person):
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

class Bob(Measurer):
    def __init__(self):
        super().__init__()
    def one_step(self, rho):
        return super().measure(rho)

class Alice(Creator):
    def __init__(self):
        super().__init__()
    def one_step(self):
        return super().create_qubit()

class Eve(Measurer, Creator):
    def __init__(self, percentage):
        Measurer.__init__(self)
        Creator.__init__(self)
        self.percentage = percentage
    def one_step(self, rho):
        if random.random()< self.percentage:
            bit, basis = Measurer.measure(rho)
            qubit = Creator.creator(bit,basis)
            print(qubit)
            return qubit

class System:
    def __init__(self, eavesdropper=False, percentageOfEavesdropping=0.3):
        self.b = Bob()
        self.a = Alice()
        self.name_list = ["Alice"]
        self.object_list = [self.a]
        self.eavesdropper = eavesdropper
        if eavesdropper:
            self.e = Eve(percentageOfEavesdropping)
            self.name_list.append("Eve")
            self.object_list.append(self.e)
        self.name_list.append("Bob")
        self.object_list.append(self.b)
        self.currentStep = 0
        self.initializeTkinter()

        self.postprocessing()
    def initializeTkinter(self):
        self.window = tk.Tk()
        for name in self.name_list:
            frame = tk.Frame(
                master=self.window,
                relief=tk.RAISED,
                borderwidth=1
            )
            frame.grid(row=self.name_list.index(name)*3, column=1)
            label = tk.Label(master=frame, text=name)
            label.pack()
        self.btn_1 = tk.Button(master=self.window,
                    text="Simulate one cycle",
                    width=25,
                    height=5,
                    bg="grey",
                    fg="black",
                    command = self.simulate_one_cycle
                    )
        self.btn_1.grid(row=0,column=0)
        self.btn_2 = tk.Button(master=self.window,
                    text="Simulate multiple cycles",
                    width=25,
                    height=5,
                    command = self.simulate_multiple_cycle
                    )
        self.btn_2.grid(row=1,column=0)
        label = tk.Label(text="Number of cycles")
        label.grid(row=2,column=0)
        self.entry = tk.Entry()
        self.entry.grid(row=3,column=0)


        self.window.mainloop()
        self.mainprocess()


    def simulate_one_cycle(self):
        qubit = self.a.one_step()
        #print(qubit)
        if self.eavesdropper:
            qubit = self.e.one_step(qubit)
        result = self.b.one_step(qubit)
        #print(result)
        self.displaying(self.currentStep)
        self.currentStep += 1

    def simulate_multiple_cycle(self):
        number = int(self.entry.get())
        self.entry.delete(0,tk.END)
        for i in range(number):
            self.simulate_one_cycle()

    def displaying(self, number):
        for n in self.object_list:
            frame = tk.Frame(master=self.window)
            frame.grid(row=self.object_list.index(n)*3, column=2+number)
            label = tk.Label(master=frame, text=str(n.bit_array[number]))
            label.pack()
            label2 = tk.Label(master=frame, text=str(n.basis_array[number]))
            label2.pack()
            name = str(n.bit_array[number])+str(n.basis_array[number])+".png"
            load = Image.open(name)
            render = ImageTk.PhotoImage(load)
            img = tk.Label(master=frame, image=render)
            img.image = render
            img.pack()



    def postprocessing(self):
        self.compare_basis()
        print("bits", self.a.bit_array)
        print("basis",self.a.basis_array)
        print("bits", self.b.bit_array)
        print("basis",self.b.basis_array)
    def compare_basis(self):
        if True:
            pass

test_system = System()