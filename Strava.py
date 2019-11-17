
import numpy as np # matrix functions
import pandas as pd # data manipulation
import requests # http requests
from bs4 import BeautifulSoup # html parsing
import matplotlib.pyplot as plt # plotting
import seaborn as sns # plotting
import os # change directory
import re # replace stings

# Access Strava data using API
###############################

# Initialize the dataframe
col_names = ['id','type']
activities = pd.DataFrame(columns=col_names)

access_token = "access_token=xxxxxxxxxxxxxxxxxxxxxxxxx" # enter your access code here
url = "https://www.strava.com/api/v3/activities"

page = 1

while True:
    
    # get page of activities from Strava
    r = requests.get(url + '?' + access_token + '&per_page=50' + '&page=' + str(page))
    r = r.json()

    # if no results then exit loop
    if (not r):
        break
    
    # otherwise add new data to dataframe
    for x in range(len(r)):
        activities.loc[x + (page-1)*50,'id'] = r[x]['id']
        activities.loc[x + (page-1)*50,'type'] = r[x]['type']

    # increment page
    page += 1

# barchart of activity types
activities.head()
activities['type'].value_counts().plot('bar')
plt.title('Activity Breakdown', fontsize=18, fontweight="bold")
plt.xticks(fontsize=14)
plt.yticks(fontsize=16)
plt.ylabel('Frequency', fontsize=18)
 
# filter to only runs
runs = activities[activities.type == 'Run']

# initialize dataframe for split data
col_names = ['average_speed','distance','elapsed_time','elevation_difference','moving_time','pace_zone',
             'split','id','date','description']
splits = pd.DataFrame(columns=col_names)

# loop through each activity id and retrieve data
for run_id in runs['id']:
    
    # Load activity data
    print(run_id)
    r = requests.get(url + '/' + str(run_id) + '?' + access_token)
    r = r.json()

    # Extract Activity Splits
    activity_splits = pd.DataFrame(r['splits_metric']) 
    activity_splits['id'] = run_id
    activity_splits['date'] = r['start_date']
    activity_splits['description'] = r['description']
    
    # Add to total list of splits
    splits = pd.concat([splits, activity_splits])

# Histogram for split distances
plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
plt.hist(splits['distance'], facecolor='blue', alpha=0.5)
plt.title('Split Distances', fontsize=18, fontweight="bold")
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Distance (m)', fontsize=18)
plt.ylabel('Frequency', fontsize=18)

# Filter to only those within +/-50m of 1000m
splits = splits[(splits.distance > 950) & (splits.distance < 1050)]

# Scatter plot of elevation vs. pace
plt.plot( 'elevation_difference', 'moving_time', data=splits, linestyle='', marker='o', markersize=3, alpha=0.1, color="blue")
plt.title('Running Pace vs. Elevation Change', fontsize=18, fontweight="bold")
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Elevation Change (m)', fontsize=18)
plt.ylabel('1km Pace (sec)', fontsize=18)
