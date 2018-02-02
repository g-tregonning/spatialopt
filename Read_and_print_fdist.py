# -*- coding: utf-8 -*-
"""
Module to read the values for fdist from csv and print them
"""
import numpy as np


Data_folder  = "C:/Users/a8093548/PhD/Python_Codes/Data/London/"
fdist_list = np.loadtxt(Data_folder+"fdist_values_Available.txt",delimiter=";")

f = open(Data_folder+"fdist_values_Available_output.txt", 'w') # or 'w'?

for element in fdist_list:

    f.write("(("+str(element[0])+","+str(element[1])+"),"+str(element[2])+"),\n")


f.close()