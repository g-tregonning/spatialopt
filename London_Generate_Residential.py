# -*- coding: utf-8 -*-
"""

"""
import numpy as np

import rasterIO # allows the reading of rasters into arrays


"""""""""""""""""""""""""""""""""""""""
# DATASETS USED
"""""""""""""""""""""""""""""""""""""""

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
    agg, dev_list = 0,[]
    while agg < Tot_Dwell:
        # Selecting a random development density
        dev = rnd.randint(0,3)
        # Add four time the amount of dwellings density as working at 200m
        # resolution which is 
        agg +=  4*(Density_Lookup[dev])
        dev_list.append(Density_Lookup[dev])
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
    
    
print  Generate_Residential(340000)

