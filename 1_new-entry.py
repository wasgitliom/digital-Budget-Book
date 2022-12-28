# -------------- IMPORTS --------------

# https://discuss.streamlit.io/t/streamlit-deployment-as-an-executable-file-exe-for-windows-macos-and-android/6812


import pandas as pd

import streamlit as st
from streamlit_option_menu import option_menu  

import datetime
from datetime import datetime
from datetime import date

from dateutil.relativedelta import relativedelta
import calendar

# -------------- SETTINGS --------------
currency = "€"
page_title = "new entry"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
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

# -------------- OPTIONS -------------
years = [date.today().year - 1, date.today().year]
months = list(calendar.month_name[1:])
days = list(calendar.day_abbr)

options_categorie_cost = {
        'housing🏠', 
        'utilities🦼', 
        'food🥗', 
        'transportation🚗', 
        'student loan👨‍🎓', 
        'insurance🤕', 
        'health💊', 
        'clothing👕', 
        'entertainment📺'}

options_categorie_revenue = {
        'savings💰',
        'salary🧑‍💼',
        'transfer💸'}

option_type = {
        'costs📉', 
        'revenue📈'}

option_rep_string = {
        'day',
        'week',
        'month',
        'year'}

# -------------- MENU BAND --------------
selected = option_menu(
        menu_title=None,
        options=['variable', 'fix'],
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
                rep_number = int(df_fix_init['rep_number'][index])

                if df_fix_init['rep_string'][index] == 'day': 
                        new_date = date_object + relativedelta(days = rep_number)

                elif df_fix_init['rep_string'][index] == 'week': 
                        new_date = date_object + relativedelta(weeks = rep_number)

                elif df_fix_init['rep_string'][index] == 'month': 
                        new_date = date_object + relativedelta(months = rep_number)

                elif df_fix_init['rep_string'][index] == 'year': 
                        new_date = date_object + relativedelta(years = rep_number)
                
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
if selected == "variable":
        duration = "variable"

        date_chosen = st.date_input(label='calendar', key="calendar").strftime("%Y-%m-%d")

        col1, col2 = st.columns(2)
        with col1:                 
                type = st.selectbox('type',options=option_type)
                amount = st.number_input('amount', min_value=0)
        with col2:
                if type == 'costs📉':
                        categorie = st.selectbox('categorie', options=options_categorie_cost)
                else: categorie = st.selectbox('categorie', options=options_categorie_revenue)
                comment = st.text_input('comment')
        

        # -------------- SAVE NEW ENTRY --------------
        new_row = {
                'date':date_chosen,
                'duration':duration, 
                'type':type,
                'categorie': categorie, 
                'comment':comment, 
                'amount':amount,
                'key':type+duration+categorie, # TODO: check if neccessary
                'key1':type+duration
                }

        if st.button(label='upload new entry'):
                df_trans = df_trans.append(new_row, ignore_index=True)
                with pd.ExcelWriter(excel_file, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
                        df_trans.to_excel(writer, sheet_name=sheet_trans)
                        # TODO dont replace be water instead and append
                st.experimental_rerun()

        # -------------- LAST ENTRIES, DELETE LAST ROW --------------
        st.write('---')
        st.subheader('last 3 entries')
        df_last = df_trans.tail(3)
        df_last = df_last.drop(columns=['key', 'key1', 'rep_string', 'rep_number']) #TODO: dont change if keys are neccessary
        df_last

        if st.button(label='delete last entry'):
                df_trans.drop(index=df_trans.index[-1], axis=0, inplace=True)   
                with pd.ExcelWriter(excel_file, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
                        df_trans.to_excel(writer, sheet_name=sheet_trans) 
                st.experimental_rerun()

if selected == "fix":
        duration = "fix"
      
        col1, col2, col3 = st.columns(3)
        with col1: date_chosen = st.date_input(label='calendar', key="calendar").strftime("%Y-%m-%d")
        with col2: rep_number = st.number_input('rep_number', min_value=1)
        with col3: rep_string = st.selectbox('rep_string', options=option_rep_string)

        col1, col2 = st.columns(2)
        with col1:                 
                type = st.selectbox('type',options=option_type)
                amount = st.number_input('amount', min_value=0)

        with col2:
                if type == 'costs📉':
                        categorie = st.selectbox('categorie', options=options_categorie_cost)
                else: categorie = st.selectbox('categorie', options=options_categorie_revenue)
                comment = st.text_input('comment')
        
        # -------------- SAVE NEW ENTRY --------------
        new_row = {
                'date':date_chosen,
                'duration':duration, 
                'type':type,
                'categorie': categorie, 
                'comment':comment, 
                'amount':amount,
                'key':type+duration+categorie,
                'key1':type+duration,
                'rep_number':rep_number,
                'rep_string': rep_string
                }

        if st.button(label='upload new entry'):
                df_fix_init = df_fix_init.append(new_row, ignore_index=True)
                with pd.ExcelWriter(excel_file, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
                        df_fix_init.to_excel(writer, sheet_name=sheet_fix_init)
                st.experimental_rerun()

        # -------------- LAST ENTRIES, DELETE LAST ROW --------------
        st.write('---')
        st.header('all fix entries')

        st.subheader('Ausgaben')
        df_fix_ausgaben = df_fix_init[df_fix_init['type'] == 'costs📉']
        df_fix_ausgaben = df_fix_ausgaben.drop(columns=['duration', 'key', 'key1', 'type'])
        df_fix_ausgaben


        st.subheader('Einnahmen')
        df_fix_einnahmen = df_fix_init[df_fix_init['type'] == 'revenue📈']
        df_fix_einnahmen = df_fix_einnahmen.drop(columns=['duration', 'key', 'key1', 'type'])
        df_fix_einnahmen


# -------------- HIDE STREAMLIT --------------
#hide_st_style = """
        #<style>
        ##MainMenu {visibility: hidden;}
        #footer {visibility: hidden;}
        #header {visibility: hidden;}
        #</style>
        #"""
#st.markdown(hide_st_style, unsafe_allow_html=True)
# --------------------------------------               