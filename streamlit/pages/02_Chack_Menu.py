from pandas.api.types import (
    is_datetime64_any_dtype,
    is_categorical_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st
import os
import streamlit.components.v1 as components
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
st.title('Check Menu')
st.write('Now that you are here have a look at your selected place\'s menu.')

menuItem_path = dirname[:-16]+'/Extracted CSVs/MenuItem.csv'
menuCategory_path = dirname[:-16]+'/Extracted CSVs/MenuCategory.csv'
df_data =  pd.read_csv(dirname[:-6]+"/data.csv")

menuItem_df = pd.read_csv(menuItem_path).set_index('menu_category_id')
menuCategory_df = pd.read_csv(menuCategory_path).set_index('menu_category_id')
menu_df = pd.merge(menuCategory_df, menuItem_df)
df_filtered = filter_dataframe(menu_df)
st.dataframe(df_filtered)
map_df = df_filtered.merge(df_data , right_on = "id" , left_on = "restaurant_id")
components.html('<p dir = "rtl">آدرس رستوران یا کافی شاپ‌هایی که در بالا غذاهای آن‌هاا لیست شده است را در نقشه پایین می‌توانید مشاهده کنید:</p>')
st.map(map_df)


st.write('Hope we could help.')
