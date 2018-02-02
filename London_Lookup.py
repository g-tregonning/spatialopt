# -*- coding: utf-8 -*-
"""
London Lookup 26/08/14

Intention to coincide with GA v2 which instead of calling different modules 
depening on the different spatial resolutions just defines the spatial 
and gives it to the modules to calculate itself.

So the function will find the undeveloped brownfield and intensification raster
and generate a look up table itself and return it. 

Intention is for the GA module to call it along with the evaluation and write
raster modules

NOTE:
    + Need to check it doesn't greatly increase the operating time. 
    + compare this to having different modules with preset 
"""

def Generate_Lookup(Spatial_Res):
    # Imports the file which allows for rasters to be opened into arrays    
    import rasterIO
    
    # define the data folder based on the spatial resolution (added to the folder name)
    data_folder= "C:/Users/danie_000/Python_Codes/Data/London/Rasters/"+str(Spatial_Res)+"m Resolution/"
    
    # Open the Undev_Brwnfld_Intn from this file into an array
    file_pointer = rasterIO.opengdalraster(data_folder+'Undev_Brwnfld_Intn.tif')  
    Undev=rasterIO.readrasterband(file_pointer,1) 
    driver, XSize, YSize, proj_wkt, geo_t_params = rasterIO.readrastermeta(file_pointer)
    
    # Define the arrya which contains the locations of undev brownfield and 
    # intensification areas
    Undev_Lookup =[]
    for x in range(0,XSize):
        for y in range(0,YSize):
            if Undev[y,x]==1:
                site =  (y,x)
                Undev_Lookup.append(site)
    
    return Undev_Lookup
    
    
    
    
    
    
    
    