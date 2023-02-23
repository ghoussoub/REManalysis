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
def load_txs():
    df = pd.read_csv(r'txs_sales.csv',encoding=('utf_8'))
    df['year'] = pd.DatetimeIndex(df['instance_date']).year
    df['month'] = pd.DatetimeIndex(df['instance_date']).month
    df['txs_date'] = pd.to_datetime(df['instance_date'],format='%d-%m-%Y')
    df['fst_day'] = df['txs_date'].apply(lambda x : x.replace(day=1))
    df['fst_qtr'] = df['instance_date'].apply(quarter_month)
    df['fst_day'] = pd.to_datetime(df['fst_day']).dt.date
    df['fst_qtr'] = pd.to_datetime(df['fst_qtr'],format='%d-%m-%Y')
    return(df)
df = load_txs()
#area = df['area_name_en'].drop_duplicates()
area = list(df['area_name_en'].unique())
#area.sort_values(by=['area_name_en'], inplace=True)
#area.sort_values('area_name_en',axis=0,ascending=False).reset_index(drop=True)
flat_sales = df[(df['trans_group_id']==1)&(df['property_type_id']==3)&(df['property_sub_type_id']==60)]
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
option = st.sidebar.selectbox("Select Dashboard?", ('Comparative Area Performance','Flats Prices Trend', 'Flats Transactions Search','Flat Price Estimation'))
if option == 'Flats Prices Trend':
    registry = st.sidebar.selectbox('Select registry type?',('Existing Properties','Off-Plan Properties'))
    if registry == "Existing Properties":
        registry_code = 1
    else:
        registry_code = 0
    flat_area = flat_sales['area_name_en'].unique()
    select_area = st.sidebar.selectbox('Select area?',flat_area)
    #st.header("Area Market Analysis of : {}".format(select_area))
    st.header(option+" in : {}".format(select_area))
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
    this_period_median_meter_price = int(flat_sales_selected_period['meter_sale_price'].median())
    flat_sales_selected_previous_period = flat_sales[(flat_sales['reg_type_id']==registry_code)&(flat_sales['area_name_en']==select_area)&(flat_sales['txs_date']<=end_date - datetime.timedelta(days=365))&(flat_sales['txs_date']>=end_date - datetime.timedelta(days=455))]
    previous_period_count = flat_sales_selected_previous_period['transaction_id'].count()
    this_period_txs_count_prct_chg = (this_period_count-previous_period_count)/previous_period_count
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
    single_area_median_prices_df['rolling_mean'] = single_area_median_prices_df.set_index('fst_day').groupby('Room_En', sort=False)['single_area_median_price'].rolling(6).mean().round(2).to_numpy()
    single_area_median_prices_df['meter_rolling_mean'] = single_area_median_prices_df.set_index('fst_day').groupby('Room_En', sort=False)['single_area_median_meter_price'].rolling(6).mean().round(2).to_numpy()
    single_area_median_prices_df['txs_count_rolling_mean'] = single_area_median_prices_df.set_index('fst_day').groupby('Room_En', sort=False)['single_area_txs_count'].rolling(6).mean().round(2).to_numpy()
    single_area_median_prices_start_df = single_area_median_prices_df[single_area_median_prices_df['fst_day']==start_day]
    single_area_median_prices_added_start_df = pd.merge(single_area_median_prices_df,single_area_median_prices_start_df,left_on="Room_En",right_on="Room_En",how = "left")
    single_area_median_prices_added_start_df['price_pct_chg'] = 100*(single_area_median_prices_added_start_df['single_area_median_price_x']-single_area_median_prices_added_start_df['single_area_median_price_y'])/single_area_median_prices_added_start_df['single_area_median_price_y']
    single_area_median_prices_added_start_df['meter_price_pct_chg'] = 100*(single_area_median_prices_added_start_df['single_area_median_meter_price_x']-single_area_median_prices_added_start_df['single_area_median_meter_price_y'])/single_area_median_prices_added_start_df['single_area_median_meter_price_y']
    kpi4,kpi5,kpi6 = st.columns(3)
    kpi4.metric("Last 90 Days 1 B/R median Price",f"{this_period_1bed_median_price:,}","{0:.0%}".format(this_period_1bed_price_pct_chg))
    kpi5.metric("Last 90 Days 2 B/R median Price",f"{this_period_2bed_median_price:,}","{0:.0%}".format(this_period_2bed_price_pct_chg))
    kpi6.metric("Last 90 Days 3 B/R median Price",f"{this_period_3bed_median_price:,}","{0:.0%}".format(this_period_3bed_price_pct_chg))
    st.markdown("Scatter Plot of price & size")
    base = alt.Chart(flat_sales_selected_period).properties(height=300)
    point = base.mark_circle(size=20).encode(x=alt.X('actual_worth' + ':Q', title="price"), y=alt.Y('procedure_area' + ':Q', title="size"),color=alt.Color('Room_En', title='Rooms',legend=alt.Legend(orient='bottom-right')))
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
    base5 = alt.Chart(single_area_qtr_median_prices_df).properties(height=300)
    line5 = base5.mark_line(size=2).encode(x=alt.X('fst_qtr', title='Date'),y=alt.Y('single_area_qtr_median_price', title='median price'),color=alt.Color('Room_En', title='Flat Size',legend=alt.Legend(orient='right')))
    st.altair_chart(line5,use_container_width=True)
    base7 = alt.Chart(single_area_qtr_median_prices_df).properties(height=300)
    line7 = base7.mark_line(size=2).encode(x=alt.X('fst_qtr', title='Date'),y=alt.Y('single_area_qtr_median_meter_price', title='meter_median price'),color=alt.Color('Room_En', title='Flat Size',legend=alt.Legend(orient='right')))
    st.altair_chart(line7,use_container_width=True)
    base6 = alt.Chart(single_area_qtr_median_prices_df).properties(height=300)
    line6 = base6.mark_line(size=2).encode(x=alt.X('fst_qtr', title='Date'),y=alt.Y('single_area_txs_count', title='txs count'),color=alt.Color('Room_En', title='Flat Size',legend=alt.Legend(orient='right')))
    st.altair_chart(line6,use_container_width=True)
    base3 = alt.Chart(single_area_median_prices_df).properties(height=300)
    line3 = base3.mark_line(size=2).encode(x=alt.X('fst_day', title='Date'),y=alt.Y('rolling_mean', title='rolling median price'),color=alt.Color('Room_En', title='Flat Size',legend=alt.Legend(orient='right')))
    st.altair_chart(line3,use_container_width=True)
    #with col2:
    base4 = alt.Chart(single_area_median_prices_df).properties(height=300)
    line4 = base4.mark_line(size=2).encode(x=alt.X('fst_day', title='Date'),y=alt.Y('meter_rolling_mean', title='meter rolling median price'),color=alt.Color('Room_En', title='Flat Size',legend=alt.Legend(orient='right')))
    st.altair_chart(line4,use_container_width=True)
    base8 = alt.Chart(single_area_median_prices_df).properties(height=300)
    line8 = base8.mark_line(size=2).encode(x=alt.X('fst_day', title='Date'),y=alt.Y('txs_count_rolling_mean', title='monthly txs count ma'),color=alt.Color('Room_En', title='Flat Size',legend=alt.Legend(orient='right')))
    st.altair_chart(line8,use_container_width=True)
    #flat_sales_select = flat_sales[(flat_sales['reg_type_en']==registry)]
if option == 'Comparative Area Performance': 
    def perf_class(x):
        if x >= 20:
            perf = "more than 20%"
        elif x < 20 and x >= 5:
            perf = "btw 5 to 20%"
        elif x < 5 and x > -5:
            perf = "btw -5 & 5%"
        elif x < -5 and x > -20:
            perf = "btw -20 & -5%"
        else:
            perf = "less than -20%"
        return perf
    st.header(option)
    st.markdown("Area performance is determined by the area median price percentage change for the last 90 days period compared to same period last year")
    registry = st.sidebar.selectbox('Select registry type?',('Existing Properties','Off-Plan Properties'))
    if registry == "Existing Properties":
        registry_code = 1
    else:
        registry_code = 0
    select_rooms = st.sidebar.selectbox('Select Flat Rooms', ('1 B/R','2 B/R','3 B/R'))
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
    st.dataframe(merged_subset)
    #print_some_rows = merged_subset.head(5)
    #print(print_some_rows)
    #with st.sidebar:
        #add_radio = st.radio("Sorting Result by:",("Area Name", "Flat Price","Txs Count"))
    st.markdown('###')
    st.header("Interactive Area Performance Chart")
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
    
    
    