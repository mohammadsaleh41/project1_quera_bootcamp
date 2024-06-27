import requests
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
import streamlit.components.v1 as components
import os
dirname = os.path.dirname(__file__)

st.set_page_config(page_title='Fidilio Info')
st.title('Fidilio As Data Source')
st.write("""
            We manage to gather different information for each place like coffee shops and restaurants
            registered in Fidilio website and use them for different types of analysis.
        """)
st.write('Hope you enjoy it :)')
st.write('-------')

df = pd.read_csv(dirname+"/data.csv")

st.map(df)