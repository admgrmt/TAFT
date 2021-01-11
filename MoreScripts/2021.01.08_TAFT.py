# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 14:48:21 2021

@author: Adam
"""

import pandas as pd 
import matplotlib.pyplot as plt
from pandas import DataFrame
import numpy as np


# Objective is to create a compilation of the soleus trails and then go through and eliminate the slope


# Import data from integrated file generate in c3d
# Data format will be ASCII
# Import read will be

#old import from seperate document
#df = pd.read_csv ('G:/My Drive/AllExportedVelocityIntegration.txt', engine='python', delimiter='\t', header=1, skiprows=[2,3,4])

#ammended import for needs
df = pd.read_csv ('G:/My Drive/AllExportedVelocityIntegration.txt', engine='python', delimiter='\t', skiprows=[1,2,3,4], header=0)

## level time to the frequency of collection (in this case. 148.148)

df['Unnamed: 0'] = df['Unnamed: 0'] 

## small rename label for index 1

df=df.rename(columns = {'Unnamed: 0':'Time'})

##Rename dataframe unnnamed to time

df

import os
import os.path
file_list = os.listdir("G:/My Drive/Adam_G_Thesis/4_Data/Pilot/Raw_data/Raw_EMG_Data/2020.11.16.TAFTPilot/Footswitch_Signals")

# Remove from list

#=============================================
# ## Example code

# # animals list
# animals = ['cat', 'dog', 'rabbit', 'guinea pig']

# # 'rabbit' is removed
# animals.remove('rabbit')

# # Updated animals List
# print('Updated animals list: ', animals)
#=============================================

print(file_list)

file_list.remove('desktop.ini')
file_list.remove('TAFT_P5_180_5_x_30_sec_Rep_6.15_148_1481Hz.c3d')
file_list.remove('TAFT_P5_180_5_x_30_sec_Rep_5.14_148_1481Hz.c3d')

print(file_list)

for names in file_list:
        df.plot(x = "Time", y = names, kind = 'scatter', s=2.00)
        plt.show()	
        print(names)

#====================================================================
## make line of best fit for one datapoint or something
#x = np.array([1, 2, 3, 4])
# y = np.array([1, 2, 3, 4 ])
# m, b = np.polyfit(x, y, 1)
# print(m)
# print(b)

# plt.plot(x, y, 'o')
# plt.plot(x, m*x + b)
#====================================================================

rep_name='TAFT_P5_6x4_5_x_30_sec_Rep_5.9_148_1481Hz.c3d'

x = np.array(df.iloc[:]['Time'])
y = np.array(df.iloc[:][rep_name])
m, b = np.polyfit(x, y, 1)
print(m)
print(b)

plt.plot(x, y, 'o')
plt.plot(x, m*x + b)

#complete
#================
# want to create a series of points to mimic the slope for the amount of points in the data index

# get a count for the amount in the data
temp_number=df[rep_name].shape
temp_number=temp_number[0]
#extract tupple from integer
#make index addition
#generate list then add to dataframe

slope_points = []
index_range=range(0, temp_number)

value1=0

for i in index_range:
   if i > 0 :
       value1 = m + value1
       slope_points.append(value1)
   else :
       value1 = b
       slope_points.append(value1)

d = pd.DataFrame()
d['Slope_Points'] = slope_points
d['Time']=df.iloc[0:temp_number]['Time']


#plotting with mulitple dataframes
ax = d.plot(x = 'Time', y = 'Slope_Points', kind = 'scatter', s=1.00) 
df.plot(ax=ax, x = 'Time', y = rep_name, kind = 'scatter', s=1.00)

plt.show()	


# Best fit line complete