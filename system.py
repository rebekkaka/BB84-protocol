
import tkinter as tk
from PIL import Image, ImageTk 
from channel import *

class System:
    def __init__(self):
        #channel handles Alice, Bob, and Eve
        self.channel = None
        #information about the current state of the simulation
        self.currentStep = 0
        self.number_of_error_steps = 0
        self.phase = 0
        #storage of label objects
        self.phase1Objects = []
        self.phase2Objects = []
        self.phase3Objects = []
        self.phase4Objects = []
        #helper variable for plotting
        self.two_values = []
        #set up tkinter window
        self.initializeTkinter()
        
    def go_to_next_phase(self):
        """prepares variables and menu for the upcoming phase"""
        #transmission and measurement of qubits
        if self.phase ==0:
            number = self.getNumber("probability")
            while number==None:
                number = self.getNumber("probability")
            self.channel = Channel(number)
            self.go_to_phase1(number)
        #key sifting
        elif self.phase ==1:
            self.go_to_phase2()  
        #calculation of error rate
        elif self.phase ==2:
            self.go_to_phase3()
        #error correction
        elif self.phase ==3:
            self.go_to_phase4()
        #privacy amplification
        elif self.phase ==4:
            self.channel.preparePostprocessing()
            self.go_to_phase5()
            self.two_values = []
            self.number_of_error_steps = 0
        self.phase += 1


    def simulate_one_cycle(self):
        """Alice generates one qubit, Bob (and possibly Eve) measures it,
        result is displayed in window"""
        plottingList = self.channel.simulate_one_cycle(self.currentStep)
        self.displaying(self.currentStep, plottingList)
        self.currentStep += 1
    def simulate_multiple_cycle(self):
        """Alice generates a by the user defined number of qubits, Bob (and 
        possibly Eve) measures it, results are displayed in window"""
        number = int(self.getNumber("int"))
        while number==None:
            number = self.getNumber("int")
        for i in range(number):
            self.simulate_one_cycle()
        

    def initializeTkinter(self):
        """Tkinter setup and preparation of the start-menu"""
        self.window = tk.Tk()
        self.menu_frame = tk.Frame(master=self.window)
        self.menu_frame.grid(row=0, column =0)
        self.process_frame = tk.Frame(master=self.window)
        self.process_frame.grid(row=0, column =1)
        self.phase_label = tk.Text(master = self.menu_frame,
                                    width=25, height=10)
        self.phase_label.grid(row=0, column = 0)
        self.phase_label.insert(tk.END, 'Hey, welcome to this\nsimulation of the BB84\nprotocol.\nPlease select the\neavesdropping rate\n(e.g. 0 for no\neavesdropper, 0.3 for\n30 % eavesdropping):')
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


            
    def getNumber(self, typeArgument):
        """returns number entered by the user, raises exceptions in invalid 
        cases"""
        
        try:
            #get number
            number = float(self.entry.get())
            self.entry.delete(0,tk.END)
            try:
                #check if value ranges are respected
                if typeArgument=="probability" and (number<0 or number>1):
                    raise ValueError("A probability must be between 0 and 1")
                elif typeArgument=="int" and number<=0:
                    raise ValueError("The number must be positive")
                return number
            except ValueError:
                #tell user to reenter a valid number
                self.errorwindow = tk.Tk()
                label = tk.Label(master=self.errorwindow, text='Please pay attention to the allowed value ranges')
                label.grid(row=0, column=0)
                button = tk.Button(master=self.errorwindow, text="OK", width=15, 
                                   height=5, command = self.errorwindow.destroy)
                button.grid(row=1, column=0)
                return None
            
        except:
            #tell user to enter number
            self.errorwindow = tk.Tk()
            label = tk.Label(master=self.errorwindow, text='Please enter a number')
            label.grid(row=0, column=0)
            button = tk.Button(master=self.errorwindow, text="OK", width=15, 
                               height=5, command = self.errorwindow.destroy )
            button.grid(row=1, column=0)
        
            
        
    
    
    def go_to_phase1(self, number):
        """displays menu and table layout for phase "transmission and 
        measurement of qubits"""
        #prepare setup for efficient displaying of qubits
        if number >0:
            self.eavesdropper = True
            self.indexList = [0,1,4,5]
            self.eList = [2,3]
        else:
            self.indexList = [0,1,2,3]
            self.eList = []
            self.eavesdropper = False
            
        #setup table for dispaying of qubits    
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
            label_b.grid(row=3,column =0)
            labels = text
        labels = labels + text[:2]
        for i in range(len(labels)):
            if i%3==2:
                h = 3
            else:
                h=2
            label = tk.Label(master=self.phase1_frame, text=labels[i], width = 10, height = h)
            label.grid(row = i, column = 1)
        #setup menu
        self.phase_label.delete(1.0, tk.END)
        self.phase_label.insert(tk.END,"Phase 1: Transmission of qubits")
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
            
    def go_to_phase2(self):
        """display menu for phase "key sifting" """
        self.phase_label.delete(1.0, tk.END)
        self.phase_label.insert(tk.END,'Phase 2: Key Sifting')
        self.btn_1['text'] = 'Compare bases'
        self.btn_2.grid_remove()
        self.btn_3.grid_forget()
        self.empty_space2.grid(row=2, column=0)
        self.empty_space.grid(row=4, column =0)
        self.btn_1['command'] = self.compare_bases
        self.main_label.grid_forget()
        self.entry.grid_forget()
        self.empty_space3.grid(row=0, column=0)
        
    def go_to_phase3(self):
        """display menu for phase "calculation of error rate" """
        self.empty_space3.grid_forget()
        self.phase_label.delete(1.0, tk.END)
        self.phase_label.insert(tk.END,'Phase 3: Error rate')
        self.btn_1['text'] = 'Compute error rate'
        self.main_label['text'] = 'Choose number of samples'
        self.btn_1['command'] = self.error_rate
        self.entry.grid(row=1,column=0)
        self.main_label.grid(row=0, column=0)
        self.btn_3.grid_forget()
        self.empty_space.grid(row=4, column =0)
    def go_to_phase4(self):
        """display menu for phase "error correction" """
        self.main_label.grid_forget()
        self.entry.grid_forget()
        self.empty_space3.grid(row=0, column=0)
        self.phase_label.delete(1.0, tk.END)
        self.phase_label.insert(tk.END,'Phase 4: Error correction')
        self.btn_1['text'] = 'One error correction step'
        self.empty_space2.grid_remove()
        self.btn_2['text'] = 'All error correction at once'
        self.btn_2.grid(row=2,column=0)
        self.btn_1['command'] = self.error_correction_one_step
        self.btn_2['command'] = self.error_correction
        self.phase4_frame = tk.Frame(master=self.process_frame)
        self.phase4_frame.grid(row=4,column=0)
        row_b = self.setUpNames(self.phase4_frame)
    def go_to_phase5(self):
        """display menu for phase "privacy amplification" """
        self.phase_label.delete(1.0, tk.END)
        self.phase_label.insert(tk.END,'Phase 5: Privacy amplification (PA)')
        self.btn_1['text'] = 'One PA step'
        self.btn_2['text'] = 'All PA steps at once'
        self.btn_1['command'] = self.privacy_amplification_one_step
        self.btn_2['command'] = self.privacy_amplification
        self.btn_3.grid_forget()
        self.empty_space.grid(row=4, column=0)
            
        self.phase5_frame = tk.Frame(master=self.process_frame)
        self.phase5_frame.grid(row=5,column=0)
        row_b = self.setUpNames(self.phase5_frame)
            



    def displaying(self, number, plottingList):
        """display the transmission and measurement of one qubit in the 
        tkinter window"""
        objects = []
        rn=0
        images = 0
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
                if images!=len(plottingList)-1:
                    name = str(i[0])+str(i[1])+".png"
                    load = Image.open(name)
                    render = ImageTk.PhotoImage(load)
                    img = tk.Label(master=self.phase1_frame, image=render)
                    img.image = render
                    img.grid(row=rn, column=2+number)
                    rn+=1
                    images+=1
            else:
                objects.append(None)
                objects.append(None)
                rn+=3
                images+=1
        self.phase1Objects.append(objects) 
        

        if self.currentStep == 0:
            self.empty_space.grid_forget()
            self.btn_3.grid(row=4, column=0)

    def compare_bases(self):
        """perform the step key sifting and display the result"""
        for i in range(self.currentStep):
            #determine of bases are the same
            value = self.channel.compareBasis(i)
            #highlight in green if so
            if value:
                for n in self.indexList:
                    self.phase1Objects[i][n]['background']='green2'
                if self.eavesdropper:
                    if self.channel.compareBasisE(i):
                        for n in self.eList:
                            self.phase1Objects[i][n]['background']='pale green'
        #replace the bit arrays by the new ones
        self.channel.replaceKey()   
        #display the new bit arrays         
        self.phase2_frame = tk.Frame(master=self.process_frame)
        self.phase2_frame.grid(row=1,column=0)
        row_b = self.setUpNames(self.phase2_frame)
        offset =2
        tmp = []
        bitArray = self.channel.getBits()
        for n in range(len(bitArray[0])):
            for i in range(len(bitArray)):
                if bitArray[i][n] !=-1:
                    label = tk.Label(master=self.phase2_frame, text=str(bitArray[i][n]), width=2, height=2)              
                    label.grid(row=1+i, column=offset+n)
                if len(bitArray)==2 or i!=1:
                    tmp.append(label)
            self.phase2Objects.append(tmp)
            tmp = []
        #display go-to-next-phase button
        self.empty_space.grid_forget()
        self.btn_3.grid(row=4, column=0)
    
    def setUpNames(self, frame):
        """displays the table header in a given frame"""
        label = tk.Label(master=frame, text="Shared Key",width = 10, height = 2)
        label.grid(row=0,column=1)
        label_a = tk.Label(master=frame, text='Alice',width = 10, height = 2)
        label_a.grid(row=1,column=1)
        if self.eavesdropper:
            label_e = tk.Label(master=frame, text='Eve',width = 10, height = 2)
            label_e.grid(row=2, column=1)
            row_b=3
        else:
            row_b=2
        label_b = tk.Label(master=frame, text='Bob',width = 10, height = 2)
        label_b.grid(row=row_b, column=1)
        return row_b
               
    def error_rate(self):
        """calculates the error rate on a random subsample of the size that 
        the user specified"""
        number = int(self.getNumber("int"))
        while number==None:
            number = self.getNumber("int")
        if number > self.channel.a.getArrayLength():
            number == self.channel.a.getArrayLength()-1
        #get subset for error calculation
        subset = self.channel.getSubset(number)

        counter = 0
        for i in subset:
            #display subset for calculation
            for label in self.phase2Objects[i]:
                label['background'] = 'orange'
            #count errors
            if self.channel.compareBit(i)==False:
                counter+=1
        #calculate error
        error=float(counter)/float(len(subset))
        
        #display results
        self.phase3_frame = tk.Frame(master=self.process_frame)
        self.phase3_frame.grid(row=2, column=0)
        error_label = tk.Label(master=self.phase3_frame, text = 'The error rate is ' + str(error) + '. Do you want to abort or continue with postprocessing?' )
        error_label.grid(row=0, column=0)
        self.button_frame = tk.Frame(master=self.phase3_frame)
        self.button_frame.grid(row=1, column=0)
        #give the user the choice to abort or to continue
        button_abort = tk.Button(master=self.button_frame, text = 'Abort', command = self.abort)
        button_abort.grid(row=0, column=0)
        button_continue = tk.Button(master=self.button_frame, text = 'Continue with postprocessing', command = self.continue_postprocessing)
        button_continue.grid(row=0,column=1)

        
    def continue_postprocessing(self):
        """displays table after the error rate calculation"""
        self.channel.forgetIndices()
        self.button_frame.grid_forget()
        self.button_frame.destroy()
        frame = tk.Frame(master=self.process_frame)
        frame.grid(row=3,column=0)
        row_b = self.setUpNames(frame)
        offset = 2
        tmp = []
        bitArray = self.channel.getBits()
        for n in range(len(bitArray[0])):
            for i in range(len(bitArray)):
                if bitArray[i][n] !=-1:
                    label = tk.Label(master=frame, text=str(bitArray[i][n]), width=2, height=2)              
                    label.grid(row=1+i, column=offset+n)
                    if len(bitArray)==2 or i!=1:
                        tmp.append(label)
            self.phase3Objects.append(tmp)
            tmp = []
        self.go_to_next_phase()
    
    def error_correction_one_step(self):
        """performs and displays one step of XOR error correction"""
        #color previously handled values in a different color
        for item in self.two_values:
            for label in self.phase3Objects[item]:
                label['background']='yellow'   
        #get results of error correction
        self.two_values, keep, valice, vbob, ve  = self.channel.errorCorrectionOneStep()
        #if there are enough values to do one step
        if self.two_values!=None:
            #highlight selected values, position 0 in dark orange, position 1 
            #in light orange
            for label in self.phase3Objects[self.two_values[0]]:#self.indices.index(i)]:
                label['background']='dark orange'
            for label in self.phase3Objects[self.two_values[1]]:#self.indices.index(i)]:
                label['background']='orange'
            #display result
            if keep:
                tmp = []                
                label_a = tk.Label(master = self.phase4_frame, text = str(valice), width=2, height=2)
                label_a.grid(row=1, column=2+self.number_of_error_steps)
                if ve!=-1:
                    label_e = tk.Label(master = self.phase4_frame, text = str(ve), width=2, height=2)
                    label_e.grid(row=2, column=2+self.number_of_error_steps)
                label_b = tk.Label(master = self.phase4_frame, text = str(vbob), width=2, height=2)
                if self.eavesdropper: row_b =3 
                else: row_b=2
                label_b.grid(row=row_b, column=2+self.number_of_error_steps)
                tmp.append(label_a)
                tmp.append(label_b)
                self.phase4Objects.append(tmp)
                self.number_of_error_steps +=1
        #if there are not enough value to do one step
        else:
            #display go-to-next-phase button
            self.empty_space.grid_forget()
            self.btn_3.grid(row=4, column=0)
            

            
        
        
    def error_correction(self):
        """perform all possible error correction steps"""
        while self.two_values!=None:
            self.error_correction_one_step()
        #display go-to-next-phase button
        self.empty_space.grid_forget()
        self.btn_3.grid(row=4, column=0)
        
            
    def privacy_amplification_one_step(self):
        """performs and displays one step of XOR privacy amplification"""
        #color previously handled values in a different color
        for item in self.two_values:
            for label in self.phase4Objects[item]:
                label['background']='yellow'    
        #get results of privacy amplification
        self.two_values, valice, vbob, veve  = self.channel.privacyAmplificationOneStep()
        #if there are enough values to do one step
        if self.two_values!=None:
            #highlight selected values
            for i in self.two_values:
                for label in self.phase4Objects[i]:#self.indices.index(i)]:
                    label['background']='orange'  
            #display result
            label_a = tk.Label(master = self.phase5_frame, text = str(valice), width=2, height=2)
            label_a.grid(row=1, column=2+self.number_of_error_steps)
            if veve !=-1:
                label_e = tk.Label(master = self.phase5_frame, text = str(veve), width=2, height=2)
                label_e.grid(row=2, column=2+self.number_of_error_steps)
            if self.eavesdropper: row_b =3 
            else: row_b=2
            label_b = tk.Label(master = self.phase5_frame, text = str(vbob), width=2, height=2)
            label_b.grid(row=row_b, column=2+self.number_of_error_steps)
            self.number_of_error_steps +=1
        #if there are not enough values to do one step
        else:
            #start finish routine
            self.finish_routine()
     
    def privacy_amplification(self):
        """performs all possible privacy amplification steps"""
        while self.two_values!=None:
            self.privacy_amplification_one_step() 

    def finish_routine(self):
        """prepares menu for restart and displays message about result"""
        self.btn_3['text'] = 'Restart'
        self.btn_3['command'] = self.restart
        self.empty_space.grid_forget()
        self.btn_1.grid_forget()
        self.btn_2.grid_forget()
        self.empty_space.grid(row=1, column=0)
        self.empty_space2.grid(row=2, column=0)
        self.btn_3.grid(row=4, column=0)
        frame = tk.Frame(master = self.process_frame)
        frame.grid(row=6, column=0)
        self.channel.replaceKey()
        sharedKey, private = self.channel.compareFinalKeys()
        if sharedKey:
            if private:
                displayText = 'Congratulations. You have obtained a shared private key. You can try again or exit.'
            else:
                displayText = 'Unfortunately, Eve knows at least parts of your shared private key. You might want to try again by clicking on restart.'
        else:
            displayText = 'Unfortunately, you have not obtained the same private key. You might want to try again by clicking on restart.'
        label = tk.Label(master=frame, text=displayText)
        label.grid(row=0, column=0)
    def restart(self):
        """resets all necessary values and restarts tkinter"""
        self.window.destroy()
        self.channel = None
        self.currentStep = 0
        self.number_of_error_steps = 0
        self.phase = 0
        self.phase1Objects = []
        self.phase2Objects = []
        self.phase3Objects = []
        self.phase4Objects = []
        self.two_values = []
        self.initializeTkinter()
    def abort(self):
        """restarts program"""
        self.restart()

    
