# -*- coding: utf-8 -*-
"""
Module to provide a initial spatial plan which concentrates on brownfield development
This is in order to provide a good initialisation helping towards convergence 
on the best spatial plan

Intention that this module will be called based on a probability and return 
"""

"""""""""""""""""""""""""""""""""""""""
# IMPORT DATASETS
"""""""""""""""""""""""""""""""""""""""
import rasterIO
data_folder= "C:/Users/danie_000/Python_Codes/Data/London/Rasters/500m Resolution/"

file_pointer = rasterIO.opengdalraster(data_folder+'Undeveloped.tif')  
Undev=rasterIO.readrasterband(file_pointer,1) 
driver, XSize, YSize, proj_wkt, geo_t_params = rasterIO.readrastermeta(file_pointer)
 
import numpy as np

def Generate_Residential_brownfield(dev_list, Lndn_Plan, No_Undev):
    import random as rndm
    Brownfield      = np.double(rasterIO.readrasterband(rasterIO.opengdalraster(data_folder+'Brownfield.tif'),1))
    from Undev_brwnfld_Lookup_500 import Undev_Lookup
    for dev_site in dev_list:
        while True:  
            
            rand_site = rndm.randint(0,No_Undev-1)
            # Check development hasn't already been assigned to this site
            if Lndn_Plan[rand_site]==0:
                
                if Brownfield[Undev_Lookup[rand_site]] == 1:
                    Lndn_Plan[rand_site] = dev_site
                    break
            
    return Lndn_Plan