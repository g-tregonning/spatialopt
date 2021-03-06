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
from Undev_brwnfld_Inten_Lookup_200 import Undev_Lookup

No_Undev        = len(Undev_Lookup)

Density_Lookup  = [60,100,150,350] # Different densities of residential development
Site_Hectares   = 25

def Generate_Residential(Tot_Dwell):
    import random as rndm
    if rndm.random() > 0.5:
        Density_Lookup  = [60,60,60,60]
    else:
        Density_Lookup  = [60,100,150,350]
    # Agg stores the aggregate 
    agg, dev_list = 0,[]
    while agg < Tot_Dwell:
        # Selecting a random development density
        dev = rndm.randint(0,3)
        # Multiply the density per hectare 
        agg +=  (Density_Lookup[dev]) * Site_Hectares
        dev_list.append(Density_Lookup[dev])
    Lndn_Plan = [0] * No_Undev
    for dev_site in dev_list:
        while True:        
            rand_site = rndm.randint(0,No_Undev-1)
            # Check development hasn't already been assigned to this site
            if Lndn_Plan[rand_site]==0:
                Lndn_Plan[rand_site]=dev_site
                break
            
    return Lndn_Plan
    
import Evaluate_v4_200 as Eval

Development_Plan = Generate_Residential(340000)    
Mixed_Landuse_Fit = Eval.Calc_fmixedlanduse(Development_Plan)
print Mixed_Landuse_Fit   

#Total_Sites     = np.count_nonzero(Generate_Residential(340000))
#print Total_Sites

#test = test_Generate_Residential(340000)

#import Evaluate_v2_500 as Eval
#print Eval.Calc_fbrownfield(test)
#print "sum", sum(test)

#import Write_Raster_v1_500 as WR

#WR.Write(test, "test", "C:/Users/danie_000/")