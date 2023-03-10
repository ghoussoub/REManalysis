# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 12:28:34 2023

@author: ghous
"""
import sys
import streamlit as st
import pandas as pd
import datetime
import calendar
import altair as alt
import pickle
import numpy as np
st.title('Existing Flats Price Estimation')
st.write('This Application makes an estimation of an existing flat price using machine learning technique and based on Open Data provided by Dubai Government (Digital Dubai Authority & Dubai Lands Department).')
area = pd.read_csv(r'area.csv',encoding=('utf_8'))
area.sort_values(by=['area_name_en'], inplace=True)
building = pd.read_csv(r'building.csv',encoding=('utf_8'))
Rooms = pd.read_csv(r'rooms.csv',encoding=('utf_8'))
selected_area = st.selectbox('Select Area',area['area_name_en'])
building_list = building[building['area_name_en']==selected_area]
selected_building = st.selectbox('Select Building',building_list['building_name_en'])
selected_room_no = st.selectbox('No of Rooms', options = ['Studio','1 B/R','2 B/R','3 B/R'])
rooms_selected_record = Rooms[Rooms['Room_En']==selected_room_no]
rooms = rooms_selected_record['Rooms']
flat_size = st.number_input('Select Flat Size (SQM)',min_value=20,max_value=500)
area_selected_record = area[area['area_name_en']==selected_area]
area_med_price = area_selected_record['area_median_meter_price']
area_building_id = selected_area+"/"+selected_building
building_selected_record = building_list[building_list['area_building']==area_building_id]
building_med_price = building_selected_record['meter_sale_price']
building_age = building_selected_record['building_age']
st.write('the user inputs are {}'.format([selected_area,selected_building,selected_room_no,flat_size]))
X = np.array([int(rooms),int(building_age),int(flat_size),int(area_med_price),int(building_med_price)])
X_new = X.reshape(1,-1)
#st.write(X_new)
with open(r'random_forest_regression.pkl','rb') as file:
    regr = pickle.load(file)
file.close()
#X = np.array([3,16,131,11787,10053])
#X_new = X.reshape(1,-1)
result = regr.predict(X_new)
result_format = str(f"{int(result):,}")
st.write(f"Prediction Result: **{result_format}**")
st.write(' (The estimated value should be taken as a starting point of the estimation/valuation process and will not replace a real estates professional assessment!)')
#st.write("Rooms : ",rooms)
#x_new = [[3,16,131,11787,10053]]
#result = regr.predict(x_new)
#print("Prediction: ",result) 
 #"C:\Users\ghous\.spyder-py3\streamlit_apps\streamlit_apps\random_forest_regression.pkl"