# -------------- IMPORTS --------------

# https://discuss.streamlit.io/t/streamlit-deployment-as-an-executable-file-exe-for-windows-macos-and-android/6812
import pandas as pd

import streamlit as st
from streamlit_option_menu import option_menu  

import datetime
from datetime import datetime
from datetime import date

from calendar import monthrange
from dateutil.relativedelta import relativedelta
import calendar

# -------------- SETTINGS --------------
currency = "€"
page_title = "Fix Transactions"
page_icon = ":arrows_clockwise:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

# -------------- SETUP SITE --------------
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# -------------- LOAD FILE -------------
excel_file = 'DATA.xlsx'
sheet_trans = 'TRANS'
sheet_fix_init = 'FIX_INIT'

df_trans = pd.read_excel(excel_file, sheet_name=sheet_trans, usecols='B:Z')
df_fix_init = pd.read_excel(excel_file, sheet_name=sheet_fix_init, usecols='B:Z')


# -------------- DATE INPUT --------------
current_year = date.today().year
current_month = date.today().month
lastday_month = monthrange(current_year, current_month)[1]

dts = st.date_input(label='DATE RANGE',
                value=(datetime(year=current_year, month=current_month, day=1), 
                        datetime(year=current_year, month=current_month, day=lastday_month)),
                key='#date_range',
                help="The start and end date time")

startpoint = dts[0].strftime("%Y-%m-%d")
endpoint = dts[1].strftime("%Y-%m-%d")

# -------------- DATAFRAME ZUSCHNEIDEN --------------
mask = df_fix_init['date'].between(startpoint, endpoint) # nach Datum filtern
df_fix_in_range = df_fix_init[mask] # Maske anwenden und ins neue DF speichern

st.subheader('Incomes📈')
df_fix_einnahmen = df_fix_in_range[df_fix_in_range['type'] == 'incomes📈'].reset_index(drop=True)
df_fix_einnahmen = df_fix_einnahmen.drop(columns=['duration', 'key', 'type', 'digit', 'timeunit'])
df_fix_einnahmen

st.subheader('Expenses📉')
df_fix_ausgaben = df_fix_in_range[df_fix_in_range['type'] == 'expenses📉'].reset_index(drop=True)
df_fix_ausgaben = df_fix_ausgaben.drop(columns=['duration', 'key', 'type', 'digit', 'timeunit'])
df_fix_ausgaben


st.write('---')
st.header('Edit Your Fix Transactions')

df_fix_init
col1, col2 = st.columns(2)
with col1:
        index = st.number_input('INDEX', min_value=0, max_value=df_fix_init.last_valid_index())
        if st.button(label='DELETE'):
                df_fix_init.drop(index=df_fix_init.index[index], axis=0, inplace=True)   
                    
                with pd.ExcelWriter(excel_file, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
                        df_fix_init.to_excel(writer, sheet_name=sheet_fix_init) 
                st.experimental_rerun()

        
# -------------- HIDE STREAMLIT --------------
hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_st_style, unsafe_allow_html=True)