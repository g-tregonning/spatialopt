# -*- coding: utf-8 -*-
"""
version 2
Using newest Undev_brwnfld_Inten_Lookup_500 which has most recent 


Module to write rasters of the results of the GA algorithm over London


"""

import numpy as np
import rasterIO
data_folder= "C:/Users/danie_000/Python_Codes/Data/London/Rasters/500m Resolution/"

file_pointer = rasterIO.opengdalraster(data_folder+'Undeveloped.tif')  
Undev=rasterIO.readrasterband(file_pointer,1) 
driver, XSize, YSize, proj_wkt, geo_t_params = rasterIO.readrastermeta(file_pointer)

def Plan(Development_Plan):
    # Function which takes an empty raster for the entire London Dataset and
    # assigns the development sites from the individual
    from copy import copy
    undev_copy = copy(Undev)
    # creating a blank array of london to add our new dwellings to
    # tested the sum which is 0 
    # Making it a double so that the large values will be kept
    Lndn_Dev_Plan =np.double(np.subtract(Undev,undev_copy))
    

    # looks up where each undeveloped site lies within the overall London plan
    # currently at the 200m spatial resolution
    import Undev_brwnfld_Inten_Lookup_500 as Lookup
    # Currently ased on dwelling
    # multiply y average dsize dwelling if I want to change it
    # Getting problem that a lot of dwelling lost all of a sudden
    # Ok so problem is that 
    for a in range(0,len(Development_Plan)):
        yx = Lookup.Undev_Lookup[a]
            
        Lndn_Dev_Plan[yx]=Development_Plan[a]

    #print "non zeros of lndn dev plan", np.count_nonzero(Development_Plan) 
    
    #from collections import Counter  
    #print "Count Dev Plan", Counter(Development_Plan)
    #for x in Lndn_Dev_Plan:
     #   print x
   # print "after Planning", np.sum(Lndn_Dev_Plan)
    return Lndn_Dev_Plan    


def Write(Development_Plan, Name, Results_folder):
    Lndn_Dev_Plan = Plan(Development_Plan)
   
    epsg = 27700
    #writerasterbands(outfile, format, XSize, YSize, geotrans, epsg, NoDataVal=None, *rasterarrays)
    outfile = Results_folder+Name+".tif"
    #rasterIO.writerasterbands(outfile = 'C:/Users/danie_000/Python_Codes/Results/Result_test', format = 'GeoTIFF', XSize = 298, YSize = 155, geotrans = (418865.1870485451, 200.0, 0.0, 537326.0941855921, 0.0, -200.0), epsg='2770', NoDataVal=None, *rasterarrays = Boundary)
    rasterIO.writerasterbands(outfile, 'GTiff', XSize, YSize, geo_t_params, epsg, None, Lndn_Dev_Plan)
    print "Written "+(Name)+" Raster"
    
    
def Write_Array(Array_Dev_Plans, Results_folder, suffix):
    # Go through array of spatial plans and save each of them
    count = 0
    for Spatial_Plan in Array_Dev_Plans:
        count += 1        
        Name = suffix+str(count)
        Write(Spatial_Plan, Name, Results_folder)

    
    