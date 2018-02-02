# -*- coding: utf-8 -*-
"""
Module created for GA v3

Creating a lookup table for all the sites within the study area which have 
undeveloped space (i.e. not 0%)
"""

def Extract_lookup():
    import rasterIO
    data_folder= "C:/Users/danie_000/Python_Codes/Data/London/"
        
    file_pointer = rasterIO.opengdalraster(data_folder+'Per_Undev.tif')  
    Undev=rasterIO.readrasterband(file_pointer,1) 
    driver, XSize, YSize, proj_wkt, geo_t_params = rasterIO.readrastermeta(file_pointer)
    
    for x in range(0,XSize):
        for y in range(0,YSize):
            if Undev[y,x]>0:
                print "(",y,",",x,"),"
                
Extract_lookup()