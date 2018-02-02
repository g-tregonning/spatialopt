# -*- coding: utf-8 -*-
"""
version 3 - Trying to incoportate both 200 and 500 metre spatial resolution

"""

import numpy as np
import rasterIO
data_folder= "C:/Users/danie_000/Python_Codes/Data/London/Rasters/200m Resolution/"

file_pointer = rasterIO.opengdalraster(data_folder+'Undeveloped.tif')  
Undev=rasterIO.readrasterband(file_pointer,1) 
driver, XSize, YSize, proj_wkt, geo_t_params = rasterIO.readrastermeta(file_pointer)

def Plan(Development_Plan, Spat_Res):
    # Function which takes an empty raster for the entire London Dataset and
    # assigns the development sites from the individual
    from copy import copy
    
    # importing boundary file to create an empty raster to write to
    # Add the folder name onto the data folder using the spatial resolution
    data_spat_res_folder = data_folder+str(Spat_Res)+"m Resolution/" 
    file_pointer = rasterIO.opengdalraster(data_spat_res_folder+'Boundary.tif') 
    Boundary=rasterIO.readrasterband(file_pointer,1) 
    
    Bound_copy = copy(Boundary)
    # creating a blank array of london to add our new dwellings to
    # tested the sum which is 0 
    # Making it a double so that the large values will be kept
    Lndn_Dev_Plan =np.double(np.subtract(Boundary,Bound_copy))
    

    # instead of callin an indiidual module based on spatial resolution
    # calling a module and giing it the spat res so it can generate
    # its own look up table
    import London_Lookup as Lookup
    
    # Using the lookup module to generate a look up table    
    Undev_Lookup = Lookup.Generate_Lookup(Spat_Res)
    
    # So for each dwelling site in the development pla
    for a in range(0,len(Development_Plan)):
        # we find its corresponding location in the overall london plan
        # and assign the development there
        yx = Undev_Lookup[a]
            
        Lndn_Dev_Plan[yx]=Development_Plan[a]

    return Lndn_Dev_Plan       


def Write(Development_Plan, Name, Results_folder):
    Lndn_Dev_Plan = Development_Plan
   
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

    
    