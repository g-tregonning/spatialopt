# -*- coding: utf-8 -*-
"""
Module Containing a series of constraint handling for the genetic algorithm
Ensures it can 

Notes:
    - Calculate a total average of the retaintion of offspring solutions
        @ currently done at each iteration
        @ options
            # Keep transfering a variable forward and back between this and GA module
                > a lot of faf
    - PTAL Enforcement
        @ currently enforcing it on each density
        @ Maybe should just be enforced on lower densities?
    

"""

import numpy as np
import rasterIO

def PTAL_Constraint(PTAL, Site, Density):
    #print "PTAL"
    # Newest version of the PTAL constraint 
    #print "Density ", Density, " PTAL ", PTAL[Site]
    # Catch the 150, 250 and 400 uha densities between PTAL 6B (2) and PTAL 4 (5)
    Site = tuple([int(i) for i in Site])
    if Density >= 150:# and PTAL[Site] < 6:
        return True
    # Catch 100 u/ha density in either PTAL 3 (6) or PTAL 2 (7)
    elif Density == 100 and PTAL[Site] >=6:# or Density == 100 and PTAL[Site] == 7:
        return True
    # Catch 60 and 35 u/ha'
    elif Density >= 60 and PTAL[Site] >= 8:
        return True
    else:
        return False
"""
def PTAL_Constraint(PTAL, Site, Density):
    # previous version of the PTAL constraint
    print "Density ", Density, " PTAL ", PTAL[Site]
    # Catch the 150, 250 and 400 uha densities between PTAL 6B (2) and PTAL 4 (5)
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
"""        
def DwellingTotal_Constraint(DwellingPlan, Dwellings_Min, Dwellings_Max):
    # old code which would be used if we are using availability
    # Conversion to a numpy array so a sum can be taken    
    numpy_DwellPlan = np.array( DwellingPlan)
    ravel_numpy_DwellPlan = numpy_DwellPlan.ravel()
    #print "in constraint", sum(ravel_numpy_DwellPlan) 
    print sum(ravel_numpy_DwellPlan) 
    if sum(ravel_numpy_DwellPlan) < Dwellings_Min or sum(ravel_numpy_DwellPlan) > Dwellings_Max:
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

def Check_PTAL_Constraint(Data_Folder):
    # Decrotor function acts as a constraint which interupts the selection 
    # process to ensure that the children selected achieve the required
    # number of dwellings
    def decCheckBounds(func):
        def wrapCheckBounds(*args, **kargs):
            # Extract the offspring solutions
            offsprings = func(*args, **kargs)
            # Extract each of the children from the offspring
            strt_len=len(offsprings)
            
            # Upload the PTAL dataset
            file_pointer = rasterIO.opengdalraster(Data_Folder+'ptal.tif') 
            PTAL = rasterIO.readrasterband(file_pointer,1)
                       
            # Upload the lookup table from the generated file.
            Lookup = (np.loadtxt("lookup.txt",delimiter=",")).tolist()
            for child in offsprings:
                # loop continues until a child which doesnt comply is found
                # at which point it breaks the loop
                
                
                while True:
                    for j in range(0, len(Lookup)):
                        # Convert the j coordinate to an ji coordinate
                        ji = tuple(Lookup[j]) 
                        # if there is a proposed development on this site
                        
                        
                        if child[j]> 0:
                            # Site is the location within the entire london plan                     
                            Density = child[j]
                            if PTAL_Constraint(PTAL, ji, Density)== False:
                                # if a site is found to not comply with density 
                                # matrix, the child is deleted
                                offsprings=Remove(offsprings,child)                             
                                break
                    break
            
            end_len = len(offsprings)
            # Calculate the number of solutions retained after the constraint
            
            per_retained = float(100* end_len/ strt_len)

                
                # Load the previous list of retaintion rates and add new retention
            Retained_list = np.loadtxt("PTAL_Constraint.txt",delimiter=",")
            Updated_Retained_list = np.append(Retained_list,per_retained)
            # Save the updated list
            np.savetxt("PTAL_Constraint.txt", Updated_Retained_list,  delimiter=',', newline='\n', fmt="%i")
            
            #print '% of solutions retained after PTAL Constraint', per_retained
            
            return offsprings
        return wrapCheckBounds
    return decCheckBounds   
    
def Check_TotDwellings_Constraint(Dwellings_Min, Dwellings_Max,
                                  Data_Folder, Site_Hectares):
    # Decrotor function acts as a constraint which interupts the selection 
    # process to ensure that the children selected achieve the required
    # number of dwellings
    def decCheckBounds(func):
        def wrapCheckBounds(*args, **kargs):

            # Extract the offspring solutions
            offsprings = func(*args, **kargs)
            strt_len=len(offsprings)
            #orig_len = len(offsprings)
            # Extract each of the children from the offspring
            for child in offsprings:
                # import intialise module to create a dwelling plan else
                # the total dwellings only counts densities
                num_dwellings = sum(child)* Site_Hectares
                
                #if DwellingTotal_Constraint(DwellPlan, Dwellings_Min, Dwellings_Max) == True:
                if num_dwellings < Dwellings_Min or num_dwellings > Dwellings_Max:
                        
                    # if a development plan doesnt fall between the min and max
                    # it is removed from the offspring
                    offsprings=Remove(offsprings,child)
                    
            end_len = len(offsprings)
           
            # Calculate the number of solutions retained after the constraint
            per_retained = float(100* end_len/ strt_len)
            
            # Load the previous list of retaintion rates and add new retention
            Retained_list = np.loadtxt("Dwell_Constraint.txt",delimiter=",")
            Updated_Retained_list = np.append(Retained_list,per_retained)
            # Save the updated list
            np.savetxt("Dwell_Constraint.txt", Updated_Retained_list,  delimiter=',', newline='\n',fmt="%i")
            
            
            
            #print '% of solutions retained after Total Dwellings Constraint', per_retained
            return offsprings
        return wrapCheckBounds
    return decCheckBounds   

