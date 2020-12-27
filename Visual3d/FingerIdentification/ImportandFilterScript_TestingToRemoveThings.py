# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 16:25:29 2020
*Modified 7:52PM

@author: Adam
"""

import neurokit2 as nk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame



#df = pd.read_csv ('ACC1LA_70deg.csv',delimiter='comma', header=0, engine="python")
# reading all the data from the accelration file for this one trial
df = pd.read_csv ('C:/Users/Adam/Drive/Coding/GitRepos/Thesis_TAFT/Visual3d/FingerIdentification/ACC_FP Data/SA_70Deg_01 ACCFP3.csv', header=1, skiprows=[2,3,4] )

# the next step will be to integrate this data
##maybe I can just apply filtering through the Biomechanical toolkit

df2 = df.iloc[0:29077, 1:25]

#=============================================================
#### inserting formula with integration 
#### attempting to make new column of data for integration of each signal

#inserts a blank data frame for the integrated values
df2.insert(24, "Sensor 1 Acc.ACCX1 Constant", 0)
df2.insert(25, "Sensor 1 Acc.ACCX1 Velocity", 0)
df2.insert(26, "Sensor 1 Acc.ACCX1 Position", 0)

df2["Sensor 1 Acc.ACCX1 Constant"] = df2["Sensor 1 Acc.ACCX1"].subtract(df2.iloc[0]['Sensor 1 Acc.ACCX1'])

# creates a function to integrate a column of values on a 1 m/s change  
# this particular function was to integrate acceleration into "average velocity" on 1 m/s interval    
def avg_integrate_values (value):
    fin_value = 1
    init_value= 0
    change_output = 0
    while fin_value <= value:
        change_output = ((((df2.loc[fin_value]['Sensor 1 Acc.ACCX1 Constant'] + df2.loc[init_value]['Sensor 1 Acc.ACCX1 Constant'])/2)*1) + change_output)
        df2.loc[fin_value,'Sensor 1 Acc.ACCX1 Velocity'] = change_output
        fin_value = fin_value + 1
        init_value = init_value + 1
        #print(change_output)
    return change_output

avg_integrate_values(29076) 

df2["Sensor 1 Acc.ACCX1 Velocity"] = df2["Sensor 1 Acc.ACCX1 Velocity"].subtract(df2.iloc[0]['Sensor 1 Acc.ACCX1 Velocity'])


###=====================================
### going to try and integrate velocity data to positional data
###=====================================

# manipulating earlier function to apply velocity values for the change - making new function
def avg_integrate_vel_values (value):
    fin_value = 1
    init_value= 0
    change_output = 0
    while fin_value <= value:
        change_output = ((((df2.loc[fin_value]['Sensor 1 Acc.ACCX1 Velocity'] + df2.loc[init_value]['Sensor 1 Acc.ACCX1 Velocity'])/2)*1) + change_output)
        df2.loc[fin_value,'Sensor 1 Acc.ACCX1 Position'] = change_output
        fin_value = fin_value + 1
        init_value = init_value + 1
        #print(change_output)
    return change_output

avg_integrate_vel_values(29076)

df2["Sensor 1 Acc.ACCX1 Position"] = df2["Sensor 1 Acc.ACCX1 Position"].subtract(df2.iloc[0]['Sensor 1 Acc.ACCX1 Position'])

#===================================================
Time = (df['Unnamed: 0'])
S1_ACCX = df['Sensor 1 Acc.ACCX1']
FP3Y = df['Force.Fy3']

"""
Original Code
### plotting figures next to each other
fig = plt.figure()
plt.plot(Time, Y)
plt.xlabel('Time (sec)')
plt.ylabel('EMG or FP Marks')
fig_name = 'fig2.png'
fig.set_size_inches(w=11,h=7)
fig.savefig(fig_name)

print (df['Force.Fy3'])
df['Sensor 1 Acc.ACCX1']
"""

# FULL Graph! 
x = (df['Unnamed: 0'])
y1 = df['Sensor 1 Acc.ACCX1']
y2 = df['Force.Fy3']


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(x, y2, 'g-', linestyle = "--")
ax1.plot(x, y1, 'r-')

ax1.set_xlabel('X data')
ax1.set_ylabel('Y1 data', color='black')
ax2.set_ylabel('Y2 data', color='black')


plt.ylim(9, 10)

plt.show ()


##### Succesful plotting. Now I will want to reduce the dataframes for the events that I would like around FP

"""
#found onset events....
#https://neurokit.readthedocs.io/en/latest/tutorials/Python.html
events = nk.find_events(df['Force.Fy3'], cut="higher")
events
"""
"""
## from neurokit 1_ uninstaled 9:00 10.24.2020
y2.plot
events = nk.find_events(df['Force.Fy3'], cut="lower")
events
"""
### 11:11pm 12.23.2020

"""
### EMG Event Detection
emg = nk.emg_simulate(duration=10, burst_number=3)
emg_cleaned = nk.emg_clean(emg)
emg_amplitude = nk.emg_amplitude(emg_cleaned)

activity, info = nk.emg_activation(emg_amplitude=emg_amplitude, method="threshold")
fig = nk.events_plot([info["EMG_Offsets"], info["EMG_Onsets"]], emg_cleaned)
fig  
"""""

#detecting events from forceplate and plott
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
ACCX1 = df2['Sensor 1 Acc.ACCX1']
FP3 = df['Force.Fy3']

print(ACCX1)

Temo1 = Onset_Values_Range.iloc[0]['Onset Values']
Temo2 = Offset_Values_Range.iloc[0]['Offset Values']

GraphDFTime = Time.iloc[Temo1:Temo2]
GraphDFACCX1 = ACCX1.iloc[Temo1:Temo2]
GraphDFFP3 = FP3.iloc[Temo1:Temo2]


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')

ax1.set_xlabel('Time')
ax1.set_ylabel('Acceleration X', color='black')
ax2.set_ylabel('FP3 Y Axis', color='black')


plt.show ()


### ==========================
### Test graph for velocity
### ==========================


Time = df['Unnamed: 0']
ACCX1 = df2['Sensor 1 Acc.ACCX1 Velocity']
FP3 = df['Force.Fy3']

print(ACCX1)

Temo1 = Onset_Values_Range.iloc[0]['Onset Values']
Temo2 = Offset_Values_Range.iloc[0]['Offset Values']

GraphDFTime = Time.iloc[Temo1:Temo2]
GraphDFACCX1 = ACCX1.iloc[Temo1:Temo2]
GraphDFFP3 = FP3.iloc[Temo1:Temo2]


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')

ax1.set_xlabel('Time')
ax1.set_ylabel('Acceleration X', color='black')
ax2.set_ylabel('FP3 Y Axis', color='black')


plt.show ()

### ===========================
### Test graph for position function
### ===========================

Time = df['Unnamed: 0']
ACCX1 = df2['Sensor 1 Acc.ACCX1 Position']
FP3 = df['Force.Fy3']

print(ACCX1)

Temo1 = Onset_Values_Range.iloc[0]['Onset Values']
Temo2 = Offset_Values_Range.iloc[0]['Offset Values']

GraphDFTime = Time.iloc[Temo1:Temo2]
GraphDFACCX1 = ACCX1.iloc[Temo1:Temo2]
GraphDFFP3 = FP3.iloc[Temo1:Temo2]


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')

ax1.set_xlabel('Time')
ax1.set_ylabel('Acceleration X', color='black')
ax2.set_ylabel('FP3 Y Axis', color='black')


plt.show ()

### ============================
### Index 1
### ==============================

Temo1 = Onset_Values_Range.iloc[0]['Onset Values']
Temo2 = Offset_Values_Range.iloc[0]['Offset Values']

GraphDFTime = Time.iloc[Temo1:Temo2]
GraphDFACCX1 = ACCX1.iloc[Temo1:Temo2]
GraphDFFP3 = FP3.iloc[Temo1:Temo2]


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')

ax1.set_xlabel('Time')
ax1.set_ylabel('Acceleration X', color='black')
ax2.set_ylabel('FP3 Y Axis', color='black')


plt.show ()

###========================
### Beginning original graph index for all 7 repetitions
### =======================

Time = df['Unnamed: 0']
ACCX1 = df2['Sensor 1 Acc.ACCX1 Velocity']
FP3 = df['Force.Fy3']

print(ACCX1)

### ============================
### Index 1
### ==============================

Temo1 = Onset_Values_Range.iloc[0]['Onset Values']
Temo2 = Offset_Values_Range.iloc[0]['Offset Values']

GraphDFTime = Time.iloc[Temo1:Temo2]
GraphDFACCX1 = ACCX1.iloc[Temo1:Temo2]
GraphDFFP3 = FP3.iloc[Temo1:Temo2]


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')

ax1.set_xlabel('Time')
ax1.set_ylabel('Acceleration X', color='black')
ax2.set_ylabel('FP3 Y Axis', color='black')


plt.show ()


### ============================
### Index 2
### ==============================

Temo1 = Onset_Values_Range.iloc[1]['Onset Values']
Temo2 = Offset_Values_Range.iloc[1]['Offset Values']

GraphDFTime = Time.iloc[Temo1:Temo2]
GraphDFACCX1 = ACCX1.iloc[Temo1:Temo2]
GraphDFFP3 = FP3.iloc[Temo1:Temo2]


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')

ax1.set_xlabel('Time')
ax1.set_ylabel('Acceleration X', color='black')
ax2.set_ylabel('FP3 Y Axis', color='black')


plt.show ()


### ============================
### Index 3
### ==============================

Temo1 = Onset_Values_Range.iloc[2]['Onset Values']
Temo2 = Offset_Values_Range.iloc[2]['Offset Values']

GraphDFTime = Time.iloc[Temo1:Temo2]
GraphDFACCX1 = ACCX1.iloc[Temo1:Temo2]
GraphDFFP3 = FP3.iloc[Temo1:Temo2]


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')

ax1.set_xlabel('Time')
ax1.set_ylabel('Acceleration X', color='black')
ax2.set_ylabel('FP3 Y Axis', color='black')


plt.show ()


### ============================
### Index 4
### ============================== 

Temo1 = Onset_Values_Range.iloc[3]['Onset Values']
Temo2 = Offset_Values_Range.iloc[3]['Offset Values']

GraphDFTime = Time.iloc[Temo1:Temo2]
GraphDFACCX1 = ACCX1.iloc[Temo1:Temo2]
GraphDFFP3 = FP3.iloc[Temo1:Temo2]


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')

ax1.set_xlabel('Time')
ax1.set_ylabel('Acceleration X', color='black')
ax2.set_ylabel('FP3 Y Axis', color='black')


plt.show ()


### ============================
### Index 5
### ==============================

Temo1 = Onset_Values_Range.iloc[4]['Onset Values']
Temo2 = Offset_Values_Range.iloc[4]['Offset Values']

GraphDFTime = Time.iloc[Temo1:Temo2]
GraphDFACCX1 = ACCX1.iloc[Temo1:Temo2]
GraphDFFP3 = FP3.iloc[Temo1:Temo2]


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')

ax1.set_xlabel('Time')
ax1.set_ylabel('Acceleration X', color='black')
ax2.set_ylabel('FP3 Y Axis', color='black')


plt.show ()


### ============================
### Index 6
### ==============================

Temo1 = Onset_Values_Range.iloc[5]['Onset Values']
Temo2 = Offset_Values_Range.iloc[5]['Offset Values']

GraphDFTime = Time.iloc[Temo1:Temo2]
GraphDFACCX1 = ACCX1.iloc[Temo1:Temo2]
GraphDFFP3 = FP3.iloc[Temo1:Temo2]


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')

ax1.set_xlabel('Time')
ax1.set_ylabel('Acceleration X', color='black')
ax2.set_ylabel('FP3 Y Axis', color='black')


plt.show ()


### ============================
### Index 7
### ==============================

Temo1 = Onset_Values_Range.iloc[6]['Onset Values']
Temo2 = Offset_Values_Range.iloc[6]['Offset Values']

GraphDFTime = Time.iloc[Temo1:Temo2]
GraphDFACCX1 = ACCX1.iloc[Temo1:Temo2]
GraphDFFP3 = FP3.iloc[Temo1:Temo2]


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')

ax1.set_xlabel('Time')
ax1.set_ylabel('Acceleration X', color='black')
ax2.set_ylabel('FP3 Y Axis', color='black')






