# -------------- IMPORTS --------------
import pandas as pd
import streamlit as st
from datetime import datetime as dt
import calendar
from calendar import monthrange
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime
# --------------------------------------

# -------------- SETUP SITE --------------
st.set_page_config(
        page_title='tableview',
        page_icon=":umbrella:",
        layout="centered")
st.header('tableview')  

# -------------- SETTINGS --------------
durations = {'fix', 'variable'}
types = {'costs📉', 'revenue📈'}
categories = [
        'housing🏠', 
        'utilities🦼', 
        'food🥗', 
        'transportation🚗', 
        'student loan👨‍🎓', 
        'insurance🤕', 
        'health💊', 
        'clothing👕', 
        'entertainment📺',
        'savings💰',
        'salary🧑‍💼',
        'transfer💸']

# -------------- LOAD DATA --------------
excel_file2 = 'DATA.xlsx'
sheet_trans = 'TRANS'
df_trans = pd.read_excel(excel_file2, sheet_name=sheet_trans, usecols='B:Z')


# -------------- DATE INPUT --------------
current_year = date.today().year
current_month = date.today().month
lastday_month = monthrange(current_year, current_month)[1]

dts = st.date_input(label='date range: ',
                value=(dt(year=current_year, month=current_month, day=1), 
                        dt(year=current_year, month=current_month, day=lastday_month)),
                key='#date_range',
                help="The start and end date time")

startpoint = dts[0].strftime("%d-%m-%Y")
endpoint = dts[1].strftime("%d-%m-%Y")
st.write('Start: ', startpoint, "___End: ", endpoint)

# -------------- DATAFRAME ZUSCHNEIDEN --------------









df_single_level_cols = pd.DataFrame([[0, 1], [2, 3]],
                                    index=['cat', 'dog'],
                                    columns=['weight', 'height'])


df = df_single_level_cols.stack()
df



mask = df_trans['date'].between(startpoint,endpoint)
df_trans = df_trans[mask]

df_trans = df_trans.sort_values(['date', 'categorie', 'type'])


 
df_trans = df_trans.drop(columns=['type', 'comment'])

index = [1,2,1,2,3,4,1,2,3,4,1,2,1,1]
index
df_trans.insert(loc=0, column='data', value=index)

df_trans = df_trans.pivot_table("amount", index=['date', 'data'], columns="categorie", fill_value='')
df_trans

# df_trans = df_trans.reset_index(drop=True)

# list = []
# for i in df_trans.index:                      
#         if str(df_trans.loc[i, 'type']) == 'costs📉': 
#                 vorzeichen = '-'
#         else: vorzeichen = '+'
       
#         new_cell = f"{vorzeichen}{str(df_trans.loc[i, 'amount'])} ({df_trans.loc[i, 'comment']})"
#         list.append(new_cell)

# list




# df_trans.insert(loc=0, column='data', value=list)

# df_trans = df_trans.drop(columns=['type', 'comment', 'amount'])
# df_trans = df_trans.reset_index()
# df_trans = df_trans.set_index(['date', 'index'])

# df_trans 


# table = pd.pivot_table(data=df_trans,index=['categorie'])
# table

# df_trans.pivot_table("data",index=["date", "categorie"], columns="categorie")



#df_trans = df_trans.unstack()

# f"{df_trans['amount'].tolist()}"




# df = df_trans.set_index('categorie').drop(columns=['key', 'key1', 'repetition', 'duration'])
# df



# dates = pd.date_range(dts[0],dts[1]).strftime("%d-%m-%Y")

# df_trans = df_trans.set_index('date')
# keys = list(df_trans.index.intersection(dates))
# st.subheader('keys')
# keys


# for key in keys:
#         df_help = df_trans.loc[key]
#         df_help 
