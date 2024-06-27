# %%
import pandas as pd

# %%
df = pd.read_csv("../fidilio scrape/data.csv")
df.head()

# %%
df.columns

# %%
places = df[["id","name"]]
places.head()

# %%
places.to_csv("Places.csv")

# %%

# %%


# %%


# %%


# %%