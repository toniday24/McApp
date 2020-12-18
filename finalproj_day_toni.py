"""
Class: CS230--Section HB1 
Name: Toni Day
Data: McDonalds CSV
Description: This app takes the McDonald's dataset and presents a variety of visualizations. The first displays a list of the ten closest
locations through user input of a zip code. It then displays coordinates on a map. The second gives you the perfect location based
on zip code again and a variety of filters. The third presents a chart of the number of stores by region in the US.
I pledge that I have completed the programming assignment independently. 
I have not copied the code from a student or any source.
I have not given my code to any student. 

"""
# Import all necessary applications
import streamlit as st
import pandas as pd
import numpy as np
import csv
import pgeocode
import matplotlib.pyplot as plt


# read mcdonalds (after cleaning) and use pandas to create dataframe
file = 'mcdonalds_clean1.csv'
read_mcdonalds = pd.read_csv(file, header=0 )
mcdonalds = pd.DataFrame(read_mcdonalds)

st.image('https://i.ytimg.com/vi/1CeCFqeDYuM/maxresdefault.jpg', caption=None, use_column_width=True, clamp=False, channels='RGB', output_format='auto')
st.title("My McApp \n")

# begin first vizualization- using pgeocode, allow user to enter zip and convert it into coordinates
st.write("\t\t Map out my McDonalds")
zip = (st.sidebar.text_input("Enter your zip code (Must be Five Digits): "))
nomi = pgeocode.Nominatim('us')
areaInfo = nomi.query_postal_code(zip)
areaDf = pd.DataFrame(areaInfo)
lat = areaDf.loc["latitude"]
long = areaDf.loc["longitude"]

# Using a formula find the distance between coordinates and all the coordinates in the data set
from math import sin, cos, sqrt, atan2, radians

# first need to convert to radians
long1 = radians(long)
lat1 = radians(lat)
# need to make mcdonalds data set into a list in order to convert to radians using numpy
list_of_long = mcdonalds['X'].to_list()
list_of_lat = mcdonalds['Y'].to_list()
lat2= np.radians(list_of_lat)
long2 = np.radians(list_of_long)

R = 6373.0 # Approximate radius of earth

list = [] # creates empty list

for i in range(len(lat2)):  # for loop that iterates over all coordinates and creates distance PROUD OF THIS!
    dlat = lat2[i] - lat1
    dlon = long2[i] - long1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2[i]) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    list.append(distance)

mcdonalds["Distance (KM)"]= list # create new column

ten_closest = mcdonalds.nsmallest(10,'Distance (KM)') #orders the 10 smallest distance
closest_dict = {'lat': ten_closest['Y'], 'lon': ten_closest['X'],'address':ten_closest['address'], 'city':ten_closest['city'], 'state':ten_closest['state'], 'zip':ten_closest['zip'], 'phone':ten_closest['phone'], 'Distance (KM)':ten_closest['Distance (KM)']}
closestDF = pd.DataFrame(data=closest_dict).dropna()
st.write(closestDF)
print(closestDF)

only_coord = closestDF[['lat', 'lon']] # creates a dataframe of only the coordinates
st.write ("\t\t\t\t Your McMap")
st.map(only_coord) # uses this dataframe to map out all of the coordinates


# Create a set of filters that is based on distance and preferences
st.write("\t\t Find Your Perfect Golden Arches")

playplace = st.sidebar.selectbox("Does your Mickey D's have a play place?", ["Y", "N"]) #creates a selectbox that allows user to choose Yes or No
st.sidebar.write(f"You selected: {playplace}") # presents choice

driveThru = st.sidebar.selectbox("Does your Mickey D's have a drivethru?", ["Y", "N"])
st.sidebar.write(f"You selected: {driveThru}")

wifi = st.sidebar.selectbox("Does your Mickey D's have free wifi?", ["Y", "N"])
st.sidebar.write(f"You selected: {wifi}")

archCard = st.sidebar.selectbox("Does your Mickey D's have an Arch Card option?", ["Y", "N"])
st.sidebar.write(f"You selected: {archCard}")

perfectDf= ten_closest.loc[(ten_closest["playplace"]== playplace) & (ten_closest["driveThru"]== driveThru) & (ten_closest["freeWifi"]== wifi) & (ten_closest["archCard"]== archCard)]
FILTERS = ("address", "city", "state", "zip", "phone", "Distance (KM)" ) #links choice to data in csv
perfectDf = perfectDf.filter(FILTERS) #filters out all of the choices and presents df
st.write(perfectDf)
print(perfectDf)

index = perfectDf.index
number_of_rows = len(index) #counts the number of rows to show how many stores are there
st.write(f'You have {number_of_rows} perfect Golden Arches to McDine at!')

# Third visualization will group the data by state and then take the totals by region to present number of stores per region
mcgroup=mcdonalds.groupby("state").size() #groups by state and takes count
mcgroup= pd.DataFrame(mcgroup)

NE = mcgroup.loc[['CT', 'ME','MA', 'NH', 'NJ', 'NY', 'PA', 'RI', 'VA']].sum() #takes the totals for each state that falls under a specific region
MW = mcgroup.loc[['KS', 'IA', 'IL', 'IN', 'MI', 'MN', 'ND', 'NE', 'SD', 'OH', 'WI']].sum()
S = mcgroup.loc[['AK', 'AL', 'DC', 'DE', 'FL', 'GA', 'KY', 'LA', 'MD', 'MS', 'NC', 'OK', 'SC', 'TN','TX', 'VA','WV']].sum()
W = mcgroup.loc[['AL', 'AZ', 'CA', 'CO', 'HI', 'ID', 'MO', 'NV', 'OR', 'NM', 'UT', 'WA', 'WY']].sum()

plotData = pd.DataFrame({
    "Total Stores":[NE, MW, S, W],
    },
    index=["NE", "MW", "S", "W"]
) #makes this into a DF
plotData["Total Stores"] = plotData["Total Stores"].astype(int) #turns the totals into an integer to plot data properly

st.write("\n Number of McDonalds by Region")
st.bar_chart(plotData) #plots this data into a bar chart
