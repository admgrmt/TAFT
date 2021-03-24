# -*- coding: utf-8 -*-
"""
@author: Adam
Written 1/26/2021

For use with K4B2 data export and "New_Metabolic_Analysis"

Made to convert K4B2 xlsx file to a importable "parvo formatted" xls sheet.
Automating copy and paste...
"""

import pandas as pd 
from tkinter import filedialog as fd 
import numpy as np

#Imports in the MatlabFile
print("Please choose the 'Template_MATLAB.xls' file -- should be in same folder")
path=fd.askopenfilename() 
df_MATLAB = pd.read_excel(path)

#ask for path and places that in name variable
#imports in the K4b2 File (user will need to read in appropriate file)
print("Please pick the K4B2 file that you would like to transcribe")
print("*** File must be '.xls extension' ***")
path=fd.askopenfilename() 
df_original = pd.read_excel(path)

#duplicating matlab data frame
New_MATLAB = df_MATLAB

#importing time frame volume to MATLAB (currently named REM_05_MATLAB)
temp_count= df_original['t'].shape
#print("this is how long time is for K4B2")
#print(temp_count)

temp_count = temp_count[0] - 2
#this is the entire data index. 2:tempcount

#makes values into a list
original_list = df_original['t'][2:].values.tolist()

New_MATLAB = New_MATLAB.append(pd.DataFrame(original_list, columns=['Humboldt State University']), ignore_index=True)
##That fucking worked so far...

temp_count_MAT=temp_count + 29
data = New_MATLAB['Humboldt State University'][29:temp_count_MAT].tolist()

# Go through each time in column and append...

#declare an empty list

time_list = [] 

for time in data:
    t = time
    (h, m, s) = t.split(':')
    result = int(h) * 3600 + int(m) * 60 + int(s)
    result = result / 60
    # append to a list
    time_list.append(result)

#clean things up
del t, h, m, s, result, time

#import list into proper location
New_MATLAB['Humboldt State University'][29:temp_count_MAT] = time_list

#clean things up
del data, time_list

#=========================================================
#import V02
original_list = df_original['VO2'][2:].values.tolist()
### do not want to use append again because it will end onto the end of the NAN... 
### now we just need to ILOC AND REPLACE.

#Need temp count, then need to extract out tupple to int.
temp_count = New_MATLAB['Humboldt State University'].shape
temp_count = temp_count[0] 

#replace
New_MATLAB['Unnamed: 1'][29:temp_count_MAT] = original_list
# change mL values to L
New_MATLAB['Unnamed: 1'][29:temp_count_MAT] = New_MATLAB['Unnamed: 1'][29:temp_count_MAT] *0.001
#===============================================
### now we repeat what will later be itterated.

original_list = df_original['VO2/Kg'][2:].values.tolist()
New_MATLAB['Unnamed: 2'][29:temp_count_MAT] = original_list

#===============================================

original_list = df_original['METS'][2:].values.tolist()
New_MATLAB['Unnamed: 3'][29:temp_count_MAT] = original_list

#===============================================

original_list = df_original['VCO2'][2:].values.tolist()
New_MATLAB['Unnamed: 4'][29:temp_count_MAT] = original_list

#change mL values to L
New_MATLAB['Unnamed: 4'][29:temp_count_MAT] = New_MATLAB['Unnamed: 1'][29:temp_count_MAT] *0.001
#===============================================

original_list = df_original['VE'][2:].values.tolist()
New_MATLAB['Unnamed: 5'][29:temp_count_MAT] = original_list

#===============================================

original_list = df_original['R'][2:].values.tolist()
New_MATLAB['Unnamed: 6'][29:temp_count_MAT] = original_list

###
tempdf = pd.DataFrame([[np.NaN] * len(New_MATLAB.columns)], columns=New_MATLAB.columns)
New_MATLAB = tempdf.append(New_MATLAB, ignore_index=True)
New_MATLAB.iloc[0][0] = 'Humboldt State University'

#===============================================
## Finished import up to RR....
#### filling in with zeros for now.

New_MATLAB["Unnamed: 7"][29:temp_count_MAT] = 0
New_MATLAB["Unnamed: 8"][29:temp_count_MAT] = 0
New_MATLAB["Unnamed: 9"][29:temp_count_MAT] = 0
New_MATLAB["Unnamed: 10"][29:temp_count_MAT] = 0
New_MATLAB["Unnamed: 11"][29:temp_count_MAT] = 0
New_MATLAB["Unnamed: 12"][29:temp_count_MAT] = 0
New_MATLAB["Unnamed: 13"][29:temp_count_MAT] = 0
##=============================================
# now want to export / write back to xlsx file.

import os
import pandas as pd

#checks current directory
os.getcwd()

#user file dialogue to change directory
print("Where would you like to save your file?")
folderpath = fd.askdirectory()
os.chdir(folderpath) #updates directory to user input string

#ask for user input
print("=================================================")
print("")
print("If you receive an access error, ensure that the file is not already open")
print("")
print("")

print("Do not include spaces after the prompt below")
print("*** Program will close after file is named ***")
print("")
user_input = input('What would you like to name your file? \nTYPE HERE:')
user_input = user_input + ".xls"

writer = pd.ExcelWriter(user_input)
New_MATLAB.to_excel(writer,'Sheet1', header=False, index=False)
writer.save()
