# -------------- IMPORTS --------------
import pandas as pd

import streamlit as st

from datetime import datetime as dt
from datetime import date
from calendar import monthrange

import plotly.express as px
import plotly.graph_objects as go

# -------------- SETUP SITE --------------
st.set_page_config(
        page_title='statistics',
        page_icon=":bar_chart:",
        layout="centered")
st.header('incomes and expenses for')  

# -------------- OPTIONS --------------
durations = {'fix', 'variable'}
types = {'costs📉', 'revenue📈'}

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

startpoint = dts[0].strftime("%d.%m.%Y")
endpoint = dts[1].strftime("%d.%m.%Y")
st.write('Start: ', startpoint, "___End: ", endpoint)

# -------------- DATAFRAME ZUSCHNEIDEN --------------

mask = df_trans['date'].between(startpoint,endpoint)
df_trans = df_trans[mask]

df_sunburst = df_trans # für später wichtig

# -------------- DATEN AUFADDIEREN, VARIABLEN FESTLEGEN --------------
df_trans = df_trans.groupby(['key1']).sum() 
labels = df_trans.index
values = df_trans['amount']
colors = [ 'lightgreen', 'mediumturquoise', 'gold', 'darkorange']

# -------------- PIE CHART --------------
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
fig.update_traces(
        hoverinfo='label+percent', 
        textinfo='value', 
        textfont_size=20,
        marker=dict(colors=colors, line=dict(color='#000000', width=2)))
st.plotly_chart(fig)

# -------------- SUNBURST CHART --------------
st.header('sunburst chart with categories')
fig = px.sunburst(
        data_frame = df_sunburst,
        path = ['type', 'duration', 'categorie'],
        values = 'amount')
st.plotly_chart(fig)


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