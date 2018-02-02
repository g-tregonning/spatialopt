# -*- coding: utf-8 -*-
"""
Module created for GA v3

Creating a lookup table for all the sites within the study area which have 
brownfield space (i.e. not 0%). Intention is to be called by the initialisation
to create a development plan entirely within brownfield areas.
"""

def Extract_lookup():
    import rasterIO
    data_folder= "C:/Users/danie_000/Python_Codes/Data/London/"
        
    file_pointer = rasterIO.opengdalraster(data_folder+'Brwnfld_per.tif')  
    Undev=rasterIO.readrasterband(file_pointer,1) 
    driver, XSize, YSize, proj_wkt, geo_t_params = rasterIO.readrastermeta(file_pointer)
    
    for x in range(0,XSize):
        for y in range(0,YSize):
            if Undev[y,x]>0:
                print "(",y,",",x,"),"
#Extract_lookup()
Brownfield_Lookup = [( 19 , 1 ),
( 33 , 2 ),
( 35 , 3 ),
( 40 , 4 ),
( 41 , 5 ),
( 42 , 6 ),
( 31 , 7 ),
( 55 , 7 ),
( 31 , 8 ),
( 55 , 8 ),
( 47 , 10 ),
( 39 , 11 ),
( 42 , 11 ),
( 43 , 11 ),
( 42 , 12 ),
( 47 , 13 ),
( 55 , 13 ),
( 43 , 14 ),
( 44 , 14 ),
( 54 , 14 ),
( 55 , 14 ),
( 56 , 14 ),
( 57 , 14 ),
( 40 , 15 ),
( 41 , 15 ),
( 42 , 15 ),
( 44 , 15 ),
( 56 , 15 ),
( 57 , 15 ),
( 40 , 16 ),
( 41 , 16 ),
( 42 , 16 ),
( 30 , 17 ),
( 41 , 17 ),
( 42 , 17 ),
( 43 , 17 ),
( 49 , 17 ),
( 54 , 17 ),
( 39 , 18 ),
( 40 , 18 ),
( 41 , 18 ),
( 42 , 18 ),
( 43 , 18 ),
( 50 , 18 ),
( 19 , 19 ),
( 34 , 19 ),
( 43 , 19 ),
( 50 , 19 ),
( 54 , 19 ),
( 55 , 19 ),
( 63 , 19 ),
( 28 , 20 ),
( 42 , 20 ),
( 62 , 20 ),
( 28 , 21 ),
( 36 , 21 ),
( 37 , 21 ),
( 49 , 21 ),
( 50 , 21 ),
( 22 , 22 ),
( 33 , 22 ),
( 22 , 23 ),
( 24 , 23 ),
( 25 , 23 ),
( 41 , 23 ),
( 42 , 23 ),
( 43 , 23 ),
( 54 , 23 ),
( 22 , 24 ),
( 25 , 24 ),
( 34 , 24 ),
( 41 , 24 ),
( 50 , 24 ),
( 20 , 25 ),
( 22 , 25 ),
( 30 , 25 ),
( 34 , 25 ),
( 41 , 25 ),
( 50 , 25 ),
( 54 , 25 ),
( 34 , 26 ),
( 40 , 26 ),
( 61 , 26 ),
( 16 , 27 ),
( 40 , 27 ),
( 47 , 27 ),
( 58 , 27 ),
( 16 , 28 ),
( 19 , 28 ),
( 30 , 28 ),
( 31 , 28 ),
( 39 , 28 ),
( 40 , 28 ),
( 45 , 28 ),
( 46 , 28 ),
( 47 , 28 ),
( 51 , 28 ),
( 58 , 28 ),
( 64 , 28 ),
( 67 , 28 ),
( 19 , 29 ),
( 27 , 29 ),
( 30 , 29 ),
( 31 , 29 ),
( 34 , 29 ),
( 45 , 29 ),
( 51 , 29 ),
( 62 , 29 ),
( 63 , 29 ),
( 64 , 29 ),
( 67 , 29 ),
( 23 , 30 ),
( 24 , 30 ),
( 30 , 30 ),
( 31 , 30 ),
( 35 , 30 ),
( 45 , 30 ),
( 70 , 30 ),
( 18 , 31 ),
( 29 , 31 ),
( 30 , 31 ),
( 32 , 31 ),
( 34 , 31 ),
( 35 , 31 ),
( 36 , 31 ),
( 37 , 31 ),
( 43 , 31 ),
( 61 , 31 ),
( 62 , 31 ),
( 63 , 31 ),
( 18 , 32 ),
( 30 , 32 ),
( 33 , 32 ),
( 34 , 32 ),
( 41 , 32 ),
( 42 , 32 ),
( 43 , 32 ),
( 61 , 32 ),
( 62 , 32 ),
( 70 , 32 ),
( 22 , 33 ),
( 30 , 33 ),
( 34 , 33 ),
( 41 , 33 ),
( 42 , 33 ),
( 44 , 33 ),
( 58 , 33 ),
( 21 , 34 ),
( 32 , 34 ),
( 38 , 34 ),
( 58 , 34 ),
( 59 , 34 ),
( 21 , 35 ),
( 31 , 35 ),
( 36 , 35 ),
( 42 , 35 ),
( 65 , 35 ),
( 31 , 36 ),
( 44 , 36 ),
( 50 , 36 ),
( 65 , 36 ),
( 29 , 37 ),
( 31 , 37 ),
( 33 , 37 ),
( 40 , 37 ),
( 53 , 37 ),
( 57 , 37 ),
( 61 , 37 ),
( 65 , 37 ),
( 24 , 38 ),
( 26 , 38 ),
( 27 , 38 ),
( 49 , 38 ),
( 61 , 38 ),
( 64 , 38 ),
( 26 , 39 ),
( 27 , 39 ),
( 28 , 39 ),
( 36 , 39 ),
( 37 , 39 ),
( 39 , 39 ),
( 40 , 39 ),
( 45 , 39 ),
( 48 , 39 ),
( 65 , 39 ),
( 66 , 39 ),
( 68 , 39 ),
( 71 , 39 ),
( 17 , 40 ),
( 18 , 40 ),
( 27 , 40 ),
( 35 , 40 ),
( 36 , 40 ),
( 37 , 40 ),
( 39 , 40 ),
( 40 , 40 ),
( 48 , 40 ),
( 52 , 40 ),
( 66 , 40 ),
( 71 , 40 ),
( 8 , 41 ),
( 17 , 41 ),
( 18 , 41 ),
( 51 , 41 ),
( 55 , 41 ),
( 69 , 41 ),
( 8 , 42 ),
( 38 , 42 ),
( 43 , 42 ),
( 44 , 42 ),
( 46 , 42 ),
( 48 , 42 ),
( 60 , 42 ),
( 62 , 42 ),
( 70 , 42 ),
( 9 , 43 ),
( 20 , 43 ),
( 30 , 43 ),
( 31 , 43 ),
( 32 , 43 ),
( 38 , 43 ),
( 51 , 43 ),
( 53 , 43 ),
( 72 , 43 ),
( 73 , 43 ),
( 31 , 44 ),
( 38 , 44 ),
( 47 , 44 ),
( 51 , 44 ),
( 53 , 44 ),
( 58 , 44 ),
( 64 , 44 ),
( 66 , 44 ),
( 67 , 44 ),
( 72 , 44 ),
( 73 , 44 ),
( 74 , 44 ),
( 8 , 45 ),
( 9 , 45 ),
( 38 , 45 ),
( 47 , 45 ),
( 48 , 45 ),
( 50 , 45 ),
( 51 , 45 ),
( 57 , 45 ),
( 63 , 45 ),
( 74 , 45 ),
( 25 , 46 ),
( 38 , 46 ),
( 39 , 46 ),
( 45 , 46 ),
( 50 , 46 ),
( 57 , 46 ),
( 59 , 46 ),
( 60 , 46 ),
( 61 , 46 ),
( 63 , 46 ),
( 64 , 46 ),
( 65 , 46 ),
( 68 , 46 ),
( 23 , 47 ),
( 44 , 47 ),
( 63 , 47 ),
( 7 , 48 ),
( 24 , 48 ),
( 26 , 48 ),
( 38 , 48 ),
( 62 , 48 ),
( 63 , 48 ),
( 65 , 48 ),
( 33 , 49 ),
( 38 , 49 ),
( 39 , 49 ),
( 45 , 49 ),
( 48 , 49 ),
( 50 , 49 ),
( 17 , 50 ),
( 18 , 50 ),
( 30 , 50 ),
( 33 , 50 ),
( 37 , 50 ),
( 41 , 50 ),
( 43 , 50 ),
( 44 , 50 ),
( 46 , 50 ),
( 47 , 50 ),
( 48 , 50 ),
( 74 , 50 ),
( 84 , 50 ),
( 23 , 51 ),
( 28 , 51 ),
( 36 , 51 ),
( 38 , 51 ),
( 39 , 51 ),
( 40 , 51 ),
( 43 , 51 ),
( 45 , 51 ),
( 46 , 51 ),
( 47 , 51 ),
( 62 , 51 ),
( 63 , 51 ),
( 68 , 51 ),
( 83 , 51 ),
( 84 , 51 ),
( 23 , 52 ),
( 34 , 52 ),
( 35 , 52 ),
( 36 , 52 ),
( 39 , 52 ),
( 47 , 52 ),
( 59 , 52 ),
( 67 , 52 ),
( 68 , 52 ),
( 82 , 52 ),
( 83 , 52 ),
( 22 , 53 ),
( 23 , 53 ),
( 25 , 53 ),
( 33 , 53 ),
( 34 , 53 ),
( 35 , 53 ),
( 44 , 53 ),
( 68 , 53 ),
( 70 , 53 ),
( 71 , 53 ),
( 20 , 54 ),
( 22 , 54 ),
( 23 , 54 ),
( 29 , 54 ),
( 36 , 54 ),
( 50 , 54 ),
( 63 , 54 ),
( 67 , 54 ),
( 68 , 54 ),
( 69 , 54 ),
( 70 , 54 ),
( 71 , 54 ),
( 72 , 54 ),
( 73 , 54 ),
( 79 , 54 ),
( 20 , 55 ),
( 28 , 55 ),
( 35 , 55 ),
( 38 , 55 ),
( 39 , 55 ),
( 41 , 55 ),
( 69 , 55 ),
( 70 , 55 ),
( 72 , 55 ),
( 74 , 55 ),
( 75 , 55 ),
( 78 , 55 ),
( 25 , 56 ),
( 31 , 56 ),
( 32 , 56 ),
( 33 , 56 ),
( 38 , 56 ),
( 40 , 56 ),
( 42 , 56 ),
( 43 , 56 ),
( 44 , 56 ),
( 58 , 56 ),
( 66 , 56 ),
( 69 , 56 ),
( 78 , 56 ),
( 23 , 57 ),
( 24 , 57 ),
( 25 , 57 ),
( 26 , 57 ),
( 35 , 57 ),
( 39 , 57 ),
( 41 , 57 ),
( 43 , 57 ),
( 44 , 57 ),
( 45 , 57 ),
( 48 , 57 ),
( 66 , 57 ),
( 67 , 57 ),
( 69 , 57 ),
( 70 , 57 ),
( 71 , 57 ),
( 24 , 58 ),
( 37 , 58 ),
( 38 , 58 ),
( 39 , 58 ),
( 40 , 58 ),
( 44 , 58 ),
( 69 , 58 ),
( 70 , 58 ),
( 76 , 58 ),
( 82 , 58 ),
( 23 , 59 ),
( 34 , 59 ),
( 37 , 59 ),
( 38 , 59 ),
( 39 , 59 ),
( 42 , 59 ),
( 47 , 59 ),
( 52 , 59 ),
( 65 , 59 ),
( 70 , 59 ),
( 6 , 60 ),
( 18 , 60 ),
( 19 , 60 ),
( 20 , 60 ),
( 21 , 60 ),
( 22 , 60 ),
( 23 , 60 ),
( 24 , 60 ),
( 31 , 60 ),
( 32 , 60 ),
( 43 , 60 ),
( 5 , 61 ),
( 10 , 61 ),
( 19 , 61 ),
( 21 , 61 ),
( 22 , 61 ),
( 23 , 61 ),
( 35 , 61 ),
( 37 , 61 ),
( 40 , 61 ),
( 42 , 61 ),
( 48 , 61 ),
( 49 , 61 ),
( 64 , 61 ),
( 76 , 61 ),
( 8 , 62 ),
( 9 , 62 ),
( 17 , 62 ),
( 18 , 62 ),
( 21 , 62 ),
( 22 , 62 ),
( 23 , 62 ),
( 37 , 62 ),
( 41 , 62 ),
( 45 , 62 ),
( 46 , 62 ),
( 48 , 62 ),
( 68 , 62 ),
( 4 , 63 ),
( 14 , 63 ),
( 15 , 63 ),
( 16 , 63 ),
( 17 , 63 ),
( 18 , 63 ),
( 22 , 63 ),
( 27 , 63 ),
( 28 , 63 ),
( 32 , 63 ),
( 43 , 63 ),
( 47 , 63 ),
( 68 , 63 ),
( 2 , 64 ),
( 14 , 64 ),
( 15 , 64 ),
( 17 , 64 ),
( 18 , 64 ),
( 20 , 64 ),
( 23 , 64 ),
( 26 , 64 ),
( 29 , 64 ),
( 39 , 64 ),
( 42 , 64 ),
( 43 , 64 ),
( 44 , 64 ),
( 45 , 64 ),
( 58 , 64 ),
( 2 , 65 ),
( 10 , 65 ),
( 14 , 65 ),
( 26 , 65 ),
( 27 , 65 ),
( 37 , 65 ),
( 38 , 65 ),
( 39 , 65 ),
( 43 , 65 ),
( 47 , 65 ),
( 57 , 65 ),
( 58 , 65 ),
( 68 , 65 ),
( 2 , 66 ),
( 5 , 66 ),
( 6 , 66 ),
( 23 , 66 ),
( 27 , 66 ),
( 36 , 66 ),
( 37 , 66 ),
( 45 , 66 ),
( 46 , 66 ),
( 48 , 66 ),
( 57 , 66 ),
( 58 , 66 ),
( 73 , 66 ),
( 18 , 67 ),
( 23 , 67 ),
( 31 , 67 ),
( 33 , 67 ),
( 34 , 67 ),
( 37 , 67 ),
( 40 , 67 ),
( 45 , 67 ),
( 46 , 67 ),
( 53 , 67 ),
( 28 , 68 ),
( 32 , 68 ),
( 33 , 68 ),
( 34 , 68 ),
( 35 , 68 ),
( 37 , 68 ),
( 40 , 68 ),
( 44 , 68 ),
( 45 , 68 ),
( 46 , 68 ),
( 18 , 69 ),
( 21 , 69 ),
( 26 , 69 ),
( 31 , 69 ),
( 32 , 69 ),
( 33 , 69 ),
( 34 , 69 ),
( 35 , 69 ),
( 36 , 69 ),
( 37 , 69 ),
( 38 , 69 ),
( 46 , 69 ),
( 49 , 69 ),
( 50 , 69 ),
( 51 , 69 ),
( 78 , 69 ),
( 24 , 70 ),
( 31 , 70 ),
( 32 , 70 ),
( 33 , 70 ),
( 34 , 70 ),
( 35 , 70 ),
( 36 , 70 ),
( 37 , 70 ),
( 38 , 70 ),
( 41 , 70 ),
( 42 , 70 ),
( 44 , 70 ),
( 45 , 70 ),
( 59 , 70 ),
( 32 , 71 ),
( 36 , 71 ),
( 37 , 71 ),
( 38 , 71 ),
( 40 , 71 ),
( 41 , 71 ),
( 42 , 71 ),
( 43 , 71 ),
( 44 , 71 ),
( 45 , 71 ),
( 20 , 72 ),
( 39 , 72 ),
( 40 , 72 ),
( 41 , 72 ),
( 42 , 72 ),
( 16 , 73 ),
( 21 , 73 ),
( 23 , 73 ),
( 31 , 73 ),
( 32 , 73 ),
( 39 , 73 ),
( 40 , 73 ),
( 41 , 73 ),
( 43 , 73 ),
( 44 , 73 ),
( 45 , 73 ),
( 17 , 74 ),
( 18 , 74 ),
( 41 , 74 ),
( 42 , 74 ),
( 49 , 74 ),
( 19 , 75 ),
( 21 , 75 ),
( 23 , 75 ),
( 34 , 75 ),
( 40 , 75 ),
( 18 , 76 ),
( 21 , 76 ),
( 22 , 76 ),
( 24 , 76 ),
( 25 , 76 ),
( 37 , 76 ),
( 41 , 76 ),
( 34 , 77 ),
( 43 , 77 ),
( 74 , 77 ),
( 29 , 78 ),
( 47 , 78 ),
( 28 , 79 ),
( 29 , 79 ),
( 35 , 79 ),
( 39 , 79 ),
( 42 , 79 ),
( 43 , 79 ),
( 44 , 79 ),
( 47 , 79 ),
( 61 , 79 ),
( 64 , 79 ),
( 71 , 79 ),
( 72 , 79 ),
( 28 , 80 ),
( 34 , 80 ),
( 35 , 80 ),
( 36 , 80 ),
( 37 , 80 ),
( 38 , 80 ),
( 39 , 80 ),
( 40 , 80 ),
( 41 , 80 ),
( 43 , 80 ),
( 28 , 81 ),
( 35 , 81 ),
( 36 , 81 ),
( 37 , 81 ),
( 38 , 81 ),
( 39 , 81 ),
( 40 , 81 ),
( 22 , 82 ),
( 24 , 82 ),
( 27 , 82 ),
( 28 , 82 ),
( 42 , 82 ),
( 43 , 82 ),
( 31 , 83 ),
( 42 , 83 ),
( 43 , 83 ),
( 17 , 84 ),
( 27 , 84 ),
( 34 , 84 ),
( 39 , 84 ),
( 40 , 84 ),
( 25 , 85 ),
( 39 , 85 ),
( 42 , 85 ),
( 26 , 86 ),
( 36 , 86 ),
( 46 , 86 ),
( 48 , 86 ),
( 17 , 87 ),
( 31 , 87 ),
( 32 , 87 ),
( 35 , 87 ),
( 36 , 87 ),
( 37 , 87 ),
( 46 , 87 ),
( 60 , 87 ),
( 17 , 88 ),
( 18 , 88 ),
( 26 , 88 ),
( 27 , 88 ),
( 32 , 88 ),
( 35 , 88 ),
( 36 , 88 ),
( 37 , 88 ),
( 56 , 88 ),
( 17 , 89 ),
( 18 , 89 ),
( 21 , 89 ),
( 22 , 89 ),
( 26 , 89 ),
( 27 , 89 ),
( 26 , 90 ),
( 27 , 90 ),
( 34 , 90 ),
( 35 , 90 ),
( 36 , 90 ),
( 18 , 91 ),
( 40 , 92 ),
( 42 , 92 ),
( 54 , 92 ),
( 45 , 93 ),
( 25 , 94 ),
( 35 , 94 ),
( 36 , 94 ),
( 37 , 94 ),
( 44 , 94 ),
( 25 , 95 ),
( 36 , 95 ),
( 37 , 95 ),
( 52 , 95 ),
( 52 , 96 ),
( 46 , 97 ),
( 51 , 97 ),
( 52 , 97 ),
( 30 , 100 ),
( 31 , 100 ),
( 20 , 101 ),
( 30 , 101 ),
( 31 , 101 )]