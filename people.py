#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 17:50:46 2020

@author: rebekka
"""

import random
import numpy as np

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
    def getInfo(self, number):
        return self.bit_array[number], self.basis_array[number]
    def keepBit(self, index):
        pass
    def deleteBit(self, index):
        self.bit_array.pop(index)

    
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