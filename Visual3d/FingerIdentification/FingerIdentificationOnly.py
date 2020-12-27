# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 12:06:30 2020

@author: Adam
"""

###=====================================
#Loading Libraries
###=====================================

import neurokit2 as nk
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame


###================================================================
#df = pd.read_csv ('ACC1LA_70deg.csv',delimiter='comma', header=0, engine="python")
# reading all the data from the accelration file for this one trial
# \t is a text import with \tab delimiter
###================================================================

df = pd.read_csv ('C:/Users/Adam/Drive/Coding/GitRepos/Thesis_TAFT/Visual3d/FingerIdentification/ACC_FP Data/LA_113Deg_01ACCFP3.txt', engine='python', delimiter='\t', header=1, skiprows=[2,3,4])

count_row = len(df.index)  # gives number of row count
count_col = df.shape[1]  # gives number of col count


###================================================================
# the next step will be to integrate this data
# generatiing a new dataframe that excludes force data
###================================================================

df2 = df.iloc[0:count_row, 1:count_col]


###================================================================
#picking a sensor to integrate and graph from the data
# this currrent senso: "Sensor 6 Acc.ACCY6" is RBF 
###================================================================

Sensor = "Sensor 6 Acc.ACCY6"

###================================================================
# inserting formula with integration 
# attempting to make new column of data for integration of each signal
#inserts a blank data frame for the integrated values of acc=constant, velocity, and position
###================================================================
df2.insert(24, Sensor + " Constant", 0)
df2.insert(25, Sensor + " Velocity", 0)
df2.insert(26,  Sensor + " Position", 0)

# df2[Sensor + " Constant"] = df2[Sensor].subtract(df2.iloc[0][Sensor])
df2[Sensor + " Constant"] = df2[Sensor].subtract(0)


###================================================================
# creates a function to integrate a column of values on a 1 m/s change  
# this particular function was to integrate acceleration into "average velocity" on 1 m/s interval    
###================================================================

def avg_integrate_velocity (value):
    fin_value = 1
    init_value= 0
    change_output = 0
    while fin_value <= value:
        change_output = ((((df2.loc[fin_value][Sensor + " Constant"] + df2.loc[init_value][Sensor + ' Constant'])/2)*1) + change_output)
        df2.loc[fin_value, Sensor + ' Velocity'] = change_output
        fin_value = fin_value + 1
        init_value = init_value + 1
        #print(change_output)
    return change_output

avg_integrate_velocity(count_row-1) 


###=====================================
### going to try and integrate velocity data to positional data
###=====================================

# manipulating earlier function to apply velocity values for the change - making new function
def avg_integrate_position (value):
    fin_value = 1
    init_value= 0
    change_output = 0
    while fin_value <= value:
        change_output = ((((df2.loc[fin_value][Sensor + ' Velocity'] + df2.loc[init_value][Sensor + ' Velocity'])/2)*1) + change_output)
        df2.loc[fin_value, Sensor + ' Position'] = change_output
        fin_value = fin_value + 1
        init_value = init_value + 1
        #print(change_output)
    return change_output

avg_integrate_position(count_row-1)

###=====================================
#detecting events from forceplate and plott
###=====================================

y2 = df['Force.Fy3']
emg_cleaned = nk.emg_clean(y2)
emg_amplitude = nk.emg_amplitude(emg_cleaned)
activity, info = nk.emg_activation(emg_amplitude=emg_amplitude, method="threshold", threshold=.5)

# fig = nk.events_plot([info["EMG_Offsets"], info["EMG_Onsets"]], emg_cleaned)
# fig


onset_values = info.get('EMG_Onsets')
offset_values = info.get('EMG_Offsets')
print(onset_values)
print (offset_values)


your_list = onset_values
Onset_Values = DataFrame(your_list,columns=['Onset Values'])
your_list = onset_values
Offset_Values = DataFrame(your_list,columns=['Offset Values'])

Onset_Values_Range = Onset_Values - 300 
Offset_Values_Range = Offset_Values + 300 


### ===========================
### Test graph for acceleration function
### ===========================

Time = df['Unnamed: 0']
ACC = df2[Sensor + ' Constant']
FP3 = df['Force.Fy3']


### If we would like to hone in on a Force Peak ||| grab appropriate index or peak# from onset/offset
### Replace Graph Values wiith .iloc of Temo1:Temo2 set for index
### Replace for Constant, Velocity, Position

# Temo1 = Onset_Values_Range.iloc[0]['Onset Values']
# Temo2 = Offset_Values_Range.iloc[0]['Offset Values']

# i.e. 

# GraphDFTime = Time.iloc[Temo1:Temo2]
# GraphDFACCX1 = ACCX1.iloc[Temo1:Temo2]
# GraphDFFP3 = FP3.iloc[Temo1:Temo2]


GraphDFTime = Time.iloc[1:count_row]
GraphDFACCX1 = ACC.iloc[1:count_row]
GraphDFFP3 = FP3.iloc[1:count_row]

print (GraphDFACCX1)

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')

ax1.set_xlabel('Time')
ax1.set_ylabel(Sensor + ' Acceleration', color='black')
ax2.set_ylabel('FP3 Y Axis', color='black')


plt.show ()


### ==========================
### Test graph for velocity
### ==========================


Time = df['Unnamed: 0']
ACC = df2[Sensor + ' Velocity']
FP3 = df['Force.Fy3']

Temo1 = Onset_Values_Range.iloc[0]['Onset Values']
Temo2 = Offset_Values_Range.iloc[0]['Offset Values']

GraphDFTime = Time.iloc[1:count_row]
GraphDFACCX1 = ACC.iloc[1:count_row]
GraphDFFP3 = FP3.iloc[1:count_row]


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')

ax1.set_xlabel('Time')
ax1.set_ylabel(Sensor + ' Velocity', color='black')
ax2.set_ylabel('FP3 Y Axis', color='black')


plt.show ()

### ===========================
### Test graph for position function
### ===========================

Time = df['Unnamed: 0']
ACC = df2[Sensor + ' Position']
FP3 = df['Force.Fy3']

Temo1 = Onset_Values_Range.iloc[0]['Onset Values']
Temo2 = Offset_Values_Range.iloc[0]['Offset Values']

GraphDFTime = Time.iloc[1:count_row]
GraphDFACCX1 = ACC.iloc[1:count_row]
GraphDFFP3 = FP3.iloc[1:count_row]


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')

ax1.set_xlabel('Time')
ax1.set_ylabel(Sensor + ' Position', color='black')
ax2.set_ylabel('FP3', color='black')


plt.show ()
