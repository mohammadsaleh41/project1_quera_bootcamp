# %%
import mysql.connector
import pandas as pd
from tqdm.notebook import tqdm

# %%
mydb = mysql.connector.connect(
  host="37.32.5.76",
  user='user_group2',
  password='n8RqKtxMFauVYD^u',
  database='group2'
)

cursor = mydb.cursor()

# %%
cursor.execute("SHOW TABLES")
TABLES = tuple()
for x in cursor:
    TABLES += x
# %%
for i, x in enumerate(TABLES):
    print(f"{i}\t{x}")
# %%
cursor.execute("ALTER TABLE `Place` CHANGE COLUMN `name` `name` NVARCHAR(50) NULL DEFAULT NULL ;")
cursor.fetchall()

# %%
df = pd.read_csv('places.csv')

columns = ["id",'name']
df_subset = df[columns]


for i, row in df_subset.iterrows():
    values = ( row['id'],row['name'])
    cursor.execute("INSERT INTO Place (web_id ,name) VALUES (%s,%s)", values)

    mydb.commit()


# %%
cursor.execute("CREATE TABLE New_Place (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, name NVARCHAR(255))")
# %%
cursor.execute("""LOAD DATA IN FILE 'Places.csv' INTO TABLE New_PlaceFIELDS TERMINATED BY ',' ENCLOSED BY '"'LINES TERMINATED BY '\n';""")


# %%

df = pd.read_csv('places.csv')

values =  df['name']
cursor.execute("INSERT INTO Place (name) VALUES (%s)", values)
# %%

# %%
cursor.execute("DELETE FROM Place;")
# %%
cursor.execute("""INSERT INTO New (name) VALUES ('hjj')""")



# %%


cursor.execute("CREATE TABLE New (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, name NVARCHAR(255))")


# %%
cursor.execute("""select * from New""")

# %%
cursor.close()
# %%
cursor.reset()
cursor.execute("""INSERT INTO New_New_Place (id, name) Values (1111,"علی")""")
mydb.commit()