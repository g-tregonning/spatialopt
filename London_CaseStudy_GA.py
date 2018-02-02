# -*- coding: utf-8 -*-
"""
Created on Sun Jul 06 17:14:24 2014

@author: danie_000
"""

import rasterIO
from copy import copy 
import numpy as np

data_folder= "C:/Users/danie_000/Python_Codes/Data/London/Rasters/100m Resolution/"

file_pointer = rasterIO.opengdalraster(data_folder+'Undev_new2.tif')  
Undev=rasterIO.readrasterband(file_pointer,1) 
driver, XSize, YSize, proj_wkt, geo_t_params = rasterIO.readrastermeta(file_pointer)

file_pointer = rasterIO.opengdalraster(data_folder+'Heat.tif')  
Heat=rasterIO.readrasterband(file_pointer,1) 

def Generate_Residential():
    import numpy as np
    import random as rnd
    
    Density_Lookup = [0,60,100,150,350]
    
    Tot_Dwell =340000
    agg = 0
    dev_list = []
    while agg < Tot_Dwell:
        dev = rnd.randint(1,4)
        agg +=  Density_Lookup[dev]
        dev_list.append(Density_Lookup[dev])
        print agg
            
    print len(dev_list)
    print agg
    
    
    Lndn = [0] * 19361
    import random as rndm
    for dev_site in dev_list:
        rand_site = rndm.randint(0,19361)
        #print rand_site
        #print dev_site
        if Lndn[rand_site]==0:
            Lndn[rand_site]=dev_site
            
    Lndn_Vuln = np.multiply(Lndn, 2.3)
    print sum(Lndn_Vuln)
    
    from collections import Counter
    print Counter(Lndn)
    
    return Lndn_Vuln

print XSize, YSize
undev_list = []
for x in range(0,XSize):
    for y in range(0,YSize):
        if Undev[y,x]==1:
            undev_list.append([y,x])
print len(undev_list)

undev_copy = copy(Undev)
    

New_Vuln =np.subtract(Undev,undev_copy)

dev = Generate_Residential()

import Undeveloped_Lookup

for a in range(0,len(dev)):
    yx = Undeveloped_Lookup.Undev_Lookup[a]
    New_Vuln[yx]=dev[a]
    
Risk = np.multiply(New_Vuln, Heat)
print "Heat Risk is ", np.sum(Risk)