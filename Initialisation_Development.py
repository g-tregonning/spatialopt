# -*- coding: utf-8 -*-
"""
Testing the initialisation function

Intention to have groupings of dwelling sizes as opposed to assigning random values
to the London Plan

Incomplete! Gets very complicated

"""
import numpy as np
import random as rndm
import rasterIO # allows the reading of rasters into arrays

data_folder= "C:/Users/danie_000/Python_Codes/Data/London/Rasters/200m Resolution/"

file_pointer = rasterIO.opengdalraster(data_folder+'Undeveloped.tif')  
Undev=rasterIO.readrasterband(file_pointer,1) 
driver, XSize, YSize, proj_wkt, geo_t_params = rasterIO.readrastermeta(file_pointer)

No_Undev = 4986

def Generate_Residential(Tot_Dwell):
    import random as rnd
    # Assuming we are working with 100x100m grids
    Density_Lookup = [60,100,150,350]
    # Agg stores the aggregate 
    # dev_list holds a list of the dwelling sizes 
    agg, dev_list = 0,[]
    # Develop up a listof different development sizes
    while agg < Tot_Dwell:
        # Selecting a random development density
        dev = rnd.randint(0,3)
        # Add four time the amount of dwellings density as working at 200m
        # resolution which is 
        agg +=  4*(Density_Lookup[dev])
        dev_list.append(Density_Lookup[dev])
    
    from collections import Counter 
    
    count_dwells = Counter(dev_list)
    # Count the number of sites for each dwelling density
    small   = count_dwells[60]    
    med     = count_dwells[100]
    large   = count_dwells[150]
    xlarge  = count_dwells[350]    
        
    dwelling_sizes = [small,med, large,xlarge]
    
    for size in dwelling_sizes:
        while size != 0:
            # get a random number of sites
            rndm_size = rndm.randint(0,size)
            # reduce the number of sites for each dwelling density            
            size = size - rndm_size
            
            Lndn_Plan = [0] * No_Undev
            import random as rndm
            while True:        
                rand_site = rndm.randint(0,No_Undev-1)
                # Check development hasn't already been assigned to this site
                if Lndn_Plan[rand_site]==0:
                    Lndn_Plan[rand_site]=dev_site
                    break
            
    
    Lndn_Plan = [0] * No_Undev
    import random as rndm
    for dev_site in dev_list:
        while True:        
            rand_site = rndm.randint(0,No_Undev-1)
            # Check development hasn't already been assigned to this site
            if Lndn_Plan[rand_site]==0:
                Lndn_Plan[rand_site]=dev_site
                break
            
    return Lndn_Plan
    
Generate_Residential(340000)
