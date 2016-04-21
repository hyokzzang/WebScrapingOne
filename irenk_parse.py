from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import numpy as np
import os

# Work path
WorkPath = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------------------
# Part0: Read all of the line level data available
# ------------------------------------------------------------------------------

# The target url
url1 = 'http://www.irenk.net/v3.0/page1/p2_3.asp?m=3'

# Read the contents in the url
ReadURL = requests.Session().get(url1)

# As BeautifulSoup object
soup = BeautifulSoup(ReadURL.content, "lxml")

# Bunch of HS2, HS4, HS8 collections
AllSelectionFields = soup.find_all("select", class_="select")

# Collect HS2
# Note: In the AllSelectionFields,
#   HS2 - [4], HS4 - [5], HS8 - [6]
HSCollectionTotal = AllSelectionFields[6]

# Retrieve only options
HSCollectionTotal = HSCollectionTotal.find_all('option')

# Drop the fist value(which is the selection field)
HSCollectionTotal = HSCollectionTotal[1:]

HS8List = []
for row in HSCollectionTotal:
    HS8List.append(row['value'])

# ------------------------------------------------------------------------------
# Part0: Read all of the line level data available
#   First try : April 21st, HS8List[0:450], Export Data
#   Second try : April 21st, HS8List[252:450], Export Data
# ------------------------------------------------------------------------------

# Empty Pandas DataFrame
Output = pd.DataFrame()

# Initialize count
i = 1
for HS8 in HS8List[252:450]:
    
    # Query
    # t_ype6 : HS2, t_ype7 : HS4, t_ype8 : HS8
    query = {
            "t_ype1":"a",
            "t_ype":"월",
            "t_ype2":"1998",
            "t_ype3":"01",
            "t_ype4":"2015",
            "t_ype5":"12",
            "x_gubun":"천달러",
            "t_ype8":HS8,
        }
        
    # Read URL as requests object by upper query
    urlobj = requests.Session().post(url1, data=query)
    
    # Request object as BeautifulSoup object
    soup = BeautifulSoup(urlobj.content, 'lxml')
    
    # Find all tables
    Find_table_m = soup.find_all("table", class_="table_m")
    
    # Extract the table below
    TableBelow = Find_table_m[1]
    
    # Find all rows
    TableBelowRows = TableBelow.find_all('tr')
    
    # Delete the first row (which is the header)
    TableBelowRows = TableBelowRows[1:]
    
    # Create empty list and loop over rows
    RowsData = []
    for row in TableBelowRows:
        RowsData.append([td.text for td in row.find_all('td')])
    
    # As Pandas DataFrame
    RowsDataFrame = pd.DataFrame(RowsData)
    
    # Rename columns
    RowsDataFrame.rename(index=None, columns={0:'Period', 1:'Ton', 2:'Value', 3:'Price(Dollar/Ton)'}, inplace=True)
    
    # Create HS8 variable
    RowsDataFrame['HS8'] = HS8
    
    # Create Flow variable
    RowsDataFrame['Flow'] = 'E'
    
    # Append to previous result
    Output = Output.append(RowsDataFrame)
    
    # Print elapsed loops
    print(i, " of ", len(HS8List), " completed")
    
    # Counter update
    i = i + 1
    
    # Put delay randomly
    RandomSleep = np.random.normal(loc = 9, scale = 3)
    time.sleep(RandomSleep)
    
    # Print sleeping time
    print("Randomly slepted ", RandomSleep, " Seconds...")
    
# Select first two letters(Year)
Output['Year'] = Output['Period'].str[:2]

# Select middle of letters(Month)
Output['Month'] = Output['Period'].str[3:-1]

# Drop period
Output.drop(['Period'], axis=1, inplace=True, errors='raise')

# Year and Month as numeric
Output['Year'] = pd.to_numeric(Output['Year'], errors='raise')
Output['Month'] = pd.to_numeric(Output['Month'], errors='raise')

# Year in four digits
def YearSort(x):
    if x > 50:
        x = x + 1900
    else:
        x = x + 2000
    
    return x

# Apply the YearSort function described above
Output['Year'] = Output['Year'].apply(YearSort)

# Resort columns
Output = Output.loc[:,['Year', 'Month', 'HS8', 'Flow', 'Value', 'Ton', 'Price(Dollar/Ton)']]

# Finally, into csv file
Output.to_csv(WorkPath + "/Output_HS8_Part2.csv", index=False)