# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 19:02:14 2020

@author: desmo
"""

import csv
import os

path = 'C:/Users/desmo/Desktop/NTU/dsp/assignment 2/'

count = 0

        
file1 = open(r'C:\Users\desmo\Desktop\NTU\dsp\assignment 2\region.csv', 'r') 
file2 = open(r'C:\Users\desmo\Desktop\NTU\dsp\assignment 2\dataset\formatted\region.csv', 'w') 

Lines = file1.readlines() 
for line in Lines: 
    print(line[:-2])
    file2.writelines(line[:-2] +"\n") 
    #file2.writelines(line.trim()[:-1])  
file1.close()
file2.close()

import glob
for filename in glob.glob('C:/Users/desmo/Desktop/NTU/dsp/assignment 2/dataset/original/*.csv'):
    file1 = open(filename, 'r') 
    csvname = filename.split('\\')[1]
    file2 = open('C:/Users/desmo/Desktop/NTU/dsp/assignment 2/dataset/formatted/'+csvname, 'w') 
    Lines = file1.readlines() 
    for line in Lines: 
        file2.writelines(line[:-2] +"\n") 
    file1.close()
    file2.close()



                          