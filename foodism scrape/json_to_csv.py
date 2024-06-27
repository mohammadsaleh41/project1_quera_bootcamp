# %%
import pandas as pd
import numpy as np
import json

# %%
df = pd.read_json("/media/mohammadsaleh/bootcamp/project1/Quera_Data_Science/foodism scrape/e.json")

# %%
print(df)
# %%
f = open("/media/mohammadsaleh/bootcamp/project1/Quera_Data_Science/foodism scrape/e.json")
j = json.load(f)

# %%
j["items"][0]
# %%