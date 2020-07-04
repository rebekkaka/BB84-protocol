import random
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

class Person:
    def __init__(self, name):
        self.bit_array = []
        self.basis_array = []
        self.name = name

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
    def measure(self,rho):
        basis = self.choose_basis()
        self.basis_array.append(basis)
        A = self.get_operator(basis)
        value = np.trace(np.matmul(rho, A))
        r = random.random()
        if r<value:
            result = 1
        else:
            result = 0
        self.bit_array.append(result)
        return result, basis
    def create_qubit(self, bit_=None, basis_=None):
        if bit_==None or basis_==None:
            if random.random()<0.5:
                bit = 0
            else:
                bit = 1
            self.bit_array.append(bit)
            basis = self.choose_basis()
            self.basis_array.append(basis)
        else:
            bit = bit_
            basis = basis_
        return self.get_density_matrix(bit, basis)


    
class Bob(Person):
    def __init__(self):
        super().__init__("Bob")
    def one_step(self, rho):
        return super().measure(rho)

class Alice(Person):
    def __init__(self):
        super().__init__("Alice")
    def one_step(self):
        return super().create_qubit()

class Eve(Person):
    def __init__(self, percentage):
        super().__init__("Eve")
        self.percentage = percentage
    def one_step(self, rho):
        if random.random()< self.percentage:
            #print("rho",rho)
            bit, basis = super().measure(rho)
            #print(bit,basis)
            qubit = super().create_qubit(bit,basis)
            #print(qubit)
            return qubit
        else:
            self.bit_array.append(-1)
            self.basis_array.append(-1)
            return rho

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
        self.phase = 0
        self.indices = []
        self.frameList = []
        self.ABList = []
        self.EList = []
        self.IList = []
        self.two_values = None
        self.final_key_alice = []
        self.final_key_bob = []
        self.initializeTkinter()
        

    def initializeTkinter(self):
        self.window = tk.Tk()
        self.menu_frame = tk.Frame(master=self.window)
        self.menu_frame.grid(row=0, column =0)
        self.process_frame = tk.Frame(master=self.window)
        self.process_frame.grid(row=0, column =1)
        self.phase1_frame =tk.Frame(master=self.process_frame)
        self.phase1_frame.grid(row=0, column=0)
        for name in self.name_list:
            frame = tk.Frame(
                master=self.phase1_frame,
                relief=tk.RAISED,
                borderwidth=1
            )
            frame.grid(row=self.name_list.index(name), column=0)
            label = tk.Label(master=frame, text=name)
            label.pack()
            frame2 = tk.Frame(
                master=self.phase1_frame,
                relief=tk.RAISED,
                borderwidth=1
            )
            frame2.grid(row=self.name_list.index(name), column=1)
            label = tk.Label(master=frame2, text="Bit")
            label.pack()
            label2 = tk.Label(master=frame2, text="Basis")
            label2.pack()
            label3 = tk.Label(master=frame2, text="Qubit")
            label3.pack()
            
        self.phase_label = tk.Label(master = self.menu_frame, text = "Phase 1: Transmission of qubits")
        self.phase_label.grid(row=0, column = 0)
        self.btn_1 = tk.Button(master=self.menu_frame,
                    text="Simulate one cycle",
                    width=25,
                    height=5,
                    bg="grey",
                    fg="black",
                    command = self.simulate_one_cycle
                    )
        self.btn_1.grid(row=1,column=0)
        self.btn_2 = tk.Button(master=self.menu_frame,
                    text="Simulate multiple cycles",
                    width=25,
                    height=5,
                    command = self.simulate_multiple_cycle
                    )
        self.btn_2.grid(row=2,column=0)
        self.main_label = tk.Label(master= self.menu_frame, text="Number of cycles")
        self.main_label.grid(row=3,column=0)
        self.btn_3 = tk.Button(master=self.menu_frame,
                    text="Go to next phase",
                    width=25,
                    height=5,
                    command = self.go_to_next_phase
                    )
        self.btn_3.grid(row=5,column=0)
        self.btn_4 = tk.Button(master=self.menu_frame,
                    text="Exit",
                    width=25,
                    height=5,
                    command = self.window.destroy
                    )
        self.btn_4.grid(row=6,column=0)
        self.entry = tk.Entry(master=self.menu_frame)
        self.entry.grid(row=4,column=0)


        self.window.mainloop()


    def simulate_one_cycle(self):
        self.qubit = self.a.one_step()
        #print(1,self.qubit)
        if self.eavesdropper:
            #print(2,self.qubit)
            self.qubit = self.e.one_step(self.qubit)
            #print(3,self.qubit)
        result = self.b.one_step(self.qubit)
        #print(result)
        self.displaying(self.currentStep)
        self.currentStep += 1

    def simulate_multiple_cycle(self):
        number = int(self.entry.get())
        self.entry.delete(0,tk.END)
        for i in range(number):
            self.simulate_one_cycle()
    def go_to_next_phase(self):
        self.phase += 1
        if self.phase ==1:
            self.phase_label['text'] = 'Phase 2: Key Sifting'
            self.btn_1['text'] = 'Compare bases'
            self.btn_1['command'] = self.compare_bases
        elif self.phase ==2:
            self.phase_label['text'] = 'Phase 3: Error rate'
            self.btn_1['text'] = 'Compute error rate'
            self.main_label['text'] = 'Choose number of samples'
            self.btn_1['command'] = self.error_rate
        elif self.phase ==3:
            self.phase_label['text'] = 'Phase 4: Error correction'
            self.btn_1['text'] = 'One error correction step'
            self.btn_2['text'] = 'All error correction at once'
            self.btn_1['command'] = self.error_correction_one_step
            self.btn_2['command'] = self.error_correction
        elif self.phase ==4:
            self.phase_label['text'] = 'Phase 5: Privacy amplification'
            self.btn_1['text'] = 'Compare bases'
            self.btn_1['command'] = self.compare_bases()
        elif self.phase ==5:
            self.phase_label['text'] = 'Congratulations. You have a shared private key!'
            self.btn_1['text'] = 'Compare bases'
            self.btn_1['command'] = self.compare_bases()

    def displaying(self, number):
        objects = []
        eobjects = []
        for n in self.object_list:
            if(n.bit_array[number] != -1):
                frame = tk.Frame(master=self.phase1_frame)
                self.frameList.append(frame)
                frame.grid(row=self.object_list.index(n), column=3+number)
                label = tk.Label(master=frame, text=str(n.bit_array[number]))
                
                label.pack()
                if n.basis_array[number]==0:
                    basis = '+'
                elif n.basis_array[number]==1:
                    basis = 'x'
                label2 = tk.Label(master=frame, text=basis)
                if n.name!="Eve":
                    objects.append(label)
                    objects.append(label2)
                else:
                    eobjects.append(label)
                    eobjects.append(label2)
                label2.pack()
                name = str(n.bit_array[number])+str(n.basis_array[number])+".png"
                load = Image.open(name)
                render = ImageTk.PhotoImage(load)
                img = tk.Label(master=frame, image=render)
                img.image = render
                img.pack()
        
        self.ABList.append(objects)
        self.EList.append(eobjects)

    def compare_bases(self):
        for i in range(len(self.a.basis_array)):
            if self.a.basis_array[i]==self.b.basis_array[i]:
                self.indices.append(i)
                for element in self.ABList[i]:
                    element['background']='green2'
            if self.e.basis_array[i]==self.a.basis_array[i]:
                for element in self.EList[i]:
                    element['background']='pale green'
                    
        frame = tk.Frame(master=self.process_frame)
        frame.grid(row=1,column=0)
        label = tk.Label(master=frame, text="Shared Key")
        label.grid(row=0,column=1)
        label_a = tk.Label(master=frame, text='Alice')
        label_a.grid(row=1,column=1)
        if self.eavesdropper:
            label_e = tk.Label(master=frame, text='Eve')
            label_e.grid(row=2, column=1)
            row_b=3
        else:
            row_b=2
        label_b = tk.Label(master=frame, text='Bob')
        label_b.grid(row=row_b, column=1)
        c =5
        tmp = []
        for i in range(len(self.a.basis_array)):
            if self.a.basis_array[i]==self.b.basis_array[i]:
                #frame = tk.Frame(master=self.process_frame)
                #frame.grid(row=4,column=c+2)
                label = tk.Label(master=frame, text=str(self.a.bit_array[i]))
                tmp.append(label)
                label.grid(row=1, column=c)
                if self.eavesdropper and self.e.bit_array[i]!=-1:
                    label = tk.Label(master=frame, text=str(self.e.bit_array[i]))
                    tmp.append(label)
                    label.grid(row=2, column=c)
                label = tk.Label(master=frame, text=str(self.b.bit_array[i]))
                tmp.append(label)
                label.grid(row=row_b, column=c)
                c+=1
            self.IList.append(tmp)
            tmp = []
               
    def error_rate(self):
        number = int(self.entry.get())
        print(number)
        self.subset = random.sample(self.indices, number)
        counter = 0
        for i in self.subset:
            for label in self.IList[i]:
                label['background'] = 'orange'
            if self.a.bit_array[i]!=self.b.bit_array[i]:
                counter+=1
        error=float(counter)/float(len(self.subset))
        self.phase3_frame = tk.Frame(master=self.process_frame)
        self.phase3_frame.grid(row=2, column=0)
        error_label = tk.Label(master=self.phase3_frame, text = 'The error rate is ' + str(error) + '. Do you want to abort or continue with postprocessing?' )
        error_label.grid(row=0, column=0)
        self.button_frame = tk.Frame(master=self.phase3_frame)
        self.button_frame.grid(row=1, column=0)
        button_abort = tk.Button(master=self.button_frame, text = 'Abort', command = self.abort)
        button_abort.grid(row=0, column=0)
        button_continue = tk.Button(master=self.button_frame, text = 'Continue with postprocessing', command = self.continue_postprocessing)
        button_continue.grid(row=0,column=1)
        
    def continue_postprocessing(self):
        self.button_frame.grid_forget()
        self.button_frame.destroy()
        frame = tk.Frame(master=self.process_frame)
        frame.grid(row=3,column=0)
        label = tk.Label(master=frame, text="Shared Key")
        label.grid(row=0,column=1)
        label_a = tk.Label(master=frame, text='Alice')
        label_a.grid(row=1,column=1)
        if self.eavesdropper:
            label_e = tk.Label(master=frame, text='Eve')
            label_e.grid(row=2, column=1)
            row_b=3
        else:
            row_b=2
        label_b = tk.Label(master=frame, text='Bob')
        label_b.grid(row=row_b, column=1)
        c =5
        self.IList.clear()
        tmp = []
        newlist = []
        for i in self.indices:
            if i in self.subset:
                pass
            else:
                newlist.append(i)
                #frame = tk.Frame(master=self.process_frame)
                #frame.grid(row=4,column=c+2)
                label = tk.Label(master=frame, text=str(self.a.bit_array[i]))
                tmp.append(label)
                label.grid(row=1, column=c)
                if self.eavesdropper and self.e.bit_array[i]!=-1:
                    label = tk.Label(master=frame, text=str(self.e.bit_array[i]))
                    #tmp.append(label)
                    label.grid(row=2, column=c)
                label = tk.Label(master=frame, text=str(self.b.bit_array[i]))
                tmp.append(label)
                label.grid(row=row_b, column=c)
                c+=1
                self.IList.append(tmp)
                tmp = []
        self.indices = newlist
        self.go_to_next_phase()
    
    def error_correction_one_step(self):
        if self.two_values !=None:
            for label in self.IList[self.two_values[0]]:
                label['background']='white'
            for label in self.IList[self.two_values[1]]:
                label['background']='white'
        if len(self.indices)>=2:            
            self.two_values = random.sample(self.indices, 2)
            for i in self.two_values:
                for label in self.IList[self.indices.index(i)]:
                    label['background']='orange'
            value_alice = self.a.bit_array[self.two_values[0]]^self.a.bit_array[self.two_values[1]]
            value_bob = self.b.bit_array[self.two_values[0]]^self.b.bit_array[self.two_values[1]]
            print("alice", value_alice)
            print("bob", value_bob)
            if value_alice==value_bob:
                self.final_key_alice.append(self.a.bit_array[self.two_values[0]])
                self.final_key_bob.append(self.b.bit_array[self.two_values[0]])
            else:
                pass
            self.indices = self.indices.remove(self.two_values[0])
            self.indices = self.indices.remove(self.two_values[1])
        else:
            print("not enough values")
        
            
        
        
    def error_correction(self):
        pass
                

    def postprocessing(self):
        self.compare_basis()
        print("bits", self.a.bit_array)
        print("basis",self.a.basis_array)
        print("bits", self.b.bit_array)
        print("basis",self.b.basis_array)
    def abort(self):
        pass
    

test_system = System(eavesdropper=True)