from pandas.api.types import (
    is_datetime64_any_dtype,
    is_categorical_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st
import os
dirname = os.path.dirname(__file__)
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    modify = st.checkbox("Do you want to add filters?")
    if not modify:
        return df
    df = df.copy()

    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass
        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]
    return df


st.set_page_config(page_title='Fidilio Info')
st.title('Find Your Place')
st.header('Find Where You Want To Go')
st.write('Here you can apply different types of filters in data we gathered and choose where you want to visit next.')

place_path = dirname[:-16]+'/Extracted CSVs/Places.csv'
menuItem_path = dirname[:-16]+'/Extracted CSVs/MenuItem.csv'
phoneNumber_path = dirname[:-16]+'/Extracted CSVs/PhoneNumber.csv'
menuCategory_path = dirname[:-16]+'/Extracted CSVs/MenuCategory.csv'

df_data =  pd.read_csv(dirname[:-6]+"/data.csv")
place_df = pd.read_csv(place_path)
place_df['PlaceID'] = place_df['place_id']
place_df = place_df[place_df.columns[~place_df.columns.isin(['latitude', 'longitude', 'slug'])]].set_index('place_id')
phoneNumber_df = pd.read_csv(phoneNumber_path).set_index('restaurant_id')
info_df = pd.merge(place_df, phoneNumber_df)
df_filtered = filter_dataframe(info_df)
st.dataframe(df_filtered)

map_df = df_filtered.merge(df_data , right_on = "id" , left_on = "PlaceID")

st.map(map_df)

st.write("""Now that you know where to go, copy their place_id and use it on the next page to see their menu.
            And now that you have their number you may want to call them first.""")
