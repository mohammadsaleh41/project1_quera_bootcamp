import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import os
import shutil
from csv2vcard import csv2vcard

components.html('<p dir = "rtl">آیا دوست دارین شماره تلفن همه رستوران‌ها کافه‌ها شیرینی پزی‌ها و... ای که استخراج شده رو داشته باشین؟ روی دکمه زیر کلیک کنین.</p>')
dirname = os.path.dirname(__file__)

with open(dirname+'/restaurants.zip', 'rb') as f:
   st.download_button('Download Zip', f, file_name=dirname+'/restaurants.zip')  # Defaults to 'application/octet-stream'

