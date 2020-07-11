import random
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk 
from people import *


class Channel:
    def __init__(self, eavesdroppingRate):
        self.eavesdroppingRate = eavesdroppingRate
        
        self.b = Bob()
        self.a = Alice()
        if self.eavesdroppingRate > 0:
            self.e = Eve(eavesdroppingRate)
            self.peopleList = [self.a, self.e, self.b]
        else:
            self.e = None
            self.peopleList = [self.a, self.b]
    
    
    def simulate_one_cycle(self, i):
        self.qubit = self.a.one_step()
        tmp, tmp1 = self.a.getInfo(i)
        if self.e!=None:
            self.qubit = self.e.one_step(self.qubit)
            tmp2, tmp3 = self.e.getInfo(i)
        result = self.b.one_step(self.qubit)
        tmp4, tmp5 = self.b.getInfo(i)
        return [[tmp, tmp1], [tmp2, tmp3], [tmp4, tmp5]]
    def compareBasis(self, number):            
        if self.a.basis_array[number]==self.b.basis_array[number]:
            for person in self.peopleList:
                person.keepBit(number)
            return True
        else:
            return False
        if number == a.getLength()-1:
            for person in self.peopleList:
                person.replaceKey()
    def compareBasisE(self, number):
        if self.e !=None:
            if self.a.basis_array[number]==self.e.basis_array[number] and self.e.bit_array[number]!=-1:
                return True
            else:
                return False
    
    def getBits(self):
        Alist = self.a.getBits()
        Blist = self.b.getBits()
        if self.e !=0:
            Elist = self.e.getBits()
            return [Alist, Elist, Blist]
        else:
            return [Alist, Blist]
        
        
        

        
        

        
        

class System:
    def __init__(self):#, percentageOfEavesdropping=1):
        
        self.currentStep = 0
        self.channel = None
        self.phase = 0
        self.indices = []
        self.frameList = []
        self.phase1Objects = []
        self.phase2Objects = []
        self.EList = []
        self.IList = []
        self.PList = []
        self.two_values = []
        self.final_key_alice = []
        self.final_key_bob = []
        self.number_of_error_steps = 0
        self.initializeTkinter()
        

    def initializeTkinter(self):
        self.window = tk.Tk()
        self.menu_frame = tk.Frame(master=self.window)
        self.menu_frame.grid(row=0, column =0)
        self.process_frame = tk.Frame(master=self.window)
        self.process_frame.grid(row=0, column =1)
        self.phase_label = tk.Label(master = self.menu_frame, text = 'Hey, welcome to this simulation of the BB84 protocol. Please select the eavesdropping rate (e.g. 0 for no eavesdropper, 0.3 for 30% eavesdropping):',
                                    width=25, height=25)
        self.phase_label.grid(row=0, column = 0)
        self.entry_frame = tk.Frame(master=self.menu_frame, width=25, height=3)
        self.entry_frame.grid(row=3, column=0)
        self.main_label = tk.Label(master= self.entry_frame, text="Enter eavesdropping rate")
        self.main_label.grid(row=0,column=0)
        self.entry = tk.Entry(master=self.entry_frame)
        self.entry.grid(row=1,column=0)
        self.empty_space = tk.Label(master = self.menu_frame, width=25,
                                        height=5)
        self.empty_space.grid(row=1, column=0)
        self.empty_space2 = tk.Label(master = self.menu_frame, width=25,
                                             height=5)
        self.empty_space2.grid(row=2, column=0)
        
        
        self.btn_3 = tk.Button(master=self.menu_frame,
                                   text="Start",
                                   width=25,
                                   height=5,
                                   command = self.go_to_next_phase
                                   )
        self.btn_3.grid(row=4, column=0)
        
        
        self.btn_4 = tk.Button(master=self.menu_frame,
                               text="Exit",
                               width=25,
                               height=5,
                               command = self.window.destroy
                               )
        self.btn_4.grid(row=5,column=0)
        

        self.window.mainloop()



    def simulate_one_cycle(self):
        plottingList = self.channel.simulate_one_cycle(self.currentStep)
        self.displaying(self.currentStep, plottingList)
        self.currentStep += 1

    def simulate_multiple_cycle(self):
        number = int(self.entry.get())
        self.entry.delete(0,tk.END)
        for i in range(number):
            self.simulate_one_cycle()
    def go_to_next_phase(self):
        if self.phase ==0:
            number = float(self.entry.get())
            self.entry.delete(0,tk.END)
            self.channel = Channel(number)
            if number >0:
                self.eavesdropper = True
                self.indexList = [0,1,4,5]
                self.eList = [2,3]
            else:
                self.indexList = [2,3]
                self.eList = []
                self.eavesdropper = False
            self.b = Bob()
            self.a = Alice()
            self.name_list = ["Alice"]
            self.object_list = [self.a]
            if self.eavesdropper:
                self.e = Eve(number)
                self.name_list.append("Eve")
                self.object_list.append(self.e)
            self.name_list.append("Bob")
            self.object_list.append(self.b)
            
            
            self.phase1_frame =tk.Frame(master=self.process_frame)
            self.phase1_frame.grid(row=0, column=0)

            label = tk.Label(self.phase1_frame, text='Alice', width = 10, height = 2)
            label.grid(row=0,column=0)
            label_b = tk.Label(self.phase1_frame, text='Bob', width = 10, height = 2)
            text = ["Bit", "Basis", "Qubit"]  
            if self.eavesdropper:
                label = tk.Label(self.phase1_frame, text='Eve', width = 10, height = 2)
                label.grid(row=3,column=0)
                label_b.grid(row=6,column=0)
                labels = text * 2
            else:
                label_b(row=3,column =0)
                labels = text
            labels = labels + text[:2]
            for i in range(len(labels)):
                if i%3==2:
                    h = 3
                else:
                    h=2
                label = tk.Label(master=self.phase1_frame, text=labels[i], width = 10, height = h)
                label.grid(row = i, column = 1)
                
            self.phase_label['text'] = "Phase 1: Transmission of qubits"
            self.empty_space.grid_forget()
            self.btn_1 = tk.Button(master=self.menu_frame,
                                   text="Simulate one cycle",
                                   width=25,
                                   height=5,
                                   bg="grey",
                                   fg="black",
                                   command = self.simulate_one_cycle
                                   )
            self.btn_1.grid(row=1,column=0)
            self.empty_space2.grid_forget()
            self.btn_2 = tk.Button(master=self.menu_frame,
                                   text="Simulate multiple cycles",
                                   width=25,
                                   height=5,
                                   command = self.simulate_multiple_cycle
                                   )
            self.btn_2.grid(row=2,column=0)
            self.main_label['text']="Number of cycles"
            
            self.empty_space3 = tk.Label(master = self.entry_frame, width=25,
                                         height=3)
            self.btn_3['text']="Go to next phase"
            self.btn_3.grid_forget()
            self.empty_space.grid(row=4,column=0)
            

        elif self.phase ==1:
            self.phase_label['text'] = 'Phase 2: Key Sifting'
            self.btn_1['text'] = 'Compare bases'
            self.btn_2.grid_remove()
            self.btn_3.grid_forget()
            self.empty_space2.grid(row=2, column=0)
            self.empty_space.grid(row=5, column =0)
            self.btn_1['command'] = self.compare_bases
            self.main_label.grid_forget()
            self.entry.grid_forget()
            self.empty_space3.grid(row=0, column=0)
            self.empty_space3.grid(row=0, column=0)
        
        elif self.phase ==2:
            self.phase_label['text'] = 'Phase 3: Error rate'
            self.btn_1['text'] = 'Compute error rate'
            self.main_label['text'] = 'Choose number of samples'
            self.btn_1['command'] = self.error_rate
            self.entry.grid(row=1,column=0)
            self.main_label.grid(row=0, column=0)
            self.empty_space3.grid_forget()
            self.btn_3.grid_forget()
            self.empty_space.grid(row=4, column =0)
        elif self.phase ==3:
            self.main_label.grid_forget()
            self.entry.grid_forget()
            self.empty_space3.grid(row=0, column=0)
            self.phase_label['text'] = 'Phase 4: Error correction'
            self.btn_1['text'] = 'One error correction step'
            self.empty_space2.grid_remove()
            self.btn_2['text'] = 'All error correction at once'
            self.btn_2.grid(row=2,column=0)
            self.btn_1['command'] = self.error_correction_one_step
            self.btn_2['command'] = self.error_correction
            self.phase4_frame = tk.Frame(master=self.process_frame)
            self.phase4_frame.grid(row=4,column=0)
            label = tk.Label(master=self.phase4_frame, text="Shared Key")
            label.grid(row=0,column=0)
            label_a = tk.Label(master=self.phase4_frame, text='Alice')
            label_a.grid(row=1,column=0)
            label_a = tk.Label(master=self.phase4_frame, text='Bob')
            label_a.grid(row=2,column=0)
        elif self.phase ==4:
            self.phase_label['text'] = 'Phase 5: Privacy amplification'
            self.btn_1['text'] = 'One privacy amplification step'
            self.btn_2['text'] = 'All privacy amplification at once'
            self.btn_1['command'] = self.privacy_amplification_one_step
            self.btn_2['command'] = self.privacy_amplification
            self.btn_3.grid_forget()
            self.empty_space.grid(row=5, column=0)
            
            self.phase5_frame = tk.Frame(master=self.process_frame)
            self.phase5_frame.grid(row=5,column=0)
            label = tk.Label(master=self.phase5_frame, text="Shared Key")
            label.grid(row=0,column=0)
            label_a = tk.Label(master=self.phase5_frame, text='Alice')
            label_a.grid(row=1,column=0)
            label_a = tk.Label(master=self.phase5_frame, text='Bob')
            label_a.grid(row=2,column=0)
            
            self.indices = list(range(len(self.final_key_alice)))
            self.two_values = []
            self.number_of_error_steps = 0
        self.phase += 1


    def displaying(self, number, plottingList):
        objects = []
        rn=0
        for i in plottingList:
            if i[0]!=-1:
                label = tk.Label(master=self.phase1_frame, text=str(i[0]), width=2, height=2)
                label.grid(row=rn, column=2+number)
                objects.append(label)
                rn+=1
                if i[1]==0:
                    basis = '+'
                else:
                    basis = 'x'
                label2 = tk.Label(master=self.phase1_frame, text=basis, width=2, height=2)
                label2.grid(row=rn, column=2+number)
                rn+=1
                objects.append(label2)
                if i!=len(plottingList)-1:
                    name = str(i[0])+str(i[1])+".png"
                    load = Image.open(name)
                    render = ImageTk.PhotoImage(load)
                    img = tk.Label(master=self.phase1_frame, image=render)
                    img.image = render
                    img.grid(row=rn, column=2+number)
                    rn+=1
            else:
                objects.append(None)
                objects.append(None)
                rn+=3
        self.phase1Objects.append(objects)       

        if self.currentStep == 0:
            self.empty_space.grid_forget()
            self.btn_3.grid(row=4, column=0)

    def compare_bases(self):
        for i in range(self.currentStep):
            if self.channel.compareBasis(i):
                for n in self.indexList:
                    self.phase1Objects[i][n]['background']='green2'
                if self.eavesdropper:
                    if self.channel.compareBasisE(i):
                        for n in self.eList:
                            self.phase1Objects[i][n]['background']='pale green'
                    
        self.phase2_frame = tk.Frame(master=self.process_frame)
        self.phase2_frame.grid(row=1,column=0)
        label = tk.Label(master=self.phase2_frame, text="Shared Key")
        label.grid(row=0,column=0)
        label_a = tk.Label(master=self.phase2_frame, text='Alice')
        label_a.grid(row=1,column=0)
        if self.eavesdropper:
            label_e = tk.Label(master=self.phase2_frame, text='Eve')
            label_e.grid(row=2, column=0)
            row_b=3
        else:
            row_b=2
        label_b = tk.Label(master=self.phase2_frame, text='Bob')
        label_b.grid(row=row_b, column=0)
        offset =1
        tmp = []
        bitArray = self.channel.getBits()
        for n in range(len(bitArray[0])):
            for i in range(len(bitArray)):
                label = tk.Label(master=self.phase2_frame, text=str(bitArray[i][n]))
                tmp.append(label)
                label.grid(row=1+i, column=offset+n)
            self.phase2Objects.append(tmp)
            tmp = []
        self.empty_space.grid_forget()
        self.btn_3.grid(row=4, column=0)
               
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
        #self.empty_space.grid_forget()
        #self.btn_3.grid(row=5, column=0)
        
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
        self.indices = list(range(len(self.indices)))
        self.go_to_next_phase()
    
    def error_correction_one_step(self):
        
        
        for item in self.two_values:
            #print('entered')
            print(item)
            for label in self.IList[item]:
                label['background']='yellow'
        print(self.indices)
        if len(self.indices)>=2:            
            self.two_values = random.sample(self.indices, 2)
            print(self.two_values)
            print(self.two_values)
            for i in self.two_values:
                for label in self.IList[i]:#self.indices.index(i)]:
                    label['background']='orange'
            value_alice = self.a.bit_array[self.two_values[0]]^self.a.bit_array[self.two_values[1]]
            value_bob = self.b.bit_array[self.two_values[0]]^self.b.bit_array[self.two_values[1]]
            print("alice", value_alice)
            print("bob", value_bob)
            if value_alice==value_bob:
                tmp = []
                v_alice = self.a.bit_array[self.two_values[0]]
                v_bob = self.b.bit_array[self.two_values[0]]
                self.final_key_alice.append(self.a.bit_array[self.two_values[0]])
                self.final_key_bob.append(self.b.bit_array[self.two_values[0]])
                label_a = tk.Label(master = self.phase4_frame, text = str(v_alice))
                label_a.grid(row=1, column=1+self.number_of_error_steps)
                label_b = tk.Label(master = self.phase4_frame, text = str(v_bob))
                label_b.grid(row=2, column=1+self.number_of_error_steps)
                tmp.append(label_a)
                tmp.append(label_b)
                self.PList.append(tmp)
                self.number_of_error_steps +=1
            else:
                pass
            tmp1 = self.two_values[0]
            tmp2 = self.two_values[1]
            self.indices.remove(self.two_values[0])
            self.indices.remove(self.two_values[1])
            self.two_values[0] = tmp1
            self.two_values[1] = tmp2
            print(self.indices)
        else:
            print("not enough values")
            self.empty_space.grid_forget()
            self.btn_3.grid(row=4, column=0)
            

            
        
        
    def error_correction(self):
        while len(self.indices)>=2:
            self.error_correction_one_step()
        for item in self.two_values:
            #print('entered')
            print(item)
            for label in self.IList[item]:
                label['background']='yellow'
        self.empty_space.grid_forget()
        self.btn_3.grid(row=4, column=0)
        
            
    def privacy_amplification_one_step(self):
        for item in self.two_values:
            #print('entered')
            print(item)
            for label in self.PList[item]:
                label['background']='yellow'
        print(self.indices)
        if len(self.indices)>=2:            
            self.two_values = random.sample(self.indices, 2)
            print(self.two_values)
            for i in self.two_values:
                for label in self.PList[i]:
                    label['background']='orange'
            value_alice = self.a.bit_array[self.two_values[0]]^self.a.bit_array[self.two_values[1]]
            value_bob = self.b.bit_array[self.two_values[0]]^self.b.bit_array[self.two_values[1]]
            self.final_key_alice.append(value_alice)
            self.final_key_bob.append(value_bob)
            label_a = tk.Label(master = self.phase5_frame, text = str(value_alice))
            label_a.grid(row=1, column=1+self.number_of_error_steps)
            label_b = tk.Label(master = self.phase5_frame, text = str(value_bob))
            label_b.grid(row=2, column=1+self.number_of_error_steps)
            self.number_of_error_steps +=1

            tmp1 = self.two_values[0]
            tmp2 = self.two_values[1]
            self.indices.remove(self.two_values[0])
            self.indices.remove(self.two_values[1])
            self.two_values[0] = tmp1
            self.two_values[1] = tmp2
            print(self.indices)
        else:
            print("not enough values")   
            self.finish_routine()
     
    def privacy_amplification(self):
        while len(self.indices)>=2:
            self.privacy_amplification_one_step() 
        for item in self.two_values:
            #print('entered')
            print(item)
            for label in self.PList[item]:
                label['background']='yellow'
        self.finish_routine()

    def finish_routine(self):
        self.btn_3['text'] = 'Restart'
        self.btn_3['command'] = self.restart
        self.empty_space.grid_forget()
        self.btn_3.grid(row=4, column=0)
        frame = tk.Frame(master = self.process_frame)
        frame.grid(row=6, column=0)
        label = tk.Label(master=frame, text='Congratulations. You have obtained a shared private key. You can try again or exit.')
        label.grid(row=0, column=0)
    def restart(self):
        self.process_frame.grid_remove()
        self.start()
    def abort(self):
        self.restart()
    def start(self):
        pass
    

test_system = System()