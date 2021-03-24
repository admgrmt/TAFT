import pandas as pd 


#import with all headers and rows for left foot
lfon = pd.read_csv ("G:/My Drive/Adam_G_Thesis/4_Data/2. Raw_Data/Muscle_Event_Analysis/Other/Text_ImportExports/LeftFootOnData.txt", delimiter='\t', header=1)
lfon = lfon[["Item","Time"]]

## need to get the differences between each point
## iterate and populate down list of time values

lfon_num = lfon.iloc[:]['Time'].tolist
print (lfon_num)

diff_points = []

previous = 0 
value = 0

for event in lfon_num():
    last_num = event
    event = event - previous
    diff_points.append(event)
    previous = last_num
     
lfon['Differences'] = diff_points

#the difference in time between each Toe_On is a full gait cycle
#we know that stance phase takes up 0.60 of the gait cycle
#if Toe On is 0.0 or 1.00, then heel will be timepoin to 0.60 * differences.

lfon['Differences'] = lfon['Differences'] * 0.60
# we can now add this to the timeframe to get a 0.60 timepoint or basically a full stance phase.

lfon['Time'] = lfon['Time'] - lfon['Differences'] 

#remove differences column 

del lfon['Differences']

# complete
#==========================================
#now to run again for right foot

rfon = pd.read_csv ("G:/My Drive/Adam_G_Thesis/4_Data/2. Raw_Data/Muscle_Event_Analysis/Other/Text_ImportExports/LeftFootOnData.txt", delimiter='\t', header=1)
rfon = rfon[["Item","Time"]]

rfon_num = rfon.iloc[:]['Time'].tolist
print (rfon_num)

diff_points = []

previous = 0 
value = 0

for event in rfon_num():
    last_num = event
    event = event - previous
    diff_points.append(event)
    previous = last_num
     
rfon['Differences'] = diff_points
rfon['Differences'] = rfon['Differences'] * 0.60

rfon['Time'] = rfon['Time'] - rfon['Differences'] 

del rfon['Differences']

#clean up variables
del diff_points, event, last_num, previous, value

####===============================


