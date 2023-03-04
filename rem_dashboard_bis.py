# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 10:46:31 2023

@author: ghous
"""

import sys
import streamlit as st
import pandas as pd
import datetime
import calendar
import seaborn as sns
import altair as alt
import matplotlib as plt
import plotly.express as px
import plotly.graph_objects as go
import copy
import pickle
import numpy as np
def quarter_month(date):
    month = int(date[3:5])
    qtr_month = (month-1)//3*3+1
    if qtr_month < 10:
        qtr_start = "0"+str(qtr_month)
    else:
        qtr_start = str(qtr_month)
    mod_mth = date.replace(date[3:5],qtr_start)
    mod_date = "01"+mod_mth[2:10]
    return mod_date
st.set_page_config(layout="wide")
@st.cache()
def load_flats():
    df = pd.read_csv(r'flats.csv',encoding=('utf_8'))
    df['year'] = pd.DatetimeIndex(df['instance_date']).year
    df['month'] = pd.DatetimeIndex(df['instance_date']).month
    df['txs_date'] = pd.to_datetime(df['instance_date'],format='%d-%m-%Y')
    df['fst_day'] = df['txs_date'].apply(lambda x : x.replace(day=1))
    df['fst_qtr'] = df['instance_date'].apply(quarter_month)
    #df['fst_day'] = pd.to_datetime(df['fst_day']).dt.date
    df['fst_day'] = pd.to_datetime(df['fst_day'],format='%d-%m-%Y')
    df['fst_qtr'] = pd.to_datetime(df['fst_qtr'],format='%d-%m-%Y')
    return(df)
@st.cache()
def load_villas():
    df = pd.read_csv(r'villas.csv',encoding=('utf_8'))
    df['year'] = pd.DatetimeIndex(df['instance_date']).year
    df['month'] = pd.DatetimeIndex(df['instance_date']).month
    df['txs_date'] = pd.to_datetime(df['instance_date'],format='%d-%m-%Y')
    df['fst_day'] = df['txs_date'].apply(lambda x : x.replace(day=1))
    df['fst_qtr'] = df['instance_date'].apply(quarter_month)
    #df['fst_day'] = pd.to_datetime(df['fst_day']).dt.date
    df['fst_day'] = pd.to_datetime(df['fst_day'],format='%d-%m-%Y')
    df['fst_qtr'] = pd.to_datetime(df['fst_qtr'],format='%d-%m-%Y')
    return(df)
@st.cache()
def load_lands():
    df = pd.read_csv(r'lands.csv',encoding=('utf_8'))
    df['year'] = pd.DatetimeIndex(df['instance_date']).year
    df['month'] = pd.DatetimeIndex(df['instance_date']).month
    df['txs_date'] = pd.to_datetime(df['instance_date'],format='%d-%m-%Y')
    df['fst_day'] = df['txs_date'].apply(lambda x : x.replace(day=1))
    df['fst_qtr'] = df['instance_date'].apply(quarter_month)
    #df['fst_day'] = pd.to_datetime(df['fst_day']).dt.date
    df['fst_day'] = pd.to_datetime(df['fst_day'],format='%d-%m-%Y')
    df['fst_qtr'] = pd.to_datetime(df['fst_qtr'],format='%d-%m-%Y')
    return(df) 

def perf_class(x):
    if x >= 20:
         perf = "more than 20%"
    elif x < 20 and x >= 5:
         perf = "btw 5 to 20%"
    elif x < 5 and x > -5:
         perf = "btw -5 & 5%"
    elif x < -5 and x > -20:
         perf = "btw -20 & -5%"
    elif x <= -20:
         perf = "less than -20%"
    else:
        perf = "N/A"
    return perf  
def size_range(x):
    if x >= 600:
        range = "more than 600 SQM"
    elif x < 600 and x >= 300:
        range = "btw 300 to 600"
    else:
        range = "less than 300"
    return range
def land_class(x):
    #global land_usage
    if x == "Commercial":
        land_usage = "Commercial"
    elif x == "Residential":
        land_usage = "Residential"
    elif x == "Residential / Commercial":
        land_usage = "Mixed"
    elif x == "Industrial":
        land_usage = "Industrial"
    elif x == "Agricultural":
        land_usage = "Agricultural"
    else:
        land_usage = "Other"
    return land_usage
def land_size_range(x):
    if x >= 2000:
        range = "more than 2000 SQM"
    elif x < 2000 and x >= 1000:
        range = "btw 1000 to 2000"
    elif x < 1000 and x >= 500:
        range = "btw 500 to 1000"
    elif x < 500 and x >= 200:
        range = "btw 200 to 500"
    elif x < 200 and x >=100:
        range = "btw 100 to 200"
    else:
        range = "less than 100"
    return range
def tot_count(x,y,z):
    agg_flat_sales_filter = all_registry_rooms_qtr_median_prices[(all_registry_rooms_qtr_median_prices.registry == x)&(all_registry_rooms_qtr_median_prices.Room_En == y)]
    intermediate = agg_flat_sales_filter[agg_flat_sales_filter.fst_qtr==z]
    total_count = intermediate['qtr_txs'].sum()
    return total_count
def agg_area_prices(x,y,z):
    agg_flat_sales_filter = area_summary_copy[(area_summary_copy.registry == x)&(area_summary_copy.Room_En == y)]
    intermediate = agg_flat_sales_filter[agg_flat_sales_filter.fst_qtr == z]
    agg_relative_price = intermediate['relative_price'].sum()
    return agg_relative_price
def period_count(x,y):
    period_flat_sales_filter = period_area_summary_copy[(period_area_summary_copy.Room_En == x)&(period_area_summary_copy.registry == y)]
    return period_flat_sales_filter['txs_count'].sum()
def period_villa_count(x,y):
    period_villa_sales_filter = period_villa_area_summary_copy[(period_villa_area_summary_copy.size_range == x)&(period_villa_area_summary_copy.registry == y)]
    return period_villa_sales_filter['txs_count'].sum()

def tot_villa_count(x,y,z):
    agg_villa_sales_filter = all_registry_size_qtr_median_prices[(all_registry_size_qtr_median_prices.registry == x)&(all_registry_size_qtr_median_prices.size_range == y)]
    intermediate = agg_villa_sales_filter[agg_villa_sales_filter.fst_qtr==z]
    total_count = intermediate['qtr_txs'].sum()
    return total_count
def agg_villa_area_prices(x,y,z):
    agg_villa_sales_filter = area_villa_summary_copy[(area_villa_summary_copy.registry == x)&(area_villa_summary_copy.size_range == y)]
    intermediate = agg_villa_sales_filter[agg_villa_sales_filter.fst_qtr == z]
    agg_villa_relative_price = intermediate['relative_price'].sum()
    return agg_villa_relative_price
def tot_land_count(x,y):
    agg_land_sales_filter = all_usage_qtr_median_meter_prices[(all_usage_qtr_median_meter_prices.land_usage == x)&(all_usage_qtr_median_meter_prices.fst_qtr == y)]
    total_count = agg_land_sales_filter['qtr_txs'].sum()
    return total_count
def period_land_count(x):
    period_land_sales_filter = period_land_area_summary_copy[(period_land_area_summary_copy.land_usage == x)]
    return period_land_sales_filter['txs_count'].sum()
def agg_land_area_prices(x,y):
    agg_land_sales_filter = area_land_summary_copy[(area_land_summary_copy.land_usage == x)&(area_land_summary_copy.fst_qtr == y)]
    agg_land_relative_price = agg_land_sales_filter['relative_meter_price'].sum()
    return agg_land_relative_price
df = load_flats()
df1 = load_villas()
df2 = load_lands()
#area = df['area_name_en'].drop_duplicates()
area = list(df['area_name_en'].unique())
#area.sort_values(by=['area_name_en'], inplace=True)
#area.sort_values('area_name_en',axis=0,ascending=False).reset_index(drop=True)
flats = df
flat_sales = flats.copy(deep = True)
flat_sales['registry'] = flat_sales['reg_type_id'].apply(lambda x: "Ready" if x == 1 else "OffPlan")
villas = df1[df1.procedure_area <= 1000]
villa_sales = villas.copy(deep = True)
villa_sales['registry'] = villa_sales['reg_type_id'].apply(lambda x: "Ready" if x == 1 else "OffPlan")
lands = df2[df2.procedure_area <= 10000]
land_sales = lands.copy(deep = True)
land_sales['land_usage'] = land_sales['property_usage_en'].apply(lambda x: land_class(x))
st.sidebar.title("Dubai Real Estates Market Dashboards")
#st.sidebar.markdown('###')
st.sidebar.markdown("*Settings*")
#start_year, end_year = st.sidebar.slider(
    #"Period",
    #min_value=min_year, max_value=max_year,
    #value=(min_year, max_year))

#st.sidebar.markdown('###')
#origins = st.sidebar.multiselect('Origins', origin_list,
                                 #default=origin_list)
#st.sidebar.markdown('###')
#item1 = st.sidebar.selectbox('Item 1', item_list, index=0)
#item2 = st.sidebar.selectbox('Item 2', item_list, index=3)
option = st.sidebar.selectbox("Select Dashboard?", ('Market Historical Trend','Comparative Areas Performance (flats)','Area Specific Flats Prices Analysis', 'Flats Transactions Search','Comparative Areas Performance (villas)','Area Specific Villas Prices Analysis','Villas Transactions Search','Comparative Areas Performance (lands)','Area Specific Lands Prices Analysis','Lands Transactions Search','Flat Price Estimation'))
if option == 'Area Specific Flats Prices Analysis':
    registry = st.sidebar.selectbox('Select registry type?',('Existing Properties','Off-Plan Properties'))
    if registry == "Existing Properties":
        registry_code = 1
    else:
        registry_code = 0
    flat_area = flat_sales['area_name_en'].unique()
    select_area = st.sidebar.selectbox('Select area?',flat_area)
    #st.header("Area Market Analysis of : {}".format(select_area))
    st.header(option+" in : {}".format(select_area))
    st.markdown("The metrics below are calculated based on last 90 days period compared to same period last year (YoY)")
    #select_rooms = st.sidebar.multiselect('Select Flat Rooms', ("1 B/R","2 B/R","3 B/R"),"1 B/R")
    #slider_year = st.sidebar.slider("Period",2010, int(df['year'].max()))
    #start = st.sidebar.date_input("Start Date", value = pd.to_datetime('2010-01-01'))
    #start_day = start.replace(day=1)
    start_day = pd.to_datetime('2010-01-01')
    #end = st.sidebar.date_input("End Date",value = pd.to_datetime('today'))
    #end_day = end.replace(day=1)
    end_day = flat_sales['txs_date'].max()
    #flat_sales = df[(df['trans_group_id']==1)&(df['property_type_id']==3)&(df['property_sub_type_id']==60)]
    #flat_sales_select = flat_sales[(flat_sales['reg_type_id']==registry_code)&(flat_sales['area_name_en'] == select_area)&(flat_sales['fst_day'] >= start_day)&(flat_sales['fst_day'] <= end_day)&(flat_sales['Rooms'] >= 1)&(flat_sales['Rooms']<=4)]
    end_date = flat_sales['txs_date'].max()
    start_date = end_date - datetime.timedelta(days=90)
    #flat_sales_selected_period = flat_sales[(flat_sales['reg_type_id']==registry_code)&(flat_sales['area_name_en']==select_area)&(flat_sales['Room_En'].isin( select_rooms))&(flat_sales['txs_date']<=end_date)&(flat_sales['txs_date']>=start_date)]
    flat_sales_selected_period = flat_sales[(flat_sales['reg_type_id']==registry_code)&(flat_sales['area_name_en']==select_area)&(flat_sales['txs_date']<=end_date)&(flat_sales['txs_date']>=start_date)&(flat_sales['Rooms']>=2)&(flat_sales['Rooms']<=4)]
    this_period_count = flat_sales_selected_period['transaction_id'].count()
    this_period_median_meter_price = int(flat_sales_selected_period['meter_sale_price'].median()) if this_period_count != 0 else 0
    flat_sales_selected_previous_period = flat_sales[(flat_sales['reg_type_id']==registry_code)&(flat_sales['area_name_en']==select_area)&(flat_sales['txs_date']<=end_date - datetime.timedelta(days=365))&(flat_sales['txs_date']>=end_date - datetime.timedelta(days=455))]
    previous_period_count = flat_sales_selected_previous_period['transaction_id'].count()
    this_period_txs_count_prct_chg = (this_period_count-previous_period_count)/previous_period_count if this_period_count != 0 else 0
    last_period_median_meter_price = flat_sales_selected_previous_period['meter_sale_price'].median()
    this_period_median_meter_price_prct_chg = (this_period_median_meter_price-last_period_median_meter_price)/last_period_median_meter_price
    this_period_median_flat_size = int(flat_sales_selected_period['procedure_area'].median())
    last_period_median_flat_size = flat_sales_selected_previous_period['procedure_area'].median()
    this_period_median_flat_size_prct_chg = (this_period_median_flat_size-last_period_median_flat_size)/last_period_median_flat_size
    kpi1,kpi2,kpi3 = st.columns(3)
    kpi1.metric("Last 90 Days txs count",f"{this_period_count:,}","{0:.0%}".format(this_period_txs_count_prct_chg))
    kpi2.metric("last 90 Days median meter price : ",f"{this_period_median_meter_price:,}","{0:.0%}".format(this_period_median_meter_price_prct_chg))
    kpi3.metric("Last 90 Days median flat size (SQM) : ",f"{this_period_median_flat_size:,}","{0:.0%}".format(this_period_median_flat_size_prct_chg))
    this_period_1bed_txs = flat_sales_selected_period[flat_sales_selected_period['Rooms']==2]
    this_period_1bed_median_price = int(this_period_1bed_txs['actual_worth'].median(skipna = False))
    last_period_1bed_txs = flat_sales_selected_previous_period[flat_sales_selected_previous_period['Rooms']==2]
    last_period_1bed_median_price = last_period_1bed_txs['actual_worth'].median()
    this_period_1bed_price_pct_chg = ((this_period_1bed_median_price-last_period_1bed_median_price)/last_period_1bed_median_price)
    this_period_2bed_txs = flat_sales_selected_period[flat_sales_selected_period['Rooms']==3]
    this_period_2bed_median_price = this_period_2bed_txs['actual_worth'].median()
    if pd.isna(this_period_2bed_median_price):
        this_period_2bed_median_price = 0
    this_period_2bed_median_price = int(this_period_2bed_median_price)
    last_period_2bed_txs = flat_sales_selected_previous_period[flat_sales_selected_previous_period['Rooms']==3]
    last_period_2bed_median_price = last_period_2bed_txs['actual_worth'].median()
    this_period_2bed_price_pct_chg = ((this_period_2bed_median_price-last_period_2bed_median_price)/last_period_2bed_median_price)
    this_period_3bed_txs = flat_sales_selected_period[flat_sales_selected_period['Rooms']==4]
    this_period_3bed_median_price = this_period_3bed_txs['actual_worth'].median()
    if pd.isna(this_period_3bed_median_price):
        this_period_3bed_median_price = 0
    this_period_3bed_median_price = int(this_period_3bed_median_price)
    last_period_3bed_txs = flat_sales_selected_previous_period[flat_sales_selected_previous_period['Rooms']==4]
    last_period_3bed_median_price = last_period_3bed_txs['actual_worth'].median()
    this_period_3bed_price_pct_chg = ((this_period_3bed_median_price-last_period_3bed_median_price)/last_period_3bed_median_price)
    flat_sales_select = flat_sales[(flat_sales['reg_type_id']==registry_code)&(flat_sales['area_name_en'] == select_area)&(flat_sales['Rooms']>=2)&(flat_sales['Rooms'] <=4)&(flat_sales['fst_day'] >= start_day)&(flat_sales['fst_day'] <= end_day)]
    single_area_median_prices = pd.DataFrame(flat_sales_select.groupby(['Room_En','fst_day']).agg(single_area_median_meter_price = ('meter_sale_price','median'),single_area_median_price = ('actual_worth','median'), single_area_txs_count = ('transaction_id','count')))  
    single_area_median_prices_df = single_area_median_prices.reset_index()
    single_area_qtr_median_prices = pd.DataFrame(flat_sales_select.groupby(['Room_En','fst_qtr']).agg(single_area_qtr_median_meter_price = ('meter_sale_price','median'),single_area_qtr_median_price = ('actual_worth','median'), single_area_txs_count = ('transaction_id','count')))  
    single_area_qtr_median_prices_df = single_area_qtr_median_prices.reset_index()
    single_area_median_prices_df['rolling_mean'] = single_area_median_prices_df.set_index('fst_day').groupby('Room_En', sort=False)['single_area_median_price'].rolling(9).mean().round(0).to_numpy()
    single_area_median_prices_df['meter_rolling_mean'] = single_area_median_prices_df.set_index('fst_day').groupby('Room_En', sort=False)['single_area_median_meter_price'].rolling(9).mean().round(0).to_numpy()
    single_area_median_prices_df['txs_count_rolling_mean'] = single_area_median_prices_df.set_index('fst_day').groupby('Room_En', sort=False)['single_area_txs_count'].rolling(9).mean().round(0).to_numpy()
    single_area_median_prices_start_df = single_area_median_prices_df[single_area_median_prices_df['fst_day']==start_day]
    single_area_median_prices_added_start_df = pd.merge(single_area_median_prices_df,single_area_median_prices_start_df,left_on="Room_En",right_on="Room_En",how = "left")
    single_area_median_prices_added_start_df['price_pct_chg'] = 100*(single_area_median_prices_added_start_df['single_area_median_price_x']-single_area_median_prices_added_start_df['single_area_median_price_y'])/single_area_median_prices_added_start_df['single_area_median_price_y']
    single_area_median_prices_added_start_df['meter_price_pct_chg'] = 100*(single_area_median_prices_added_start_df['single_area_median_meter_price_x']-single_area_median_prices_added_start_df['single_area_median_meter_price_y'])/single_area_median_prices_added_start_df['single_area_median_meter_price_y']
    kpi4,kpi5,kpi6 = st.columns(3)
    kpi4.metric("Last 90 Days 1 B/R median Price",f"{this_period_1bed_median_price:,}","{0:.0%}".format(this_period_1bed_price_pct_chg))
    kpi5.metric("Last 90 Days 2 B/R median Price",f"{this_period_2bed_median_price:,}","{0:.0%}".format(this_period_2bed_price_pct_chg))
    kpi6.metric("Last 90 Days 3 B/R median Price",f"{this_period_3bed_median_price:,}","{0:.0%}".format(this_period_3bed_price_pct_chg))
    st.subheader("Last 90 Days txs Scatter Plot (Price vs Size)")
    base = alt.Chart(flat_sales_selected_period).properties(height=300)
    point = base.mark_circle(size=20).encode(x=alt.X('actual_worth' + ':Q', title="price"), y=alt.Y('procedure_area' + ':Q', title="size"),color=alt.Color('Room_En', title='Rooms',legend=alt.Legend(orient='bottom-right')))
    st.altair_chart(point, use_container_width=True)
    
    st.markdown("##")
    st.subheader("Historical Trend of Flats' Prices and transactions count (Quarterly and 9 months moving average trend)")
    room_radio_selection = st.radio("Select Flat Rooms:", options = ['1 B/R','2 B/R','3 B/R'],horizontal = True)
    rolling_room_selection = single_area_median_prices_df[single_area_median_prices_df.Room_En == room_radio_selection]
    qtr_median_room_selection = single_area_qtr_median_prices_df[single_area_qtr_median_prices_df.Room_En == room_radio_selection]
    base10 = alt.Chart(qtr_median_room_selection).properties(height=300)
    line10 = base10.mark_bar(size=2).encode(x=alt.X('fst_qtr', title='Date'),y=alt.Y('single_area_qtr_median_price', title='median price'),color=alt.Color('Room_En', title='Flat Size',legend=alt.Legend(orient='right')))
    base11 = alt.Chart(rolling_room_selection).properties(height=300)
    #line11 = base11.mark_line(size=2).encode(x=alt.X('fst_day', title='Date'),y=alt.Y('rolling_mean', title='rolling median price'),color=alt.Color('Room_En', title='Flat Size',legend=alt.Legend(orient='right')))
    line11 = base11.mark_line(color='red').encode(x=alt.X('fst_day', title='Date'),y=alt.Y('rolling_mean', title='rolling median price'))
    chart10 = (line10 + line11)
    #st.altair_chart(chart10,use_container_width=True)
    base12 = alt.Chart(qtr_median_room_selection).properties(height=300)
    line12 = base12.mark_bar(size=2).encode(x=alt.X('fst_qtr', title='Date'),y=alt.Y('single_area_qtr_median_meter_price', title='median meter price'),color=alt.Color('Room_En', title='Flat Size',legend=alt.Legend(orient='right')))
    base13 = alt.Chart(rolling_room_selection).properties(height=300)
    #line13 = base13.mark_line(size=2).encode(x=alt.X('fst_day', title='Date'),y=alt.Y('meter_rolling_mean', title='rolling median meter price'),color=alt.Color('Room_En', title='Flat Size',legend=alt.Legend(orient='right')))
    line13 = base13.mark_line(color='red').encode(x=alt.X('fst_day', title='Date'),y=alt.Y('meter_rolling_mean', title='rolling median meter price'))
    chart12 = (line12 + line13)
    #st.altair_chart(chart12,use_container_width=True)
    base14 = alt.Chart(qtr_median_room_selection).properties(height=300)
    line14 = base14.mark_bar(size=2).encode(x=alt.X('fst_qtr', title='Date'),y=alt.Y('single_area_txs_count', title='Qtr txs count'),color=alt.Color('Room_En', title='Flat Size',legend=alt.Legend(orient='right')))
    base15 = alt.Chart(rolling_room_selection).properties(height=300)
    line15 = base15.mark_line(color='red').encode(x=alt.X('fst_day', title='Date'),y=alt.Y('txs_count_rolling_mean', title='Monthly Moving Average'))
    chart14 = (line14 + line15)
    #st.altair_chart(chart14,use_container_width=True)
    tab1, tab2 , tab3 = st.tabs(["Median Prices", "Median Meter Prices", "Transactions Count"])
    with tab1:
        st.altair_chart(chart10,use_container_width=True)
    with tab2:
        st.altair_chart(chart12,use_container_width=True)
    with tab3:
        st.altair_chart(chart14,use_container_width=True)
    
    
if option == 'Comparative Areas Performance (flats)': 
    #st.header(option)
    #st.markdown("Area performance is determined by the area flat median price percentage change for the last 90 days period compared to same period last year")
    registry = st.sidebar.selectbox('Select registry type?',('Existing Properties','Off-Plan Properties'))
    if registry == "Existing Properties":
        registry_code = 1
    else:
        registry_code = 0
    select_rooms = st.sidebar.selectbox('Select Flat Rooms', ('1 B/R','2 B/R','3 B/R'))
    st.header(option)
    st.markdown("Area performance is determined by the area flat median price percentage change for the last 90 days period compared to same period last year")
    end_date = flat_sales['txs_date'].max()
    start_date = end_date - datetime.timedelta(days=90)
    flat_sales_selected_period = flat_sales[(flat_sales['reg_type_id']==registry_code)&(flat_sales['Room_En'] == select_rooms)&(flat_sales['txs_date']<=end_date)&(flat_sales['txs_date']>=start_date)]
    flat_sales_selected_period_summary = pd.DataFrame(flat_sales_selected_period.groupby(['area_name_en']).agg(area_median_meter_price = ('meter_sale_price','median'),area_median_price = ('actual_worth','median'), area_txs_count = ('transaction_id','count'),flat_median_size = ('procedure_area','median')))
    flat_sales_selected_period_summary_df = flat_sales_selected_period_summary.reset_index()
    flat_sales_selected_previous_period = flat_sales[(flat_sales['reg_type_id']==registry_code)&(flat_sales['Room_En'] == select_rooms)&(flat_sales['txs_date']<=end_date - datetime.timedelta(days=365))&(flat_sales['txs_date']>=end_date - datetime.timedelta(days=455))]
    flat_sales_selected_previous_period_summary = pd.DataFrame(flat_sales_selected_previous_period.groupby(['area_name_en']).agg(previous_area_median_meter_price = ('meter_sale_price','median'),previous_area_median_price = ('actual_worth','median'), previous_area_txs_count = ('transaction_id','count')))
    flat_sales_selected_previous_period_summary_df = flat_sales_selected_previous_period_summary.reset_index()
    merged_current_previous_period = pd.merge(flat_sales_selected_period_summary_df,flat_sales_selected_previous_period_summary_df,on = "area_name_en",how = "left")
    merged_current_previous_period['median_meter_price_prct_chg'] = 100* (merged_current_previous_period['area_median_meter_price']-merged_current_previous_period['previous_area_median_meter_price'])/merged_current_previous_period['previous_area_median_meter_price']
    merged_current_previous_period['median_price_prct_chg'] = 100 * (merged_current_previous_period['area_median_price']-merged_current_previous_period['previous_area_median_price'])/merged_current_previous_period['previous_area_median_price']
    merged_current_previous_period['area_txs_count_prct_chg'] = 100 * (merged_current_previous_period['area_txs_count']-merged_current_previous_period['previous_area_txs_count'])/merged_current_previous_period['previous_area_txs_count']
    merged_subset = merged_current_previous_period[['area_name_en','area_median_price','median_price_prct_chg','area_median_meter_price','median_meter_price_prct_chg','flat_median_size','area_txs_count','area_txs_count_prct_chg']]
    merged_subset['perf_class'] = merged_subset['median_price_prct_chg'].apply(lambda x: perf_class(x))
    #merged_subset.rename(columns = {'area_name_en':'Area Name','area_median_price':'Med. Price','median_price_prct_chg':'% Price Chg','area_median_meter_price':'Med. Mtr Price','median_meter_price_prct_chg':'% Mtr Chg','flat_median_size' : 'Flat Size','area_txs_count':'Txs Count','area_txs_count_prct_chg':'% Txs Chg'},inplace = True)
    #merged_subset['% Price Chg'] = merged_subset['% Price Chg'].astype(float).map("{:.2%}".format)
    #merged_subset['% Mtr Chg'] = merged_subset['% Mtr Chg'].astype(float).map("{:.2%}".format)
    #merged_subset['% Txs Chg'] = merged_subset['% Txs Chg'].astype(float).map("{:.2%}".format)
    #merged_subset['Med. Price'] = merged_subset['Med. Price'].astype(int)
    #merged_subset['Med. Mtr Price'] = merged_subset['Med. Mtr Price'].astype(int)
    #merged_subset['Flat Size'] = merged_subset['Flat Size'].astype(int)
    #st.dataframe(merged_subset)
    #print_some_rows = merged_subset.head(5)
    #print(print_some_rows)
    #with st.sidebar:
        #add_radio = st.radio("Sorting Result by:",("Area Name", "Flat Price","Txs Count"))
    st.markdown('###')
    st.subheader("Interactive Areas Performance Chart")
    #st.markdown('')
    perf_radio_selection = st.radio("Select Area Performance Range:", options = ['All ranges','more than 20%','btw 5 to 20%','btw -5 & 5%','btw -20 & -5%','less than -20%'],horizontal = True)
    #slider1,slider2,slider3= st.columns(3)
    #with slider1:
      #  slider1 = st.slider("Price prct Change Range:",min_value = merged_subset['median_price_prct_chg'].min(),max_value = merged_subset['median_price_prct_chg'].max(),value = (merged_subset['median_price_prct_chg'].min(),merged_subset['median_price_prct_chg'].max()))
    #with slider2:
        #slider2 = st.slider("Txs Count Range :",min_value = float(merged_subset['area_txs_count'].min()),max_value=float(merged_subset['area_txs_count'].max()), value = (float(merged_subset['area_txs_count'].min()),float(merged_subset['area_txs_count'].max())),step = 10.0)
    #with slider3:
        #slider3 = st.slider("Meter Price Range :",min_value = merged_subset['area_median_meter_price'].min(),max_value = merged_subset['area_median_meter_price'].max(),value = (merged_subset['area_median_meter_price'].min(),merged_subset['area_median_meter_price'].max()))
    if perf_radio_selection == "All ranges":
        reduced_merged = merged_subset
    else: reduced_merged = merged_subset[(merged_subset['perf_class'] == perf_radio_selection)]
    base10 = alt.Chart(reduced_merged).properties(height=300)
    point10 = base10.mark_circle(size=20).encode(x=alt.X('area_median_price' + ':Q', title="price"), y=alt.Y('flat_median_size' + ':Q', title="Flat Size"),size = 'area_txs_count', tooltip = ['area_name_en','area_txs_count','area_median_price','area_median_meter_price','flat_median_size','median_price_prct_chg'],color=alt.Color('perf_class', title='Area Med. Value vs Size',legend=alt.Legend(orient='right'))).interactive()
    #point10_text = base10.mark_text
    #point10 = base10.mark_point(size=20).encode(x=alt.X('area_median_price' + ':Q', title="price"), y=alt.Y('flat_median_size' + ':Q', title="Flat Size"),size = 'area_txs_count')
    #text = point10.mark_text(align='left',baseline='middle',dx=1).encode(text='area_name_en')
    #point10 + text
    st.altair_chart(point10, use_container_width=True)
    st.markdown('###')
    st.subheader('Areas Performance Details (for selected performance range)')
    st.dataframe(reduced_merged)
if  option == 'Flats Transactions Search':
    st.header(option)
    st.markdown("- Flats transactions search is provided for the last 30 days (or part of it depending on dates selection)")
    st.markdown("- Results can be sorted on each column (ascending,desending)")
    registry = st.sidebar.selectbox('Select registry type?',('Existing Properties','Off-Plan Properties'))
    if registry == "Existing Properties":
        registry_code = 1
    else:
        registry_code = 0
    select_rooms = st.sidebar.multiselect('Select Flat Rooms', ('1 B/R','2 B/R','3 B/R','Studio'),'1 B/R')
    end_date = flat_sales['txs_date'].max()
    start_date = end_date - datetime.timedelta(days=30)
    start = st.sidebar.date_input("Start Date", value = start_date)
    end = st.sidebar.date_input("End Date",value = end_date)
    flat_area = flat_sales['area_name_en'].unique()
    select_area = st.sidebar.multiselect('Select area?',flat_area,flat_area[3])
    select_txs = flat_sales[(flat_sales['reg_type_id']==registry_code)&(flat_sales['area_name_en'].isin(select_area))&(flat_sales['Room_En'].isin(select_rooms))&(flat_sales['txs_date']<=end_date)&(flat_sales['txs_date']>=start_date)]
    select_txs['date'] = pd.to_datetime(select_txs['txs_date']).dt.date
    display_txs = select_txs[['date','area_name_en','building_name_en','Room_En','actual_worth','procedure_area','meter_sale_price']]
    st.dataframe(display_txs)
if  option == 'Flat Price Estimation':
    st.header(option)
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
if  option == 'Comparative Areas Performance (villas)':
    st.header(option)
    st.markdown("Area performance is determined by the area villa median price percentage change for the last 90 days period compared to same period last year")
    registry = st.sidebar.selectbox('Select registry type?',('Existing Properties','Off-Plan Properties'))
    if registry == "Existing Properties":
        registry_code = 1
    else:
        registry_code = 0
    select_size_range = st.sidebar.selectbox('Select Villa Size', ('All Sizes','less than 100','btw 100 to 200','btw 200 to 300','btw 300 to 400','btw 400 to 500','more than 500 SQM'))
    end_date = villa_sales['txs_date'].max()
    start_date = end_date - datetime.timedelta(days=90)
    villa_sales['size_range'] = villa_sales['procedure_area'].apply(lambda x: size_range(x))
    if select_size_range == "All Sizes":
        villa_sales_selected_period = villa_sales[(villa_sales['reg_type_id']==registry_code)&(villa_sales['txs_date']<=end_date)&(villa_sales['txs_date']>=start_date)]
    else:
        villa_sales_selected_period = villa_sales[(villa_sales['reg_type_id']==registry_code)&(villa_sales['size_range'] == select_size_range)&(villa_sales['txs_date']<=end_date)&(villa_sales['txs_date']>=start_date)]
    villa_sales_selected_period_summary = pd.DataFrame(villa_sales_selected_period.groupby(['area_name_en']).agg(area_median_meter_price = ('meter_sale_price','median'),area_median_price = ('actual_worth','median'), area_txs_count = ('transaction_id','count'),villa_median_size = ('procedure_area','median')))
    villa_sales_selected_period_summary_df = villa_sales_selected_period_summary.reset_index()
    if select_size_range == "All Sizes":
        villa_sales_selected_previous_period = villa_sales[(villa_sales['reg_type_id']==registry_code)&(villa_sales['txs_date']<=end_date - datetime.timedelta(days=365))&(villa_sales['txs_date']>=end_date - datetime.timedelta(days=455))]
    else:
        villa_sales_selected_previous_period = villa_sales[(villa_sales['reg_type_id']==registry_code)&(villa_sales['size_range'] == select_size_range)&(villa_sales['txs_date']<=end_date - datetime.timedelta(days=365))&(villa_sales['txs_date']>=end_date - datetime.timedelta(days=455))]
    villa_sales_selected_previous_period_summary = pd.DataFrame(villa_sales_selected_previous_period.groupby(['area_name_en']).agg(previous_area_median_meter_price = ('meter_sale_price','median'),previous_area_median_price = ('actual_worth','median'), previous_area_txs_count = ('transaction_id','count')))
    villa_sales_selected_previous_period_summary_df = villa_sales_selected_previous_period_summary.reset_index()
    merged_current_previous_period = pd.merge(villa_sales_selected_period_summary_df,villa_sales_selected_previous_period_summary_df,on = "area_name_en",how = "left")
    merged_current_previous_period['median_meter_price_prct_chg'] = 100* (merged_current_previous_period['area_median_meter_price']-merged_current_previous_period['previous_area_median_meter_price'])/merged_current_previous_period['previous_area_median_meter_price']
    merged_current_previous_period['median_price_prct_chg'] = 100 * (merged_current_previous_period['area_median_price']-merged_current_previous_period['previous_area_median_price'])/merged_current_previous_period['previous_area_median_price']
    merged_current_previous_period['area_txs_count_prct_chg'] = 100 * (merged_current_previous_period['area_txs_count']-merged_current_previous_period['previous_area_txs_count'])/merged_current_previous_period['previous_area_txs_count']
    merged_subset = merged_current_previous_period[['area_name_en','area_median_price','median_price_prct_chg','area_median_meter_price','median_meter_price_prct_chg','villa_median_size','area_txs_count','area_txs_count_prct_chg']]
    merged_subset['perf_class'] = merged_subset['median_price_prct_chg'].apply(lambda x: perf_class(x))
    #merged_subset.rename(columns = {'area_name_en':'Area Name','area_median_price':'Med. Price','median_price_prct_chg':'% Price Chg','area_median_meter_price':'Med. Mtr Price','median_meter_price_prct_chg':'% Mtr Chg','flat_median_size' : 'Flat Size','area_txs_count':'Txs Count','area_txs_count_prct_chg':'% Txs Chg'},inplace = True)
    #merged_subset['% Price Chg'] = merged_subset['% Price Chg'].astype(float).map("{:.2%}".format)
    #merged_subset['% Mtr Chg'] = merged_subset['% Mtr Chg'].astype(float).map("{:.2%}".format)
    #merged_subset['% Txs Chg'] = merged_subset['% Txs Chg'].astype(float).map("{:.2%}".format)
    #merged_subset['Med. Price'] = merged_subset['Med. Price'].astype(int)
    #merged_subset['Med. Mtr Price'] = merged_subset['Med. Mtr Price'].astype(int)
    #merged_subset['Flat Size'] = merged_subset['Flat Size'].astype(int)
    #print_some_rows = merged_subset.head(5)
    #print(print_some_rows)
    #with st.sidebar:
        #add_radio = st.radio("Sorting Result by:",("Area Name", "Flat Price","Txs Count"))
    st.markdown('###')
    st.header("Interactive Areas Performance Chart")
    #st.markdown('')
    perf_radio_selection = st.radio("Select Area Performance Range:", options = ['All ranges','more than 20%','btw 5 to 20%','btw -5 & 5%','btw -20 & -5%','less than -20%'],horizontal = True)
    #slider1,slider2,slider3= st.columns(3)
    #with slider1:
      #  slider1 = st.slider("Price prct Change Range:",min_value = merged_subset['median_price_prct_chg'].min(),max_value = merged_subset['median_price_prct_chg'].max(),value = (merged_subset['median_price_prct_chg'].min(),merged_subset['median_price_prct_chg'].max()))
    #with slider2:
        #slider2 = st.slider("Txs Count Range :",min_value = float(merged_subset['area_txs_count'].min()),max_value=float(merged_subset['area_txs_count'].max()), value = (float(merged_subset['area_txs_count'].min()),float(merged_subset['area_txs_count'].max())),step = 10.0)
    #with slider3:
        #slider3 = st.slider("Meter Price Range :",min_value = merged_subset['area_median_meter_price'].min(),max_value = merged_subset['area_median_meter_price'].max(),value = (merged_subset['area_median_meter_price'].min(),merged_subset['area_median_meter_price'].max()))
    if perf_radio_selection == "All ranges":
        reduced_merged = merged_subset
    else: reduced_merged = merged_subset[(merged_subset['perf_class'] == perf_radio_selection)]
    base10 = alt.Chart(reduced_merged).properties(height=300)
    point10 = base10.mark_circle(size=20).encode(x=alt.X('area_median_price' + ':Q', title="price"), y=alt.Y('villa_median_size' + ':Q', title="Villa Size"),size = 'area_txs_count', tooltip = ['area_name_en','area_txs_count','area_median_price','area_median_meter_price','villa_median_size','median_price_prct_chg'],color=alt.Color('perf_class', title='Area Med. Value vs Size',legend=alt.Legend(orient='right'))).interactive()
    #point10_text = base10.mark_text
    #point10 = base10.mark_point(size=20).encode(x=alt.X('area_median_price' + ':Q', title="price"), y=alt.Y('flat_median_size' + ':Q', title="Flat Size"),size = 'area_txs_count')
    #text = point10.mark_text(align='left',baseline='middle',dx=1).encode(text='area_name_en')
    #point10 + text
    st.altair_chart(point10, use_container_width=True)
    st.markdown('###')
    st.subheader('Areas Performance Details (for selected performance range)')
    st.dataframe(reduced_merged)
if  option == 'Area Specific Villas Prices Analysis':
    villa_area = villa_sales['area_name_en'].unique()
    select_area = st.sidebar.selectbox('Select area?',villa_area)
    #registry = st.sidebar.selectbox('Select registry type?',('Existing Properties','Off-Plan Properties'))
    #if registry == "Existing Properties":
        #registry_code = 1
    #else:
        #registry_code = 0
    #villa_area = villa_sales['area_name_en'].unique()
    #select_area = st.sidebar.selectbox('Select area?',villa_area)
    #st.header("Area Market Analysis of : {}".format(select_area))
    st.header(option+" in : {}".format(select_area))
    st.subheader("Villas key metrics")
    st.markdown("The metrics below are calculated based on last 90 days period compared to same period last year (YoY)")
    #select_rooms = st.sidebar.multiselect('Select Flat Rooms', ("1 B/R","2 B/R","3 B/R"),"1 B/R")
    #slider_year = st.sidebar.slider("Period",2010, int(df['year'].max()))
    #start = st.sidebar.date_input("Start Date", value = pd.to_datetime('2010-01-01'))
    #start_day = start.replace(day=1)
    start_day = pd.to_datetime('2010-01-01')
    #end = st.sidebar.date_input("End Date",value = pd.to_datetime('today'))
    #end_day = end.replace(day=1)
    end_day = flat_sales['txs_date'].max()
    #flat_sales = df[(df['trans_group_id']==1)&(df['property_type_id']==3)&(df['property_sub_type_id']==60)]
    #flat_sales_select = flat_sales[(flat_sales['reg_type_id']==registry_code)&(flat_sales['area_name_en'] == select_area)&(flat_sales['fst_day'] >= start_day)&(flat_sales['fst_day'] <= end_day)&(flat_sales['Rooms'] >= 1)&(flat_sales['Rooms']<=4)]
    end_date = flat_sales['txs_date'].max()
    start_date = end_date - datetime.timedelta(days=90)
    #flat_sales_selected_period = flat_sales[(flat_sales['reg_type_id']==registry_code)&(flat_sales['area_name_en']==select_area)&(flat_sales['Room_En'].isin( select_rooms))&(flat_sales['txs_date']<=end_date)&(flat_sales['txs_date']>=start_date)]
    #perf_radio_selection = st.radio("Select Area Performance Range:", options = ['All ranges','more than 20%','btw 5 to 20%','btw -5 & 5%','btw -20 & -5%','less than -20%'],horizontal = True)
    registry = st.radio('Select registry type?',('Existing Properties','Off-Plan Properties'),horizontal = True)
    if registry == "Existing Properties":
        registry_code = 1
    else:
        registry_code = 0
    villa_sales_selected_period = villa_sales[(villa_sales['reg_type_id']==registry_code)&(villa_sales['area_name_en']==select_area)&(villa_sales['txs_date']<=end_date)&(villa_sales['txs_date']>=start_date)&(villa_sales['procedure_area']>=50)&(villa_sales['procedure_area']<=2000)]
    this_period_count = villa_sales_selected_period['transaction_id'].count()
    this_period_median_meter_price = int(villa_sales_selected_period['meter_sale_price'].median()) if this_period_count != 0 else "N/A"
    #if this_period_count != 0:
        #this_period_median_meter_price = int(villa_sales_selected_period['meter_sale_price'].median(skipna = False))
    #else:
        #this_period_median_meter_price = "N/A"
    this_period_median_price = int(villa_sales_selected_period['actual_worth'].median()) if this_period_count != 0 else "N/A"
    #if this_period_count != 0:
        #this_period_median_price = int(villa_sales_selected_period['actual_worth'].median())
    #else:
        #this_period_median_price = "N/A"
    villa_sales_selected_previous_period = villa_sales[(villa_sales['reg_type_id']==registry_code)&(villa_sales['area_name_en']==select_area)&(villa_sales['txs_date']<=end_date - datetime.timedelta(days=365))&(villa_sales['txs_date']>=end_date - datetime.timedelta(days=455))&(villa_sales['procedure_area']>=50)&(villa_sales['procedure_area']<=2000)]
    previous_period_count = villa_sales_selected_previous_period['transaction_id'].count()
    this_period_txs_count_prct_chg = (this_period_count-previous_period_count)/previous_period_count if this_period_count != 0 else 0
    last_period_median_meter_price = villa_sales_selected_previous_period['meter_sale_price'].median()
    this_period_median_meter_price_prct_chg = (this_period_median_meter_price-last_period_median_meter_price)/last_period_median_meter_price if this_period_count != 0 else "N/A"
    last_period_median_price = villa_sales_selected_previous_period['actual_worth'].median() if this_period_count != 0 else "N/A"
    this_period_median_price_prct_chg = (this_period_median_price-last_period_median_price)/last_period_median_price if this_period_count else "N/A"
    this_period_median_villa_size = int(villa_sales_selected_period['procedure_area'].median()) if this_period_count != 0 else "N/A"
    last_period_median_villa_size = villa_sales_selected_previous_period['procedure_area'].median() if this_period_count != 0 else "N/A"
    this_period_median_villa_size_prct_chg = (this_period_median_villa_size-last_period_median_villa_size)/last_period_median_villa_size if this_period_count != 0 else "N/A"
    kpi1,kpi2,kpi3,kpi4 = st.columns(4)
    kpi1.metric("Last 90 Days txs count",f"{this_period_count:,}","{0:.0%}".format(this_period_txs_count_prct_chg))
    kpi2.metric("last 90 Days median meter price : ",f"{this_period_median_meter_price:,}","{0:.0%}".format(this_period_median_meter_price_prct_chg))
    kpi3.metric("Last 90 Days median villa size (SQM) : ",f"{this_period_median_villa_size:,}","{0:.0%}".format(this_period_median_villa_size_prct_chg))
    kpi4.metric("last 90 Days median price : ",f"{this_period_median_price:,}","{0:.0%}".format(this_period_median_price_prct_chg))
    villa_sales_select = villa_sales[(villa_sales['area_name_en'] == select_area)&(villa_sales['procedure_area']>=50)&(villa_sales['procedure_area'] <=2000)&(villa_sales['fst_day'] >= start_day)&(villa_sales['fst_day'] <= end_day)]
    #villa_sales_select['registry'] = villa_sales_select['reg_type_id'].apply(lambda x: "Ready" if x == 1 else "OffPlan")
    single_area_median_prices = pd.DataFrame(villa_sales_select.groupby(['registry','fst_day']).agg(single_area_median_meter_price = ('meter_sale_price','median'),single_area_median_price = ('actual_worth','median'), single_area_txs_count = ('transaction_id','count')))  
    single_area_median_prices_df = single_area_median_prices.reset_index()
    single_area_qtr_median_prices = pd.DataFrame(villa_sales_select.groupby(['registry','fst_qtr']).agg(single_area_qtr_median_meter_price = ('meter_sale_price','median'),single_area_qtr_median_price = ('actual_worth','median'), single_area_txs_count = ('transaction_id','count')))  
    single_area_qtr_median_prices_df = single_area_qtr_median_prices.reset_index()
    #single_area_median_prices_df['rolling_mean'] = single_area_median_prices_df.set_index('fst_day').groupby('Room_En', sort=False)['single_area_median_price'].rolling(6).mean().round(2).to_numpy()
    single_area_median_prices_df['rolling_mean'] = single_area_median_prices_df.set_index('fst_day')['single_area_median_price'].rolling(9).mean().round(2).to_numpy()
    single_area_median_prices_df['meter_rolling_mean'] = single_area_median_prices_df.set_index('fst_day')['single_area_median_meter_price'].rolling(9).mean().round(2).to_numpy()
    single_area_median_prices_df['txs_count_rolling_mean'] = single_area_median_prices_df.set_index('fst_day')['single_area_txs_count'].rolling(9).mean().round(2).to_numpy()
    single_area_median_prices_start_df = single_area_median_prices_df[single_area_median_prices_df['fst_day']==start_day]
    #single_area_median_prices_added_start_df = pd.merge(single_area_median_prices_df,single_area_median_prices_start_df,left_on="Room_En",right_on="Room_En",how = "left")
    #single_area_median_prices_added_start_df['price_pct_chg'] = 100*(single_area_median_prices_added_start_df['single_area_median_price_x']-single_area_median_prices_added_start_df['single_area_median_price_y'])/single_area_median_prices_added_start_df['single_area_median_price_y']
    #single_area_median_prices_added_start_df['meter_price_pct_chg'] = 100*(single_area_median_prices_added_start_df['single_area_median_meter_price_x']-single_area_median_prices_added_start_df['single_area_median_meter_price_y'])/single_area_median_prices_added_start_df['single_area_median_meter_price_y']
    #kpi4,kpi5,kpi6 = st.columns(3)
    #kpi4.metric("Last 90 Days 1 B/R median Price",f"{this_period_1bed_median_price:,}","{0:.0%}".format(this_period_1bed_price_pct_chg))
    #kpi5.metric("Last 90 Days 2 B/R median Price",f"{this_period_2bed_median_price:,}","{0:.0%}".format(this_period_2bed_price_pct_chg))
    #kpi6.metric("Last 90 Days 3 B/R median Price",f"{this_period_3bed_median_price:,}","{0:.0%}".format(this_period_3bed_price_pct_chg))
    st.subheader("Last 90 Days txs Scatter Plot (Price vs Size)")
    villa_sales_scatter_plot = villa_sales[(villa_sales['area_name_en']==select_area)&(villa_sales['txs_date']<=end_date)&(villa_sales['txs_date']>=start_date)&(villa_sales['procedure_area']>=50)&(villa_sales['procedure_area']<=2000)]
    base = alt.Chart(villa_sales_scatter_plot).properties(height=300)
    point = base.mark_circle(size=20).encode(x=alt.X('actual_worth' + ':Q', title="price"), y=alt.Y('procedure_area' + ':Q', title="size"),color=alt.Color('registry', title='registry',legend=alt.Legend(orient='bottom-right')))
    st.altair_chart(point, use_container_width=True)
    #col1, col2 = st.columns(2)
    #with col1:
        #base1 = alt.Chart(single_area_median_prices_df).properties(height=300)
        #line1 = base1.mark_line(size=2).encode(x=alt.X('fst_day', title='Date'),y=alt.Y('single_area_median_price', title='median price'),color=alt.Color('Room_En', title='Flat Size',legend=alt.Legend(orient='right')))
        #st.altair_chart(line1,use_container_width=True)
    #with col2:
        #base2 = alt.Chart(single_area_median_prices_df).properties(height=300)
        #line2 = base2.mark_line(size=2).encode(x=alt.X('fst_day', title='Date'),y=alt.Y('single_area_median_meter_price', title='median meter price'),color=alt.Color('Room_En', title='Flat Size',legend=alt.Legend(orient='right')))
        #st.altair_chart(line2,use_container_width=True)
    #col1,col2 = st.columns(2)
    #with col1:
    st.markdown("##")
    st.subheader("Historical Trend of Villas' Prices and transactions count (Quarterly and 9 months moving average trend)")
    registry_radio_selection = st.radio("Select Villa Registry Type:", options = ['Ready','OffPlan'],horizontal = True)
    villa_sales_qtr_trend = single_area_qtr_median_prices_df[(single_area_qtr_median_prices_df['registry']==registry_radio_selection)]    
    villa_sales_monthly_trend = single_area_median_prices_df[(single_area_median_prices_df['registry'] == registry_radio_selection)]
    #st.markdown("##")
    #st.subheader("Historical Graphs on Villas Prices and Activities Quarterly Trend (median villa price, median meter price & txs count)")
    base5 = alt.Chart(villa_sales_qtr_trend).properties(height=300)
    line5 = base5.mark_bar(size=2).encode(x=alt.X('fst_qtr', title='Date'),y=alt.Y('single_area_qtr_median_price', title='median price'),color=alt.Color('registry', title='registry',legend=alt.Legend(orient='right')))
    #st.altair_chart(line5,use_container_width=True)
    base7 = alt.Chart(villa_sales_qtr_trend).properties(height=300)
    line7 = base7.mark_bar(size=2).encode(x=alt.X('fst_qtr', title='Date'),y=alt.Y('single_area_qtr_median_meter_price', title='meter_median price'),color=alt.Color('registry', title='registry',legend=alt.Legend(orient='right')))
    #st.altair_chart(line7,use_container_width=True)
    base6 = alt.Chart(villa_sales_qtr_trend).properties(height=300)
    line6 = base6.mark_bar(size=2).encode(x=alt.X('fst_qtr', title='Date'),y=alt.Y('single_area_txs_count', title='txs count'),color=alt.Color('registry', title='registry',legend=alt.Legend(orient='right')))
    #st.altair_chart(line6,use_container_width=True)
    #st.subheader("Monthly Moving Averages Graphs (median price, median meter price & txs count)")
    base3 = alt.Chart(villa_sales_monthly_trend).properties(height=300)
    line3 = base3.mark_line(color = 'red').encode(x=alt.X('fst_day', title='Date'),y=alt.Y('rolling_mean', title='rolling median price'))
    #st.altair_chart(line3,use_container_width=True)
    #with col2:
    base4 = alt.Chart(villa_sales_monthly_trend).properties(height=300)
    line4 = base4.mark_line(color = 'red').encode(x=alt.X('fst_day', title='Date'),y=alt.Y('meter_rolling_mean', title='meter rolling median price'))
    #st.altair_chart(line4,use_container_width=True)
    base8 = alt.Chart(villa_sales_monthly_trend).properties(height=300)
    line8 = base8.mark_line(color = 'red').encode(x=alt.X('fst_day', title='Date'),y=alt.Y('txs_count_rolling_mean', title='monthly txs count ma'))
    #st.altair_chart(line8,use_container_width=True)
    #flat_sales_select = flat_sales[(flat_sales['reg_type_en']==registry)]
    chart10 = (line5 + line3)
    chart12 = (line7 + line4)
    chart14 = (line6 + line8)
    tab1, tab2 , tab3 = st.tabs(["Median Prices", "Median Meter Prices", "Transactions Count"])
    with tab1:
        st.altair_chart(chart10,use_container_width=True)
    with tab2:
        st.altair_chart(chart12,use_container_width=True)
    with tab3:
        st.altair_chart(chart14,use_container_width=True)
if  option == 'Comparative Areas Performance (lands)':
    #land_sales = df[(df['trans_group_id']==1)&(df['property_type_id']==1)&(df['procedure_area']<=10000)]
    #land_sales['land_usage'] = land_sales['property_usage_en'].apply(lambda x: land_class(x))

    st.header(option)
    st.markdown("Area performance is determined by the area land median meter price percentage change for the last 90 days period compared to same period last year")
    select_size_range = st.sidebar.selectbox('Select Land Size', ('All Sizes','less than 100','btw 100 to 200','btw 200 to 500','btw 500 to 1000','btw 1000 to 2000','more than 2000 SQM'))
    end_date = land_sales['txs_date'].max()
    start_date = end_date - datetime.timedelta(days=90)
    land_sales['land_size_range'] = land_sales['procedure_area'].apply(lambda x: land_size_range(x))
    if select_size_range == "All Sizes":
        land_sales_selected_period = land_sales[(land_sales['txs_date']<=end_date)&(land_sales['txs_date']>=start_date)]
    else:
        land_sales_selected_period = land_sales[(land_sales['land_size_range'] == select_size_range)&(land_sales['txs_date']<=end_date)&(land_sales['txs_date']>=start_date)]
    land_sales_selected_period_summary = pd.DataFrame(land_sales_selected_period.groupby(['area_name_en']).agg(area_median_meter_price = ('meter_sale_price','median'),area_median_price = ('actual_worth','median'), area_txs_count = ('transaction_id','count'),land_median_size = ('procedure_area','median')))
    land_sales_selected_period_summary_df = land_sales_selected_period_summary.reset_index()
    if select_size_range == "All Sizes":
        land_sales_selected_previous_period = land_sales[(land_sales['txs_date']<=end_date - datetime.timedelta(days=365))&(land_sales['txs_date']>=end_date - datetime.timedelta(days=455))]
    else:
        land_sales_selected_previous_period = land_sales[(land_sales['land_size_range'] == select_size_range)&(land_sales['txs_date']<=end_date - datetime.timedelta(days=365))&(land_sales['txs_date']>=end_date - datetime.timedelta(days=455))]
    land_sales_selected_previous_period_summary = pd.DataFrame(land_sales_selected_previous_period.groupby(['area_name_en']).agg(previous_area_median_meter_price = ('meter_sale_price','median'),previous_area_median_price = ('actual_worth','median'), previous_area_txs_count = ('transaction_id','count')))
    land_sales_selected_previous_period_summary_df = land_sales_selected_previous_period_summary.reset_index()
    merged_current_previous_period = pd.merge(land_sales_selected_period_summary_df,land_sales_selected_previous_period_summary_df,on = "area_name_en",how = "left")
    merged_current_previous_period['median_meter_price_prct_chg'] = 100* (merged_current_previous_period['area_median_meter_price']-merged_current_previous_period['previous_area_median_meter_price'])/merged_current_previous_period['previous_area_median_meter_price']
    merged_current_previous_period['median_price_prct_chg'] = 100 * (merged_current_previous_period['area_median_price']-merged_current_previous_period['previous_area_median_price'])/merged_current_previous_period['previous_area_median_price']
    merged_current_previous_period['area_txs_count_prct_chg'] = 100 * (merged_current_previous_period['area_txs_count']-merged_current_previous_period['previous_area_txs_count'])/merged_current_previous_period['previous_area_txs_count']
    merged_subset = merged_current_previous_period[['area_name_en','area_median_price','median_price_prct_chg','area_median_meter_price','median_meter_price_prct_chg','land_median_size','area_txs_count','area_txs_count_prct_chg']]
    merged_subset['perf_class'] = merged_subset['median_price_prct_chg'].apply(lambda x: perf_class(x))
    #merged_subset.rename(columns = {'area_name_en':'Area Name','area_median_price':'Med. Price','median_price_prct_chg':'% Price Chg','area_median_meter_price':'Med. Mtr Price','median_meter_price_prct_chg':'% Mtr Chg','flat_median_size' : 'Flat Size','area_txs_count':'Txs Count','area_txs_count_prct_chg':'% Txs Chg'},inplace = True)
    #merged_subset['% Price Chg'] = merged_subset['% Price Chg'].astype(float).map("{:.2%}".format)
    #merged_subset['% Mtr Chg'] = merged_subset['% Mtr Chg'].astype(float).map("{:.2%}".format)
    #merged_subset['% Txs Chg'] = merged_subset['% Txs Chg'].astype(float).map("{:.2%}".format)
    #merged_subset['Med. Price'] = merged_subset['Med. Price'].astype(int)
    #merged_subset['Med. Mtr Price'] = merged_subset['Med. Mtr Price'].astype(int)
    #merged_subset['Flat Size'] = merged_subset['Flat Size'].astype(int)
    #print_some_rows = merged_subset.head(5)
    #print(print_some_rows)
    #with st.sidebar:
        #add_radio = st.radio("Sorting Result by:",("Area Name", "Flat Price","Txs Count"))
    st.markdown('###')
    st.header("Interactive Areas Performance Chart")
    #st.markdown('')
    perf_radio_selection = st.radio("Select Area Performance Range:", options = ['All ranges','more than 20%','btw 5 to 20%','btw -5 & 5%','btw -20 & -5%','less than -20%'],horizontal = True)
    #slider1,slider2,slider3= st.columns(3)
    #with slider1:
      #  slider1 = st.slider("Price prct Change Range:",min_value = merged_subset['median_price_prct_chg'].min(),max_value = merged_subset['median_price_prct_chg'].max(),value = (merged_subset['median_price_prct_chg'].min(),merged_subset['median_price_prct_chg'].max()))
    #with slider2:
        #slider2 = st.slider("Txs Count Range :",min_value = float(merged_subset['area_txs_count'].min()),max_value=float(merged_subset['area_txs_count'].max()), value = (float(merged_subset['area_txs_count'].min()),float(merged_subset['area_txs_count'].max())),step = 10.0)
    #with slider3:
        #slider3 = st.slider("Meter Price Range :",min_value = merged_subset['area_median_meter_price'].min(),max_value = merged_subset['area_median_meter_price'].max(),value = (merged_subset['area_median_meter_price'].min(),merged_subset['area_median_meter_price'].max()))
    if perf_radio_selection == "All ranges":
        reduced_merged = merged_subset
    else: reduced_merged = merged_subset[(merged_subset['perf_class'] == perf_radio_selection)]
    base10 = alt.Chart(reduced_merged).properties(height=300)
    point10 = base10.mark_circle(size=20).encode(x=alt.X('area_median_price' + ':Q', title="price"), y=alt.Y('area_median_meter_price' + ':Q', title="Meter Price"),size = 'area_txs_count', tooltip = ['area_name_en','area_txs_count','area_median_price','area_median_meter_price','land_median_size','median_price_prct_chg'],color=alt.Color('perf_class', title='Area Med. Value vs Size',legend=alt.Legend(orient='right'))).interactive()
    #point10_text = base10.mark_text
    #point10 = base10.mark_point(size=20).encode(x=alt.X('area_median_price' + ':Q', title="price"), y=alt.Y('flat_median_size' + ':Q', title="Flat Size"),size = 'area_txs_count')
    #text = point10.mark_text(align='left',baseline='middle',dx=1).encode(text='area_name_en')
    #point10 + text
    st.altair_chart(point10, use_container_width=True)
    st.markdown('###')
    st.subheader('Areas Performance Details (for selected performance range)')
    st.dataframe(reduced_merged)
if  option == 'Area Specific Lands Prices Analysis':
    #land_sales = df[(df['trans_group_id']==1)&(df['property_type_id']==1)&(df['procedure_area']<=10000)]
    #land_sales['land_usage'] = land_sales['property_usage_en'].apply(lambda x: land_class(x))

    land_area = land_sales['area_name_en'].unique()
    select_area = st.sidebar.selectbox('Select area?',land_area)
    st.header(option+" in : {}".format(select_area))
    st.subheader("Lands key metrics")
    st.markdown("The metrics below are calculated based on last 90 days period lands prices compared to same period last year (YoY)")
    #select_rooms = st.sidebar.multiselect('Select Flat Rooms', ("1 B/R","2 B/R","3 B/R"),"1 B/R")
    #slider_year = st.sidebar.slider("Period",2010, int(df['year'].max()))
    #start = st.sidebar.date_input("Start Date", value = pd.to_datetime('2010-01-01'))
    #start_day = start.replace(day=1)
    start_day = pd.to_datetime('2010-01-01')
    #end = st.sidebar.date_input("End Date",value = pd.to_datetime('today'))
    #end_day = end.replace(day=1)
    end_day = land_sales['txs_date'].max()
    #flat_sales = df[(df['trans_group_id']==1)&(df['property_type_id']==3)&(df['property_sub_type_id']==60)]
    #flat_sales_select = flat_sales[(flat_sales['reg_type_id']==registry_code)&(flat_sales['area_name_en'] == select_area)&(flat_sales['fst_day'] >= start_day)&(flat_sales['fst_day'] <= end_day)&(flat_sales['Rooms'] >= 1)&(flat_sales['Rooms']<=4)]
    end_date = land_sales['txs_date'].max()
    start_date = end_date - datetime.timedelta(days=90)
    #flat_sales_selected_period = flat_sales[(flat_sales['reg_type_id']==registry_code)&(flat_sales['area_name_en']==select_area)&(flat_sales['Room_En'].isin( select_rooms))&(flat_sales['txs_date']<=end_date)&(flat_sales['txs_date']>=start_date)]
    #perf_radio_selection = st.radio("Select Area Performance Range:", options = ['All ranges','more than 20%','btw 5 to 20%','btw -5 & 5%','btw -20 & -5%','less than -20%'],horizontal = True)
    land_sales_selected_period = land_sales[(land_sales['area_name_en']==select_area)&(land_sales['txs_date']<=end_date)&(land_sales['txs_date']>=start_date)&(land_sales['procedure_area']>=50)&(land_sales['procedure_area']<=10000)]
    this_period_count = land_sales_selected_period['transaction_id'].count()
    this_period_median_meter_price = int(land_sales_selected_period['meter_sale_price'].median()) if this_period_count != 0 else 0
    #if this_period_count != 0:
        #this_period_median_meter_price = int(villa_sales_selected_period['meter_sale_price'].median(skipna = False))
    #else:
        #this_period_median_meter_price = "N/A"
    this_period_median_price = int(land_sales_selected_period['actual_worth'].median()) if this_period_count != 0 else 0
    #if this_period_count != 0:
        #this_period_median_price = int(villa_sales_selected_period['actual_worth'].median())
    #else:
        #this_period_median_price = "N/A"
    land_sales_selected_previous_period = land_sales[(land_sales['area_name_en']==select_area)&(land_sales['txs_date']<=end_date - datetime.timedelta(days=365))&(land_sales['txs_date']>=end_date - datetime.timedelta(days=455))&(land_sales['procedure_area']>=50)&(land_sales['procedure_area']<=10000)]
    previous_period_count = land_sales_selected_previous_period['transaction_id'].count()
    this_period_txs_count_prct_chg = (this_period_count-previous_period_count)/previous_period_count if this_period_count != 0 else 0
    last_period_median_meter_price = land_sales_selected_previous_period['meter_sale_price'].median() if this_period_count != 0 else 0
    this_period_median_meter_price_prct_chg = (this_period_median_meter_price-last_period_median_meter_price)/last_period_median_meter_price if this_period_count != 0 else 0
    last_period_median_price = land_sales_selected_previous_period['actual_worth'].median() if this_period_count != 0 else 0
    this_period_median_price_prct_chg = (this_period_median_price-last_period_median_price)/last_period_median_price if this_period_count else 0
    this_period_median_land_size = int(land_sales_selected_period['procedure_area'].median()) if this_period_count != 0 else 0
    last_period_median_land_size = land_sales_selected_previous_period['procedure_area'].median() if this_period_count != 0 else 0
    this_period_median_land_size_prct_chg = (this_period_median_land_size-last_period_median_land_size)/last_period_median_land_size if this_period_count != 0 else 0
    kpi1,kpi2,kpi3,kpi4 = st.columns(4)
    kpi1.metric("Last 90 Days txs count",f"{this_period_count:,}","{0:.0%}".format(this_period_txs_count_prct_chg))
    kpi2.metric("last 90 Days median meter price : ",f"{this_period_median_meter_price:,}","{0:.0%}".format(this_period_median_meter_price_prct_chg))
    kpi3.metric("Last 90 Days median land size (SQM) : ",f"{this_period_median_land_size:,}","{0:.0%}".format(this_period_median_land_size_prct_chg))
    kpi4.metric("last 90 Days median price : ",f"{this_period_median_price:,}","{0:.0%}".format(this_period_median_price_prct_chg))
    land_sales_select = land_sales[(land_sales['area_name_en'] == select_area)&(land_sales['procedure_area']>=50)&(land_sales['procedure_area'] <=10000)&(land_sales['fst_day'] >= start_day)&(land_sales['fst_day'] <= end_day)]
    #villa_sales_select['registry'] = villa_sales_select['reg_type_id'].apply(lambda x: "Ready" if x == 1 else "OffPlan")
    single_area_median_prices = pd.DataFrame(land_sales_select.groupby(['land_usage','fst_day']).agg(single_area_median_meter_price = ('meter_sale_price','median'),single_area_median_price = ('actual_worth','median'), single_area_txs_count = ('transaction_id','count')))  
    single_area_median_prices_df = single_area_median_prices.reset_index()
    single_area_qtr_median_prices = pd.DataFrame(land_sales_select.groupby(['land_usage','fst_qtr']).agg(single_area_qtr_median_meter_price = ('meter_sale_price','median'),single_area_qtr_median_price = ('actual_worth','median'), single_area_txs_count = ('transaction_id','count')))  
    single_area_qtr_median_prices_df = single_area_qtr_median_prices.reset_index()
    #single_area_median_prices_df['rolling_mean'] = single_area_median_prices_df.set_index('fst_day').groupby('Room_En', sort=False)['single_area_median_price'].rolling(6).mean().round(2).to_numpy()
    single_area_median_prices_df['rolling_mean'] = single_area_median_prices_df.set_index('fst_day').groupby('land_usage',sort = False)['single_area_median_price'].rolling(6).mean().round(2).to_numpy()
    single_area_median_prices_df['meter_rolling_mean'] = single_area_median_prices_df.set_index('fst_day')['single_area_median_meter_price'].rolling(6).mean().round(2).to_numpy()
    single_area_median_prices_df['txs_count_rolling_mean'] = single_area_median_prices_df.set_index('fst_day')['single_area_txs_count'].rolling(6).mean().round(2).to_numpy()
    single_area_median_prices_start_df = single_area_median_prices_df[single_area_median_prices_df['fst_day']==start_day]
    #single_area_median_prices_added_start_df = pd.merge(single_area_median_prices_df,single_area_median_prices_start_df,left_on="Room_En",right_on="Room_En",how = "left")
    #single_area_median_prices_added_start_df['price_pct_chg'] = 100*(single_area_median_prices_added_start_df['single_area_median_price_x']-single_area_median_prices_added_start_df['single_area_median_price_y'])/single_area_median_prices_added_start_df['single_area_median_price_y']
    #single_area_median_prices_added_start_df['meter_price_pct_chg'] = 100*(single_area_median_prices_added_start_df['single_area_median_meter_price_x']-single_area_median_prices_added_start_df['single_area_median_meter_price_y'])/single_area_median_prices_added_start_df['single_area_median_meter_price_y']
    #kpi4,kpi5,kpi6 = st.columns(3)
    #kpi4.metric("Last 90 Days 1 B/R median Price",f"{this_period_1bed_median_price:,}","{0:.0%}".format(this_period_1bed_price_pct_chg))
    #kpi5.metric("Last 90 Days 2 B/R median Price",f"{this_period_2bed_median_price:,}","{0:.0%}".format(this_period_2bed_price_pct_chg))
    #kpi6.metric("Last 90 Days 3 B/R median Price",f"{this_period_3bed_median_price:,}","{0:.0%}".format(this_period_3bed_price_pct_chg))
    st.subheader("Last 90 Days txs Scatter Plot (Price vs Size)")
    land_sales_scatter_plot = land_sales[(land_sales['area_name_en']==select_area)&(land_sales['txs_date']<=end_date)&(land_sales['txs_date']>=start_date)&(land_sales['procedure_area']>=50)&(land_sales['procedure_area']<=10000)]
    base = alt.Chart(land_sales_scatter_plot).properties(height=300)
    point = base.mark_circle(size=20).encode(x=alt.X('actual_worth' + ':Q', title="price"), y=alt.Y('procedure_area' + ':Q', title="size"),color=alt.Color('land_usage', title='Usage',legend=alt.Legend(orient='bottom-right')))
    st.altair_chart(point, use_container_width=True)
    #col1, col2 = st.columns(2)
    #with col1:
        #base1 = alt.Chart(single_area_median_prices_df).properties(height=300)
        #line1 = base1.mark_line(size=2).encode(x=alt.X('fst_day', title='Date'),y=alt.Y('single_area_median_price', title='median price'),color=alt.Color('Room_En', title='Flat Size',legend=alt.Legend(orient='right')))
        #st.altair_chart(line1,use_container_width=True)
    #with col2:
        #base2 = alt.Chart(single_area_median_prices_df).properties(height=300)
        #line2 = base2.mark_line(size=2).encode(x=alt.X('fst_day', title='Date'),y=alt.Y('single_area_median_meter_price', title='median meter price'),color=alt.Color('Room_En', title='Flat Size',legend=alt.Legend(orient='right')))
        #st.altair_chart(line2,use_container_width=True)
    #col1,col2 = st.columns(2)
    #with col1:
    st.markdown("##")
    st.subheader("Historical Trend of Lands' Prices and transactions count (Quarterly and 9 months moving average trend)")
    usage_radio_selection = st.radio("Select Land Usage Type:", options = ['Commercial','Residential','Industrial'],horizontal = True)    
    land_sales_qtr_trend = single_area_qtr_median_prices_df[(single_area_qtr_median_prices_df['land_usage']==usage_radio_selection)]    
    land_sales_monthly_trend = single_area_median_prices_df[(single_area_median_prices_df['land_usage'] == usage_radio_selection)]
    #st.markdown("##")
    #st.subheader("Historical Graphs on Lands Prices and Activities Quarterly Trend (median villa price, median meter price & txs count)")
    base5 = alt.Chart(land_sales_qtr_trend).properties(height=300)
    line5 = base5.mark_bar(size=2).encode(x=alt.X('fst_qtr', title='Date'),y=alt.Y('single_area_qtr_median_price', title='median price'),color=alt.Color('land_usage', title='Usage',legend=alt.Legend(orient='right')))
    #st.altair_chart(line5,use_container_width=True)
    base7 = alt.Chart(land_sales_qtr_trend).properties(height=300)
    line7 = base7.mark_bar(size=2).encode(x=alt.X('fst_qtr', title='Date'),y=alt.Y('single_area_qtr_median_meter_price', title='meter_median price'),color=alt.Color('land_usage', title='Usage',legend=alt.Legend(orient='right')))
    #st.altair_chart(line7,use_container_width=True)
    base6 = alt.Chart(land_sales_qtr_trend).properties(height=300)
    line6 = base6.mark_bar(size=2).encode(x=alt.X('fst_qtr', title='Date'),y=alt.Y('single_area_txs_count', title='txs count'),color=alt.Color('land_usage', title='Usage',legend=alt.Legend(orient='right')))
    #st.altair_chart(line6,use_container_width=True)
    #st.subheader("Monthly Moving Averages Graphs (median price, median meter price & txs count)")
    base3 = alt.Chart(land_sales_monthly_trend).properties(height=300)
    line3 = base3.mark_line(color = 'red').encode(x=alt.X('fst_day', title='Date'),y=alt.Y('rolling_mean', title='rolling median price'))
    #st.altair_chart(line3,use_container_width=True)
    #with col2:
    base4 = alt.Chart(land_sales_monthly_trend).properties(height=300)
    line4 = base4.mark_line(color = 'red').encode(x=alt.X('fst_day', title='Date'),y=alt.Y('meter_rolling_mean', title='meter rolling median price'))
    #st.altair_chart(line4,use_container_width=True)
    base8 = alt.Chart(land_sales_monthly_trend).properties(height=300)
    line8 = base8.mark_line(color = 'red').encode(x=alt.X('fst_day', title='Date'),y=alt.Y('txs_count_rolling_mean', title='monthly txs count ma'))
    #st.altair_chart(line8,use_container_width=True)
    chart10 = (line5 + line3)
    chart11 = (line7 + line4)
    chart12 = (line6 + line8)
    tab1, tab2 , tab3 = st.tabs(["Median Prices", "Median Meter Prices", "Transactions Count"])
    with tab1:
        st.altair_chart(chart10,use_container_width=True)
    with tab2:
        st.altair_chart(chart11,use_container_width=True)
    with tab3:
        st.altair_chart(chart12,use_container_width=True)
    
if  option == 'Market Historical Trend':
    registry = st.sidebar.radio("Select Flat/Villa Registry:", options = ['Existing Properties','Off-Plan Properties'],horizontal = True)
    if registry == "Existing Properties":
        registry_code = 1
    else:
        registry_code = 0
    st.header(option)
    st.markdown("Market trend is represented by the Composite Prices Trend of flats, villas and lands. Composite prices are calculated as the sum of weighted area prices (where weights represent the relative value of transactions activities in each area for each calendar period/quarter)")
    st.markdown('###')
    st.subheader("Flats Composite Prices Trend")
    #registry = st.sidebar.radio("Select Flat Registry:", options = ['Existing Properties','Off-Plan Properties'],horizontal = True)
    #if registry == "Existing Properties":
        #registry_code = 1
    #else:
        #registry_code = 0
    
    start_day = pd.to_datetime('2010-01-01')
    flat_start_day = start_day
    end_day = flat_sales['txs_date'].max()
    end_date = flat_sales['txs_date'].max()
    start_date = end_date - datetime.timedelta(days=90)
    flat_sales_select = flat_sales[(flat_sales['txs_date']<=end_day)&(flat_sales['txs_date']>=start_day)&(flat_sales['Rooms']>=2)&(flat_sales['Rooms']<=4)&(flat_sales['reg_type_id'] == registry_code)]
    all_registry_rooms_area_qtr_median_prices = pd.DataFrame(flat_sales_select.groupby(['registry','Room_En','area_name_en','fst_qtr']).agg(qtr_median_meter_price = ('meter_sale_price','median'),qtr_median_price = ('actual_worth','median'), txs_count = ('transaction_id','count'))).reset_index()
    #st.dataframe(all_registry_rooms_area_qtr_median_prices)
    all_registry_rooms_qtr_median_prices = pd.DataFrame(all_registry_rooms_area_qtr_median_prices.groupby(['registry','Room_En','fst_qtr']).agg(qtr_txs = ('txs_count','sum'))).reset_index()
    #st.dataframe(all_registry_rooms_qtr_median_prices)
    #test = tot_count("OffPlan","1 B/R","2011-04-01")
    #st.write(test)
    #all_registry_rooms_area_qtr_median_prices['relative_weight'] = all_registry_rooms_area_qtr_median_prices.apply(lambda x:x['txs_count']/tot_count(x['registry'],x['Room_En'],x['fst_qtr']),axis = 1)
    #st.dataframe(all_registry_rooms_area_qtr_median_prices)
    area_summary_copy = all_registry_rooms_area_qtr_median_prices.copy(deep = True)
    #st.dataframe(area_summary_copy)
    area_summary_copy['relative_weight'] = area_summary_copy.apply(lambda x:x['txs_count']/tot_count(x['registry'],x['Room_En'],x['fst_qtr']),axis = 1)
    area_summary_copy['relative_price'] = area_summary_copy.apply(lambda x:(x['relative_weight'])*(x['qtr_median_price']),axis = 1)
    #st.dataframe(area_summary_copy)
    all_registry_rooms_qtr_median_prices['composite_median_price'] = all_registry_rooms_qtr_median_prices.apply(lambda x:agg_area_prices(x['registry'],x['Room_En'],x['fst_qtr']),axis=1)
    #st.dataframe(all_registry_rooms_qtr_median_prices)
    #st.markdown("##")
    #st.subheader("Historical Graphs on Flats Prices and Activities Quarterly Trend (median flat price, median meter price & txs count)")
    flat_sales_select_period = flat_sales_select[flat_sales_select['txs_date']>=start_date]
    period_flat_count = flat_sales_select_period['transaction_id'].count()
    period_registry_rooms_area_median_prices = pd.DataFrame(flat_sales_select_period.groupby(['registry','Room_En','area_name_en']).agg(period_median_meter_price = ('meter_sale_price','median'),period_median_price = ('actual_worth','median'), txs_count = ('transaction_id','count'))).reset_index()
    period_registry_rooms_median_prices = pd.DataFrame(period_registry_rooms_area_median_prices.groupby(['registry','Room_En']).agg(period_txs = ('txs_count','sum'))).reset_index()
    period_area_summary_copy = period_registry_rooms_area_median_prices.copy(deep = True)
    period_area_summary_copy['relative_weight'] = period_area_summary_copy.apply(lambda x:x['txs_count']/period_count(x['Room_En'],x['registry']),axis = 1)
    period_area_summary_copy['relative_price'] = period_area_summary_copy.apply(lambda x:(x['relative_weight'])*(x['period_median_price']),axis = 1)
    #period_registry_rooms_median_prices['period_composite_median_price'] = period_registry_rooms_median_prices.apply(lambda x:agg_area_prices(x['registry'],x['Room_En'],x['fst_qtr']),axis=1)
    period_1BD = period_area_summary_copy[(period_area_summary_copy.Room_En == "1 B/R")]
    period_1BD_composite = int(period_1BD['relative_price'].sum())
    initial_1BD = all_registry_rooms_qtr_median_prices[(all_registry_rooms_qtr_median_prices.Room_En == "1 B/R")&(all_registry_rooms_qtr_median_prices.fst_qtr == '2010-01-01')]
    initial_1BD_composite = initial_1BD['composite_median_price'].sum()
    period_1BD_composite_prct_chg = (period_1BD_composite - initial_1BD_composite) / initial_1BD_composite
    period_2BD = period_area_summary_copy[(period_area_summary_copy.Room_En == "2 B/R")]
    period_2BD_composite = int(period_2BD['relative_price'].sum())
    initial_2BD = all_registry_rooms_qtr_median_prices[(all_registry_rooms_qtr_median_prices.Room_En == "2 B/R")&(all_registry_rooms_qtr_median_prices.fst_qtr == '2010-01-01')]
    initial_2BD_composite = initial_2BD['composite_median_price'].sum()
    period_2BD_composite_prct_chg = (period_2BD_composite - initial_2BD_composite) / initial_2BD_composite
    period_3BD = period_area_summary_copy[(period_area_summary_copy.Room_En == "3 B/R")]
    period_3BD_composite = int(period_3BD['relative_price'].sum())
    initial_3BD = all_registry_rooms_qtr_median_prices[(all_registry_rooms_qtr_median_prices.Room_En == "3 B/R")&(all_registry_rooms_qtr_median_prices.fst_qtr == '2010-01-01')]
    initial_3BD_composite = initial_3BD['composite_median_price'].sum()
    period_3BD_composite_prct_chg = (period_3BD_composite - initial_3BD_composite) / initial_3BD_composite
    base1 = alt.Chart(all_registry_rooms_qtr_median_prices).properties(height=300)
    line1 = base1.mark_line(size=2).encode(x=alt.X('fst_qtr', title='Date'),y=alt.Y('composite_median_price', title='Composite Median Price'),tooltip = ['fst_qtr','Room_En','composite_median_price','qtr_txs'],color=alt.Color('Room_En', title='Flat Size',legend=alt.Legend(orient='right')))
    st.altair_chart(line1,use_container_width=True)
    st.markdown("Flats Current Market performance is measured by the percent change of composite price for last 90 days compared to initial period (first quarter of 2010). Performance is shown by the three indicators below:")
    kpi1,kpi2,kpi3 = st.columns(3)
    kpi1.metric("Last 90 Days 1 B/R composite median Price",f"{period_1BD_composite:,}","{0:.0%}".format(period_1BD_composite_prct_chg))
    kpi2.metric("Last 90 Days 2 B/R composite median Price",f"{period_2BD_composite:,}","{0:.0%}".format(period_2BD_composite_prct_chg))
    kpi3.metric("Last 90 Days 3 B/R composite median Price",f"{period_3BD_composite:,}","{0:.0%}".format(period_3BD_composite_prct_chg))
    #base1 = alt.Chart(all_registry_rooms_qtr_median_prices).properties(height=300)
    #line1 = base1.mark_line(size=2).encode(x=alt.X('fst_qtr', title='Date'),y=alt.Y('composite_median_price', title='Composite Median Price'),tooltip = ['fst_qtr','Room_En','composite_median_price','qtr_txs'],color=alt.Color('Room_En', title='Flat Size',legend=alt.Legend(orient='right')))
    #st.altair_chart(line1,use_container_width=True)
    
    st.markdown('###')
    st.subheader("Villas Composite Prices Trend")
    villa_sales['size_range'] = villa_sales['procedure_area'].apply(lambda x: size_range(x))
    start_day = pd.to_datetime('2010-01-01')
    end_day = villa_sales['txs_date'].max()
    end_date = villa_sales['txs_date'].max()
    start_date = end_date - datetime.timedelta(days=90)
    villa_sales_select = villa_sales[(villa_sales['txs_date']<=end_day)&(villa_sales['txs_date']>=start_day)&(villa_sales['reg_type_id'] == registry_code)]
    all_registry_size_area_qtr_median_prices = pd.DataFrame(villa_sales_select.groupby(['registry','size_range','area_name_en','fst_qtr']).agg(qtr_median_meter_price = ('meter_sale_price','median'),qtr_median_price = ('actual_worth','median'), txs_count = ('transaction_id','count'))).reset_index()
    #st.dataframe(all_registry_size_area_qtr_median_prices)
    all_registry_size_qtr_median_prices = pd.DataFrame(all_registry_size_area_qtr_median_prices.groupby(['registry','size_range','fst_qtr']).agg(qtr_txs = ('txs_count','sum'))).reset_index()
    #st.dataframe(all_registry_size_qtr_median_prices)
    #test = tot_count("OffPlan","1 B/R","2011-04-01")
    #st.write(test)
    #all_registry_rooms_area_qtr_median_prices['relative_weight'] = all_registry_rooms_area_qtr_median_prices.apply(lambda x:x['txs_count']/tot_count(x['registry'],x['Room_En'],x['fst_qtr']),axis = 1)
    #st.dataframe(all_registry_rooms_area_qtr_median_prices)
    area_villa_summary_copy = all_registry_size_area_qtr_median_prices.copy(deep = True)
    area_villa_summary_copy['relative_weight'] = area_villa_summary_copy.apply(lambda x:x['txs_count']/tot_villa_count(x['registry'],x['size_range'],x['fst_qtr']),axis = 1)
    #st.dataframe(area_villa_summary_copy)
    area_villa_summary_copy['relative_price'] = area_villa_summary_copy.apply(lambda x:(x['relative_weight'])*(x['qtr_median_price']),axis = 1)
    #st.dataframe(area_summary_copy)
    all_registry_size_qtr_median_prices['composite_villa_median_price'] = all_registry_size_qtr_median_prices.apply(lambda x:agg_villa_area_prices(x['registry'],x['size_range'],x['fst_qtr']),axis=1)
    #st.dataframe(all_registry_size_qtr_median_prices)
    #st.markdown("##")
    #st.subheader("Historical Graphs on Flats Prices and Activities Quarterly Trend (median flat price, median meter price & txs count)")
    villa_sales_select_period = villa_sales_select[villa_sales_select['txs_date']>=start_date]
    #period_villa_count = villa_sales_select_period['transaction_id'].count()
    period_registry_size_area_median_prices = pd.DataFrame(villa_sales_select_period.groupby(['registry','size_range','area_name_en']).agg(period_median_meter_price = ('meter_sale_price','median'),period_median_price = ('actual_worth','median'), txs_count = ('transaction_id','count'))).reset_index()
    period_registry_size_median_prices = pd.DataFrame(period_registry_size_area_median_prices.groupby(['registry','size_range']).agg(period_txs = ('txs_count','sum'))).reset_index()
    period_villa_area_summary_copy = period_registry_size_area_median_prices.copy(deep = True)
    period_villa_area_summary_copy['relative_weight'] = period_villa_area_summary_copy.apply(lambda x:x['txs_count']/period_villa_count(x['size_range'],x['registry']),axis = 1)
    period_villa_area_summary_copy['relative_price'] = period_villa_area_summary_copy.apply(lambda x:(x['relative_weight'])*(x['period_median_price']),axis = 1)
    #period_registry_rooms_median_prices['period_composite_median_price'] = period_registry_rooms_median_prices.apply(lambda x:agg_area_prices(x['registry'],x['Room_En'],x['fst_qtr']),axis=1)
    period_small = period_villa_area_summary_copy[(period_villa_area_summary_copy.size_range == "less than 300")]
    period_small_composite = int(period_small['relative_price'].sum())
    initial_small = all_registry_size_qtr_median_prices[(all_registry_size_qtr_median_prices.size_range == "less than 300")&(all_registry_size_qtr_median_prices.fst_qtr == '2010-01-01')]
    initial_small_composite = initial_small['composite_villa_median_price'].sum()
    period_small_composite_prct_chg = (period_small_composite - initial_small_composite) / initial_small_composite
    period_medium = period_villa_area_summary_copy[(period_villa_area_summary_copy.size_range == "btw 300 to 600")]
    period_medium_composite = int(period_medium['relative_price'].sum())
    initial_medium = all_registry_size_qtr_median_prices[(all_registry_size_qtr_median_prices.size_range == "btw 300 to 600")&(all_registry_size_qtr_median_prices.fst_qtr == '2010-01-01')]
    initial_medium_composite = initial_medium['composite_villa_median_price'].sum()
    period_medium_composite_prct_chg = (period_medium_composite - initial_medium_composite) / initial_medium_composite
    period_large = period_villa_area_summary_copy[(period_villa_area_summary_copy.size_range == "more than 600 SQM")]
    period_large_composite = int(period_large['relative_price'].sum())
    initial_large = all_registry_size_qtr_median_prices[(all_registry_size_qtr_median_prices.size_range == "more than 600 SQM")&(all_registry_size_qtr_median_prices.fst_qtr == '2010-01-01')]
    initial_large_composite = initial_large['composite_villa_median_price'].sum()
    period_large_composite_prct_chg = (period_large_composite - initial_large_composite) / initial_large_composite
    
    base2 = alt.Chart(all_registry_size_qtr_median_prices).properties(height=300)
    line2 = base2.mark_line(size=2).encode(x=alt.X('fst_qtr', title='Date'),y=alt.Y('composite_villa_median_price', title='Composite Median Price'), tooltip = ['fst_qtr','size_range','composite_villa_median_price','qtr_txs'],color=alt.Color('size_range', title='Size Range',legend=alt.Legend(orient='right')))
    st.altair_chart(line2,use_container_width=True) 
    st.markdown("Villas Current Market performance is measured by the percent change of composite price for last 90 days compared to initial period (first quarter of 2010). Performance is shown by the three indicators below:")
    kpi1,kpi2,kpi3 = st.columns(3)
    kpi1.metric("Last 90 Days Small composite median Price",f"{period_small_composite:,}","{0:.0%}".format(period_small_composite_prct_chg))
    kpi2.metric("Last 90 Days Medium composite median Price",f"{period_medium_composite:,}","{0:.0%}".format(period_medium_composite_prct_chg))
    kpi3.metric("Last 90 Days Large composite median Price",f"{period_large_composite:,}","{0:.0%}".format(period_large_composite_prct_chg))
    
    #base2 = alt.Chart(all_registry_size_qtr_median_prices).properties(height=300)
    #line2 = base2.mark_line(size=2).encode(x=alt.X('fst_qtr', title='Date'),y=alt.Y('composite_villa_median_price', title='Composite Median Price'), tooltip = ['fst_qtr','size_range','composite_villa_median_price','qtr_txs'],color=alt.Color('size_range', title='Size Range',legend=alt.Legend(orient='right')))
    #st.altair_chart(line2,use_container_width=True) 
    
    st.markdown('###')
    st.subheader("Lands Composite Prices Trend")
    land_sales['size_range'] = land_sales['procedure_area'].apply(lambda x: land_size_range(x))
    start_day = pd.to_datetime('2010-01-01')
    #start_day = datetime.datetime(2010,1,1)
    end_day = land_sales['txs_date'].max()
    end_date = land_sales['txs_date'].max()
    start_date = end_date - datetime.timedelta(days=90)
    land_sales_select = land_sales[(land_sales['txs_date']<=end_day)&(land_sales['txs_date']>=start_day)]
    land_sales_select = land_sales_select[land_sales_select['land_usage'].isin(['Commercial','Residential'])]
    all_usage_area_qtr_median_meter_prices = pd.DataFrame(land_sales_select.groupby(['land_usage','area_name_en','fst_qtr']).agg(qtr_median_meter_price = ('meter_sale_price','median'),qtr_median_price = ('actual_worth','median'), txs_count = ('transaction_id','count'))).reset_index()
    #st.dataframe(all_usage_area_qtr_median_meter_prices)
    all_usage_qtr_median_meter_prices = pd.DataFrame(all_usage_area_qtr_median_meter_prices.groupby(['land_usage','fst_qtr']).agg(qtr_txs = ('txs_count','sum'))).reset_index()
    #st.dataframe(all_usage_qtr_median_meter_prices)
    #test = tot_count("OffPlan","1 B/R","2011-04-01")
    #st.write(test)
    #all_registry_rooms_area_qtr_median_prices['relative_weight'] = all_registry_rooms_area_qtr_median_prices.apply(lambda x:x['txs_count']/tot_count(x['registry'],x['Room_En'],x['fst_qtr']),axis = 1)
    #st.dataframe(all_registry_rooms_area_qtr_median_prices)
    area_land_summary_copy = all_usage_area_qtr_median_meter_prices.copy(deep = True)
    area_land_summary_copy['relative_weight'] = area_land_summary_copy.apply(lambda x:x['txs_count']/tot_land_count(x['land_usage'],x['fst_qtr']),axis = 1)
    #st.dataframe(area_land_summary_copy)
    area_land_summary_copy['relative_meter_price'] = area_land_summary_copy.apply(lambda x:(x['relative_weight'])*(x['qtr_median_meter_price']),axis = 1)
    #st.dataframe(area_land_summary_copy)
    all_usage_qtr_median_meter_prices['composite_land_median_meter_price'] = all_usage_qtr_median_meter_prices.apply(lambda x:agg_land_area_prices(x['land_usage'],x['fst_qtr']),axis=1)
    #st.dataframe(all_usage_qtr_median_meter_prices)
    #st.markdown("##")
    #st.subheader("Historical Graphs on Flats Prices and Activities Quarterly Trend (median flat price, median meter price & txs count)")
    land_sales_select_period = land_sales_select[land_sales_select['txs_date']>=start_date]
    #period_villa_count = villa_sales_select_period['transaction_id'].count()
    period_usage_area_median_prices = pd.DataFrame(land_sales_select_period.groupby(['land_usage','area_name_en']).agg(period_median_meter_price = ('meter_sale_price','median'),period_median_price = ('actual_worth','median'), txs_count = ('transaction_id','count'))).reset_index()
    period_usage_median_prices = pd.DataFrame(period_usage_area_median_prices.groupby(['land_usage']).agg(period_txs = ('txs_count','sum'))).reset_index()
    period_land_area_summary_copy = period_usage_area_median_prices.copy(deep = True)
    period_land_area_summary_copy['relative_weight'] = period_land_area_summary_copy.apply(lambda x:x['txs_count']/period_land_count(x['land_usage']),axis = 1)
    period_land_area_summary_copy['relative_price'] = period_land_area_summary_copy.apply(lambda x:(x['relative_weight'])*(x['period_median_meter_price']),axis = 1)
    #period_registry_rooms_median_prices['period_composite_median_price'] = period_registry_rooms_median_prices.apply(lambda x:agg_area_prices(x['registry'],x['Room_En'],x['fst_qtr']),axis=1)
    period_Commercial = period_land_area_summary_copy[(period_land_area_summary_copy.land_usage == "Commercial")]
    period_Commercial_composite = int(period_Commercial['relative_price'].sum())
    initial_Commercial = all_usage_qtr_median_meter_prices[(all_usage_qtr_median_meter_prices.land_usage == "Commercial")&(all_usage_qtr_median_meter_prices.fst_qtr == '2010-01-01')]
    initial_Commercial_composite = initial_Commercial['composite_land_median_meter_price'].sum()
    period_Commercial_composite_prct_chg = (period_Commercial_composite - initial_Commercial_composite) / initial_Commercial_composite
    
    period_Residential = period_land_area_summary_copy[(period_land_area_summary_copy.land_usage == "Residential")]
    period_Residential_composite = int(period_Residential['relative_price'].sum())
    initial_Residential = all_usage_qtr_median_meter_prices[(all_usage_qtr_median_meter_prices.land_usage == "Residential")&(all_usage_qtr_median_meter_prices.fst_qtr == '2010-01-01')]
    initial_Residential_composite = initial_Residential['composite_land_median_meter_price'].sum()
    period_Residential_composite_prct_chg = (period_Residential_composite - initial_Residential_composite) / initial_Residential_composite
    base3 = alt.Chart(all_usage_qtr_median_meter_prices).properties(height=300)
    line3 = base3.mark_line(size=2).encode(x=alt.X('fst_qtr', title='Date'),y=alt.Y('composite_land_median_meter_price', title='Composite Median Meter Price'), tooltip = ['fst_qtr','land_usage','composite_land_median_meter_price','qtr_txs'],color=alt.Color('land_usage', title='Land Usage',legend=alt.Legend(orient='right')))
    st.altair_chart(line3,use_container_width=True)     
    st.markdown("Lands Current Market performance is measured by the percent change of composite price for last 90 days compared to initial period (first quarter of 2010). Performance is shown by the three indicators below:")
    kpi1,kpi2 = st.columns(2)
    kpi1.metric("Last 90 Days Commercial composite median Meter Price",f"{period_Commercial_composite:,}","{0:.0%}".format(period_Commercial_composite_prct_chg))
    kpi2.metric("Last 90 Days Residential composite median Price",f"{period_Residential_composite:,}","{0:.0%}".format(period_Residential_composite_prct_chg))
    
if  option == 'Villas Transactions Search':
    st.header(option)
    st.markdown("- Villas transactions search is provided for the last 30 days (or part of it depending on dates selection)")
    st.markdown("- Results can be sorted on each column (ascending,desending)")
    registry = st.sidebar.selectbox('Select registry type?',('Existing Properties','Off-Plan Properties'))
    if registry == "Existing Properties":
        registry_code = 1
    else:
        registry_code = 0
    start_size, end_size = st.slider("Select Villa Size Range", min_value= 50, max_value=2000, value=(100, 1000),step = 10)

    #select_rooms = st.sidebar.multiselect('Select Flat Rooms', ('1 B/R','2 B/R','3 B/R','Studio'),'1 B/R')
    end_date = villa_sales['txs_date'].max()
    start_date = end_date - datetime.timedelta(days=30)
    start = st.sidebar.date_input("Start Date", value = start_date)
    end = st.sidebar.date_input("End Date",value = end_date)
    villa_area = villa_sales['area_name_en'].unique()
    select_area = st.sidebar.multiselect('Select area?',villa_area,villa_area[34])
    select_txs = villa_sales[(villa_sales['reg_type_id']==registry_code)&(villa_sales['area_name_en'].isin(select_area))&(villa_sales['procedure_area'] >= start_size)&(villa_sales['procedure_area'] <= end_size)&(villa_sales['txs_date']<=end_date)&(villa_sales['txs_date']>=start_date)]
    select_txs['date'] = pd.to_datetime(select_txs['txs_date']).dt.date
    display_txs = select_txs[['date','area_name_en','project_name_en','procedure_area','actual_worth','meter_sale_price']]
    st.dataframe(display_txs)

if  option == 'Lands Transactions Search':
    st.header(option)
    st.markdown("- Lands transactions search is provided for the last 30 days (or part of it depending on dates selection)")
    st.markdown("- Results can be sorted on each column (ascending,desending)")
    start_size, end_size = st.slider("Select Land Size Range", min_value= 200, max_value=5000, value=(100, 2000),step = 100)

    #select_rooms = st.sidebar.multiselect('Select Flat Rooms', ('1 B/R','2 B/R','3 B/R','Studio'),'1 B/R')
    end_date = land_sales['txs_date'].max()
    start_date = end_date - datetime.timedelta(days=30)
    start = st.sidebar.date_input("Start Date", value = start_date)
    end = st.sidebar.date_input("End Date",value = end_date)
    land_area = land_sales['area_name_en'].unique()
    select_area = st.sidebar.multiselect('Select area?',land_area,land_area[34])
    select_txs = land_sales[(land_sales['area_name_en'].isin(select_area))&(land_sales['procedure_area'] >= start_size)&(land_sales['procedure_area'] <= end_size)&(land_sales['txs_date']<=end_date)&(land_sales['txs_date']>=start_date)]
    select_txs['date'] = pd.to_datetime(select_txs['txs_date']).dt.date
    display_txs = select_txs[['date','area_name_en','project_name_en','procedure_area','actual_worth','meter_sale_price']]
    st.dataframe(display_txs)    
    