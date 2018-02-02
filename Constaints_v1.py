# -*- coding: utf-8 -*-
"""
Module Containing a series of constraint handling for the genetic algorithm
Ensures it can 


Aspiration would be to calculate on average how many child solutions are removed

"""

def PTAL_Constraint(PTAL, Site, Density):
    # Catch the 150, 250 and 400 uha densities between PTAL 6B (2) and PTAL 4 (5)
    print(PTAL)
    if Density >= 150 and PTAL[Site] < 6:
        return True
    # Catch 100 u/ha density in either PTAL 3 (6) or PTAL 2 (7)
    elif Density == 100 and PTAL[Site] == 6 or Density == 100 and PTAL[Site] == 7:
        return True
    # Catch 60 and 35 u/ha'
    elif Density >= 60 and PTAL[Site] >= 8:
        return True
    else:
        return False

def DwellingTotal_Constraint(DwellingPlan, Dwellings_Min, Dwellings_Max):
    if sum(DwellingPlan) < Dwellings_Min or sum(DwellingPlan) > Dwellings_Max:
        return True
    else:
        return False

def Remove(orig_tuple, element_to_remove):
    # Function which is called once a child in the offspring is found to
    # exceed the maximum number of households or be lower than the minimum
    lst = list(orig_tuple)
    lst.remove(element_to_remove)
    # return the offspring array with the element removed
    return tuple(lst)    

def Check_PTAL_Constraint(PTAL, Lookup):
    # Decrotor function acts as a constraint which interupts the selection 
    # process to ensure that the children selected achieve the required
    # number of dwellings
    def decCheckBounds(func):
        def wrapCheckBounds(*args, **kargs):
            # Extract the offspring solutions
            offsprings = func(*args, **kargs)
            # Extract each of the children from the offspring
            for child in offsprings:
                # loop continues until a child which doesnt comply is found
                # at which point it breaks the loop
                while True:
                    for x in range(0, len(Lookup)):
                        # if there is a proposed development on this site
                        if child[x]> 0:
                            # Site is the location within the entire london plan
                            Site =  Lookup[x]                       
                            Density = child[x]
                            if PTAL_Constraint(PTAL, Site, Density)== False:
                                # if a site is found to not comply with density 
                                # matrix, the child is deleted
                                offsprings=Remove(offsprings,child)                             
                                break
                        
            return offsprings
        return wrapCheckBounds
    return decCheckBounds   
    
def Check_TotDwellings_Constraint(Dwellings_Min, Dwellings_Max):
    # Decrotor function acts as a constraint which interupts the selection 
    # process to ensure that the children selected achieve the required
    # number of dwellings
    def decCheckBounds(func):
        def wrapCheckBounds(*args, **kargs):
            # Extract the offspring solutions
            offsprings = func(*args, **kargs)
            # Extract each of the children from the offspring
            for child in offsprings:
                if DwellingTotal_Constraint(child, Dwellings_Min, Dwellings_Max) == True:
                    # if a development plan doesnt fall between the min and max
                    # it is removed from the offspring
                    offsprings=Remove(offsprings,child)
            return offsprings
        return wrapCheckBounds
    return decCheckBounds   
