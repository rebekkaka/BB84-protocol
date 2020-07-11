#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 20:44:43 2020

@author: rebekka
"""


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
        if self.e!=None:
            return [[tmp, tmp1], [tmp2, tmp3], [tmp4, tmp5]]
        else:
            return [[tmp, tmp1], [tmp4, tmp5]]
    def compareBasis(self, number):         
        if self.a.basis_array[number]==self.b.basis_array[number]:
            for person in self.peopleList:
                if person.name!="Eve" or self.compareBasisE(number):
                    person.keepBit(number)
                else:
                    person.keepBit(-1)
            return True
        else:
            return False

    def compareBasisE(self, number):
        if self.e !=None:
            if self.a.basis_array[number]==self.e.basis_array[number] and self.e.bit_array[number]!=-1:
                return True
            else:
                return False
    def replaceKey(self):
        for person in self.peopleList:
            person.replaceKey()
    def compareBit(self, number):            
        if self.a.bit_array[number]==self.b.bit_array[number]:
            return True
        else:
            return False
    
    def getBits(self):
        Alist = self.a.getBits()
        Blist = self.b.getBits()
        if self.e !=None:
            Elist = self.e.getBits()
            return [Alist, Elist, Blist]
        else:
            return [Alist, Blist]
        
    def getSubset(self, number, keepTrack=False):
        return self.a.getNewSubset(number, keepTrack)
    def forgetIndices(self):
        print(self.a.bit_array)
        print(self.a.newBitArray)
        subset = self.a.subset
        for i in range(len(self.a.bit_array)):
            if i in subset:
                pass
            else:
                for person in self.peopleList:
                    person.keepBit(i)
        self.preparePostprocessing()
        
    def preparePostprocessing(self):
        for person in self.peopleList:
            person.replaceKey()
        self.a.indices = list(range(len(self.a.bit_array)))
    def errorCorrectionOneStep(self):
        twoValues = self.getSubset(2, keepTrack=True)
        if twoValues !=None:
            value_alice = self.a.XOR(twoValues[0],twoValues[1])
            value_bob = self.b.XOR(twoValues[0],twoValues[1])
            if value_alice==value_bob:
                self.a.keepBit(twoValues[0])
                self.b.keepBit(twoValues[0])
                if self.e!=None:
                    if self.e.bit_array[twoValues[0]]!=-1:
                        ve = self.e.bit_array[twoValues[0]]
                        self.e.keepBit(twoValues[0])
                    elif self.e.bit_array[twoValues[1]]!=-1:
                        ve = self.e.XOR(twoValues[1], value_alice, True)
                        self.e.keepBit(ve, value=True)
                    else:
                        ve=-1
                        self.e.keepBit(-1)
                else:
                    ve = -1
                
                return [twoValues, True, self.a.bit_array[twoValues[0]], self.b.bit_array[twoValues[0]],ve]
        
        return [twoValues, False, -1, -1,-1]
    def privacyAmplificationOneStep(self):
        twoValues = self.getSubset(2, keepTrack=True)
        if twoValues !=None:
            value_alice = self.a.XOR(twoValues[0],twoValues[1])
            value_bob = self.b.XOR(twoValues[0],twoValues[1])
            self.a.keepBit(value_alice, value=True)
            self.b.keepBit(value_bob, value=True)
            value_eve = -1
            if self.e !=None:
                if self.e.bit_array[twoValues[0]]!=-1 and self.e.bit_array[twoValues[1]]!=-1:
                    value_eve =  self.e.XOR(twoValues[0],twoValues[1], False)
                    self.e.keepBit(value_eve, value=True)
                else:
                    self.e.keepBit(-1)
            return [twoValues, value_alice, value_bob, value_eve]
        return [twoValues, -1, -1, -1]
