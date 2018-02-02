# -*- coding: utf-8 -*-
"""
Testing the ability to save a file as a lookup and import the lookup table from
it. 

Two ideas:
    1 Generate the lookup array and save it a .py file
        ~ Would require me to save it as "Lookup = ", lookuparray
    2 Save the lookup array to a .txt file and load it each time
    
Considerations:
    @ Am I gonna have to wipe the file first
"""
import numpy as np

raster = np.array([[0,1],[1,0],[1,1]])


lookup = [(1,1),(1,2),(1,3)]
PTAL = ["Ptal", 80.0]
Dwell = ["Dwell_Totals", 90]


np.savetxt("lookup.txt", lookup,  delimiter=',', newline='\n')
np.savetxt("PTAL.txt", PTAL,  delimiter=',', newline='\n', fmt="%s")



data = (np.loadtxt("lookup.txt",delimiter=",")).tolist()
PTAL_Cons = (np.loadtxt("PTAL.txt",delimiter=",",fmt="%s"))#.tolist()


print PTAL_Cons