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

##==========================================================
## Automating the process
## This for loop should grab all an acceleration signals for all three of the conditions
## For this pilot EXPLICITLY (could be exanded for other conditions)
##==========================================================

C3x4="C:/Users/Adam/Drive/Adam_G_Thesis/4_Data/Pilot/Raw_data/Raw_EMG_Data/2020.11.16.TAFTPilot/EMG_Signals/TAFT_P5_3x4_5_x_30_sec_Rep_4.3.csv"
C6x4="C:/Users/Adam/Drive/Adam_G_Thesis/4_Data/Pilot/Raw_data/Raw_EMG_Data/2020.11.16.TAFTPilot/EMG_Signals/TAFT_P5_6x4_5_x_30_sec_Rep_5.9.csv"
C180="C:/Users/Adam/Drive/Adam_G_Thesis/4_Data/Pilot/Raw_data/Raw_EMG_Data/2020.11.16.TAFTPilot/EMG_Signals/TAFT_P5_180_5_x_30_sec_Rep_4.13.csv"

##=============================================================
## Setting up the for loop
##=============================================================

filename=[C3x4, C6x4, C180]
for name in filename:
    
    condition = name.lstrip("C:/Users/Adam/Drive/Adam_G_Thesis/4_Data/Pilot/Raw_data/Raw_EMG_Data/2020.11.16.TAFTPilot/EMG_Signals/")
    
    ###================================================================
    #df = pd.read_csv ('ACC1LA_70deg.csv',delimiter='comma', header=0, engine="python")
    # because this file is importing as CSV from the direct emgworks files (portable collection)
    ## we will change the data frame parameters
    ## FP3 will act as one of the footswitches...
    ###================================================================
    
    df = pd.read_csv (name, delimiter=',')
    
    
    ## ALL acc SIGNALS + FS A (R & L) 
    ## Only works from EMG Works
    
    df2 = df.iloc[:, [2,3,5,7,11,13,15,19,21,23,27,29,31,35,37,39,43,45,47,51,53,55,59,61,63,67,69,71,75,77,79,83,85,87,91,93,95,99,101,103,107,109,111,115,123]]
    df2 = df2.iloc[0:4445]
    count_row = len(df2.index)  # gives number of row count
    count_col = df2.shape[1]  # gives number of col count
    
    
    
    
    #Footswitch values are included in the back indexes that I DO NOT want to calculate
    
    ###================================================================
    # the next step will be to integrate this data
    # generatiing a new dataframe that excludes force data
    ###================================================================
    
    
    ###================================================================
    #picking a sensor to integrate and graph from the data
    # this currrent senso: "R BICEPS FEMORIS: Acc 12.Y" is RBF 
    ###================================================================
    
    #    Left            Right
    #    1. TA           2.  TA
    #    3. RF           4.  RF
    #    5. VM           6.  VM
    #    7. SOL          8.  SOL
    #    9. LG           10. LG
    #    11.BF           12. BF
    #    13.GM           14. GM
    #    15.FS           16. FS
    
    # format "R VASTUS MEDIALIS: Acc 6.Y"
    Sensor = "R TIBIALIS ANTERIOR: Acc 2.Z"
    
    # Adding blank frames to add integrated files
    
    df2[Sensor + ' Constant']=0
    df2[Sensor + ' Velocity']=0
    df2[Sensor + ' Position']=0
    
    
    
    ###================================================================
    # inserting formula with integration 
    # attempting to make new column of data for integration of each signal
    #inserts a blank data frame for the integrated values of acc=constant, velocity, and position
    ###================================================================
    
    
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
    
    # RFS was sensor 15
    y2 = df2['Trigno FSR Adapter 15: FSR 15.B']
    
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
    
    Time = df2['X[s].1']
    ACC = df2[Sensor + ' Constant']
    FP3 = y2
    
    
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
    
    plt.figure(dpi=1200)
    fig, ax1 = plt.subplots()
    ax1.title.set_text("Acceleration || " + condition)
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
    
    
    Time = df2['X[s].1']
    ACC = df2[Sensor + ' Velocity']
    FP3 = y2
    
    #Temo1 = Onset_Values_Range.iloc[0]['Onset Values']
    #Temo2 = Offset_Values_Range.iloc[0]['Offset Values']
    
    GraphDFTime = Time.iloc[1:count_row]
    GraphDFACCX1 = ACC.iloc[1:count_row]
    GraphDFFP3 = FP3.iloc[1:count_row]
    
    plt.figure(dpi=1200)
    fig, ax1 = plt.subplots()
    ax1.title.set_text("Velocity || " + condition)
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
    
    Time = df2['X[s].1']
    ACC = df2[Sensor + ' Position']
    FP3 = y2
    
    #Temo1 = Onset_Values_Range.iloc[0]['Onset Values']
    #Temo2 = Offset_Values_Range.iloc[0]['Offset Values']
    
    GraphDFTime = Time.iloc[1:count_row]
    GraphDFACCX1 = ACC.iloc[1:count_row]
    GraphDFFP3 = FP3.iloc[1:count_row]
    
    plt.figure(dpi=1200)
    fig, ax1 = plt.subplots()
    ax1.title.set_text("Position || "+ condition)
    ax2 = ax1.twinx()
    ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
    ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')
    
    ax1.set_xlabel('Time')
    ax1.set_ylabel(Sensor + ' Position', color='black')
    ax2.set_ylabel('FP3', color='black')
    
    
    plt.show ()
