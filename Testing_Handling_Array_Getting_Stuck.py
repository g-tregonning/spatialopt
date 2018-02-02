# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 09:17:30 2014

@author: danie_000
"""

import random as rndm

def Generate():
    test = [0]*5
    check_sum = 0
    check_count = 0
    while sum(test) < 25:
                
        new = rndm.randint(0,7)
        test_element = rndm.randrange(0,len(test))
        if test[test_element] == 0:
            test[test_element] = new
        if check_sum == sum(test):
            check_count += 1
        else:
            check_count = 0
            check_sum = sum(test)
            
            
        if check_count > 100:
            return False
    return test


while True:
    Array = Generate()
    print Array
    if Array != False:
        break
        
print "Array", Array, sum(Array)