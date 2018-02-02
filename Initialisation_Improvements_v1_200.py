# -*- coding: utf-8 -*-
"""
19/08/14

Previously Brownfield_Initialisation_v1_500 and 
Initialisation_Improvements_v1_500
rewritten for 200 metre spatial resolution

Module to provide a initial spatial plan which concentrates specificed types of 
development

This is in order to provide a good initialisation helping towards convergence 
on the best spatial plan. updated to use Undev_brwnfld_Inten_Lookup_500

Intention that this module will be called based on a probability and return
a development plan concentrted in certain areas

Notes: 
    - sprawl added

  
"""

"""""""""""""""""""""""""""""""""""""""
# IMPORT DATASETS
"""""""""""""""""""""""""""""""""""""""
import rasterIO
data_folder= "C:/Users/danie_000/Python_Codes/Data/London/Rasters/200m Resolution/"

file_pointer = rasterIO.opengdalraster(data_folder+'Undeveloped.tif')  
Undev=rasterIO.readrasterband(file_pointer,1) 
driver, XSize, YSize, proj_wkt, geo_t_params = rasterIO.readrastermeta(file_pointer)
 
import numpy as np

def Generate_Residential_brownfield(dev_list, Lndn_Plan, No_Undev):
    # Theres a statement to prevent dev_lists with more than 91 
    # sites as there are only 91 brownfield sites available.

    import random as rndm
    Brownfield      = np.double(rasterIO.readrasterband(rasterIO.opengdalraster(data_folder+'Brownfield.tif'),1))
    from Undev_brwnfld_Inten_Lookup_200  import Undev_Lookup
    
    for dev_site in dev_list:
        while True:  
            
            rand_site = rndm.randint(0,No_Undev-1)
            # Check development hasn't already been assigned to this site
            if Lndn_Plan[rand_site]==0:
                
                if Brownfield[Undev_Lookup[rand_site]] == 1:
                    Lndn_Plan[rand_site] = dev_site
                    break
            
    return Lndn_Plan
    
def Generate_Residential_regeneration(dev_list, Lndn_Plan, No_Undev):
    # Generates a development plan which is solely within areas designated for 
    # regeneration    
    
    import random as rndm
    Regeneration      = np.double(rasterIO.readrasterband(rasterIO.opengdalraster(data_folder+'Regeneration.tif'),1))
        
    from Undev_brwnfld_Inten_Lookup_200 import Undev_Lookup
    for dev_site in dev_list:
        while True:  
            
            rand_site = rndm.randint(0,No_Undev-1)
            # Check development hasn't already been assigned to this site
            if Lndn_Plan[rand_site]==0:
                
                if Regeneration[Undev_Lookup[rand_site]] == 1:
                    Lndn_Plan[rand_site] = dev_site
                    break
            
    return Lndn_Plan
def Generate_Residential_floodzone(dev_list, Lndn_Plan, No_Undev):
    # Generates a development plan which excludes floodzone areas    
    import random as rndm
    Floodzone     = np.double(rasterIO.readrasterband(rasterIO.opengdalraster(data_folder+'Floodzone.tif'),1))
    from Undev_brwnfld_Inten_Lookup_200 import Undev_Lookup
    for dev_site in dev_list:
        while True:  
            
            rand_site = rndm.randint(0,No_Undev-1)
            # Check development hasn't already been assigned to this site
            if Lndn_Plan[rand_site]==0:
                if Floodzone[Undev_Lookup[rand_site]] < 1:
                    Lndn_Plan[rand_site] = dev_site
                    break
            
    return Lndn_Plan
                
def Generate_Residential_Urban(dev_list, Lndn_Plan, No_Undev):
    # Generates a development plan which excludes floodzone areas    
    import random as rndm
    Urban     = np.double(rasterIO.readrasterband(rasterIO.opengdalraster(data_folder+'Urban.tif'),1))
    from Undev_brwnfld_Inten_Lookup_200 import Undev_Lookup
    for dev_site in dev_list:
        while True:  
            
            rand_site = rndm.randint(0,No_Undev-1)
            # Check development hasn't already been assigned to this site
            if Lndn_Plan[rand_site]==0:
                if Urban[Undev_Lookup[rand_site]] == 1:
                    Lndn_Plan[rand_site] = dev_site
                    break
            
    return Lndn_Plan                