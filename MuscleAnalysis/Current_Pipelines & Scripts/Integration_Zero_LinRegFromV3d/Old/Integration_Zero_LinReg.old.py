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
# Import read will be "csv"

#old import from seperate document
#df = pd.read_csv ('G:/My Drive/AllExportedVelocityIntegration.txt', engine='python', delimiter='\t', header=1, skiprows=[2,3,4])


#import with all headers and rows
df_original = pd.read_csv ('G:/My Drive/Coding/GitRepos/Thesis_TAFT/MoreScripts/AllExportedVelocityIntegration.txt', delimiter='\t')
df_original = df_original.iloc[0:4]

#ammended import for needs
df = pd.read_csv ('G:/My Drive/Coding/GitRepos/Thesis_TAFT/MoreScripts/AllExportedVelocityIntegration.txt', delimiter='\t', skiprows=[1,2,3,4], header=0)

## level time to the frequency of collection (in this case. 148.148)

df['Unnamed: 0'] = df['Unnamed: 0'] 

## small rename label for index 1

df=df.rename(columns = {'Unnamed: 0':'Time'})

### fill NaN with Zeros.....

#df = df[:].fillna(0)

##Rename dataframe unnnamed to time

import os
import os.path
file_list = os.listdir("G:/My Drive/Adam_G_Thesis/4_Data/3. Pilot/Raw_data/Raw_EMG_Data/2020.11.16.TAFTPilot/Footswitch_Signals")

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

# print(file_list) CHECK

file_list.remove('desktop.ini')
file_list.remove('TAFT_P5_180_5_x_30_sec_Rep_6.15_148_1481Hz.c3d')
file_list.remove('TAFT_P5_180_5_x_30_sec_Rep_5.14_148_1481Hz.c3d')

print("these are the files that I will run the plotting through")
print(file_list)
# print(df.iloc[0])
"""
for names in file_list:
        df.plot(x = "Time", y = names, kind = 'scatter', s=2.00)
        plt.show()	
        # print(names) CHECK
"""
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

print( file_list)

#create a zerod dataframe globally.
zerod = df.copy()

for rep_name in file_list:
    print(rep_name)
     
    df2 = df[[rep_name, "Time"]].copy()
    #remove NaN
    df2 = df2[:].dropna()
 
    # get a count for the amount in the data
    temp_number=df2[rep_name].shape
    temp_number=temp_number[0]
    #extract tupple from integer
    #make index addition
    #generate list then add to dataframe
    
    x = np.array(df2.iloc[0:temp_number]['Time'])
    y = np.array(df2.iloc[0:temp_number][rep_name])
    m, b = np.polyfit(x, y, 1)
    print("/n This is the slope /n" + rep_name)
    print(m)
    print("/n This is the intercept for /n" + rep_name)
    print(b)
    
    #hiding plot for now because it is fat and ugly
    # plt.plot(x, y, 'o')
    # plt.plot(x, m*x + b)
    
    #complete
    #================
    # want to create a series of points to mimic the slope for the amount of points in the data index
      
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
    d['Time']=df2.iloc[0:temp_number]['Time']
    
    
    #plotting with mulitple dataframes
    ax = d.plot(x = 'Time', y = 'Slope_Points', kind = 'scatter', s=1.00) 
    df2.plot(ax=ax, x = 'Time', y = rep_name, kind = 'scatter', s=1.00)
    
    plt.show()	
    
    
    # Best fit line complete
    
    ## not to just subtract points from best line fit, replace the data, and take me back to zero.
    d['Zerod']= df[rep_name] - d['Slope_Points'] 
    
    
    
    d.plot(x = 'Time', y = 'Zerod', kind = 'scatter', s=1.00) 
    plt.axhline(y=0, color="black", linestyle="--")
    plt.axhline(y=.2, color="red", linestyle="--")
    plt.axhline(y=-.2, color="red", linestyle="--")
    plt.show
    
    
    #copy the data frame to take imports
 
    zerod[rep_name] = d["Zerod"]

# adding to dataframe original. 

zerod.rename(columns={'Time': 'Unnamed: 0'}, inplace=True)
df_original = df_original.append(zerod)

##complete and named apprioriately. 
# df_original is now ready for export to visual 3d

#df_original = pd.read_csv ('G:/My Drive/Coding/GitRepos/Thesis_TAFT/MoreScripts/AllExportedVelocityIntegration.txt', delimiter='\t')
df_original.to_csv('filename.txt', sep='\t', encoding='ascii', index=False)
