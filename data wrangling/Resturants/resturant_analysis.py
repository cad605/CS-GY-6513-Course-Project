import pandas as pd
import numpy as np
import datetime
file = pd.read_csv('U.S Restaurants.csv')
print(len(pd.unique(file['State_Tribe_Territory'])))
# finds number of unique values. Should have 51 states + 5 U.S territories.
# Currently has 56
print(file.State_Tribe_Territory.unique())
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
for i in file.State_Tribe_Territory.unique():
    if i not in states:
        print(i)
# Confirmed that the states columns are clean.
# Confirming that there's only 1 business type, restaurant
print(file.Business_Type.unique())
#Confirming the number of opening options a restaurant can have
print(file.Action.unique())
#Curbside/carryout/delivery only, Open with social distancing/reduced seating/enhanced sanitation, Authorized to fully reopen' 'Closed'
print(file.order_group.unique())
# For order group, there's ['No restriction found' 'Curbside/delivery only' 'Open with limitations', 'Authorized to fully reopen' 'Closed']
#Checking to see if date time format is accurate for date column.
dates = file.date.apply(str)

for i in dates:
    try:
        datetime.datetime.strptime(i, '%m/%d/%Y %H:%M:%S %p')
    except ValueError:
        print(i)