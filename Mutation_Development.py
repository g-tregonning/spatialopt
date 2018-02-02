# -*- coding: utf-8 -*-
"""
Testing designing my own mutation operator
Issue with the stock ones are:
    1. Theres much more zeros than development sites
    2. Need to change it from tools.mutFlipBit
    3. 
    
Issues:
    ~ If I write my own mutation operator I need to delete the fitness values
        # code: del mutant.fitness.values
    
Notes on Operator:
    ~ tools.mutGaussian returns the values changed by a degree of the mean
        # [0,0,30,0] to ([0, 0.03321389240473166, 30, -0.0047020427687865],)
    ~ tools.mutShuffleIndexes moves the attriutes around
        # [0,0,30,0,60] to ([0, 60, 0, 30, 0],)
        # Seems ideal
        # Retain the same numer of dwellings
        # Suggest using this
        
    ~ tools.mutFlipBit flips values from 0 to 1 or vice verse
        # [0,0,30,0,60] to ([1, 1, 0, 1, 0],)
    ~ tools.mutUniformInt creates a random integer to put it
        # [0,0,30,0,60] to ([24, 14, 10, 24, 12],)
        # based on low = 10, up = 30
        # work for the old algorithm
"""
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

toolbox = base.Toolbox()

test = [0,0,30,0,60]

mutant = toolbox.clone(test)
print tools.mutShuffleIndexes(mutant, indpb = 1)

a,v = [],[]
print a
print v