# -*- coding: utf-8 -*-
"""
Testing the cross over operators to decide which would be best for the london application

Notes:
    ~ cxTwoPoints and cxOnePoint 
        # Do what they say on the tin
    ~ cxUniform
        # Swaps the attributes based on a probability
        # ([7, 2, 9, 10, 5, 6], [1, 8, 3, 4, 11, 12])
    ~ cxPartialyMatched
        # Doesn't work
        # Pretty sure input is wrong for it
    ~ cxUniformPartialyMatched
        # Same as above
    ~ cxOrdered
        # Think it needs a list
    ~ 
    
"""

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

toolbox = base.Toolbox()

a = [1,2,3,4,5,6]
b = [7,8,9,10,11,12]

c = (1,2,3,4,5,6)
d = (7,8,9,10,11,12)

#print tools.(a,b,)

print tools.cxPartialyMatched(c,d)
