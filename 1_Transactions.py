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
page_title = "Transaction"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

# -------------- SETUP SITE --------------
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title("New " + page_title + " " + page_icon)

# -------------- LOAD FILE -------------
excel_file = 'DATA.xlsx'
sheet_trans = 'TRANS'
sheet_fix_init = 'FIX_INIT'

df_trans = pd.read_excel(excel_file, sheet_name=sheet_trans, usecols='B:Z')
df_fix_init = pd.read_excel(excel_file, sheet_name=sheet_fix_init, usecols='B:Z')

# -------------- OPTIONS -------------
options_categorie_cost = {
        'housing🏠', 
        'utilities🦼', 
        'food🥗', 
        'transportation🚗', 
        'study👨‍🎓', 
        'insurance🤕', 
        'healthcare💊', 
        'clothes👕', 
        'entertainment📺'}

options_categorie_incomes = {
        'salary🧑‍💼',
        'transfer💸'}

option_type = {
        'expenses📉', 
        'incomes📈'}

option_timeunit = {
        'day',
        'week',
        'month',
        'year'}

# -------------- MENU BAND --------------
selected = option_menu(
        menu_title=None,
        options=['Var', 'Fix'],
        icons=["arrow-down-up", "arrow-repeat"],
        orientation="horizontal"
)

# -------------- CHECK FOR FIX ENTRIES --------------
changed = False   # local variable, that checks the status if fix transaction inbetween the time the user was offline was made

# iterate over whole fix transactions
for index, row in df_fix_init.iterrows():
        # as long as transaction in fix init sheet is older than today, fullfill the transactions
        while (df_fix_init['date'][index]) <= date.today().strftime("%Y-%m-%d"):
                # save fix transaction (with old date) as new entry in the transaction sheet
                df_trans = df_trans.append(df_fix_init.loc[[index]])
                                
                # now change the old date of row (adding the period)
                date_object = datetime.strptime(df_fix_init['date'][index], '%Y-%m-%d')
                digit = int(df_fix_init['digit'][index])

                if df_fix_init['timeunit'][index] == 'day': 
                        new_date = date_object + relativedelta(days = digit)

                elif df_fix_init['timeunit'][index] == 'week': 
                        new_date = date_object + relativedelta(weeks = digit)

                elif df_fix_init['timeunit'][index] == 'month': 
                        new_date = date_object + relativedelta(months = digit)

                elif df_fix_init['timeunit'][index] == 'year': 
                        new_date = date_object + relativedelta(years = digit)
                
                df_fix_init['date'][index] = new_date.strftime("%Y-%m-%d")

                changed = True   

# save to sheet: fix transaction (with new date) in fix init sheet 
with pd.ExcelWriter(excel_file, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
        df_fix_init.to_excel(writer, sheet_name=sheet_fix_init)
with pd.ExcelWriter(excel_file, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
        df_trans.to_excel(writer, sheet_name=sheet_trans)                                

# rerun all, to get correct statistics               
if changed: 
        st.experimental_rerun()

# -------------- MENU: VAR OR FIX ENTRIES --------------
if selected == "Var":

        duration = "var"

        date_chosen = st.date_input(label='DATE', key="calendar").strftime("%Y-%m-%d")

        col1, col2 = st.columns(2)
        with col1:                 
                type = st.selectbox('TYPE',options=option_type)
                amount = st.number_input('AMOUNT', min_value=0)
        with col2:
                if type == 'expenses📉':
                        categorie = st.selectbox('CATEGORIE', options=options_categorie_cost)
                else: categorie = st.selectbox('CATEGORIE', options=options_categorie_incomes)
                comment = st.text_input('COMMENT')
        

        # -------------- SAVE NEW ENTRY --------------
        new_row = {
                'date':date_chosen,
                'duration':duration, 
                'type':type,
                'categorie': categorie, 
                'comment':comment, 
                'amount':amount,
                'key':type+duration
                }

        if st.button(label='UPLOAD'):
                df_trans = df_trans.append(new_row, ignore_index=True)
                with pd.ExcelWriter(excel_file, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
                        df_trans.to_excel(writer, sheet_name=sheet_trans)
                st.experimental_rerun()

        # -------------- LAST ENTRIES, DELETE LAST ROW --------------
        st.write('---')
        st.subheader('Your Last 3 Entries')
        df_last = df_trans.tail(3)
        df_last = df_last.drop(columns=['key', 'timeunit', 'digit']) 
        df_last

        if st.button(label='DELETE LAST'):
                df_trans.drop(index=df_trans.index[-1], axis=0, inplace=True)   
                with pd.ExcelWriter(excel_file, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
                        df_trans.to_excel(writer, sheet_name=sheet_trans) 
                st.experimental_rerun()

if selected == "Fix":
        duration = "fix"
      
        col1, col2, col3 = st.columns(3)
        with col1: date_chosen = st.date_input(label='CALENDAR', key="calendar").strftime("%Y-%m-%d")
        with col2: digit = st.number_input('DIGIT', min_value=1)
        with col3: timeunit = st.selectbox('TIMEUNIT', options=option_timeunit)

        col1, col2 = st.columns(2)
        with col1:                 
                type = st.selectbox('TYPE',options=option_type)
                amount = st.number_input('AMOUNT', min_value=0)

        with col2:
                if type == 'expenses📉':
                        categorie = st.selectbox('CATEGORIE', options=options_categorie_cost)
                else: categorie = st.selectbox('CATEGORIE', options=options_categorie_incomes)
                comment = st.text_input('COMMENT')
        
        # -------------- SAVE NEW ENTRY --------------
        new_row = {
                'date':date_chosen,
                'duration':duration, 
                'type':type,
                'categorie': categorie, 
                'comment':comment, 
                'amount':amount,
                'key':type+duration,
                'digit':digit,
                'timeunit': timeunit
                }

        if st.button(label='UPLOAD'):
                df_fix_init = df_fix_init.append(new_row, ignore_index=True)
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