# %%
import requests
import os
import json
import pandas as pd
from bs4 import BeautifulSoup
import time
import logging
from logging.handlers import RotatingFileHandler

# %%
dirname = os.path.dirname(__file__)
df = pd.read_csv(dirname +"/data.csv")
#اینجا رو برای ویندوز قبل report.txt رو به دو تا \\ تبدیل کنین.
logging.basicConfig(filename=dirname+'/report.txt',filemode="w",format='[TIME: %(asctime)s] [DigiKala@Torture] %(levelname)s: %(message)s', level=logging.INFO) #filename='Practices\\log.log',
LOGGER = logging.getLogger("digikala@torture")


def syslogger(msg, sev = "info"):
    if "debug" in sev :
        LOGGER.debug(msg)        
    elif "info" in sev :
        LOGGER.info(msg)
    elif "warning" in sev :
        LOGGER.warning(msg)
    elif "error" in sev :
        LOGGER.error(msg)
    elif "critical" in sev :
        LOGGER.critical(msg)
    else:
        pass

# %%
# bakhsh  اینجا همون مرحله ما هست که باید به صورت دستی تنظیم کنیم تا ۹ باید پیش رفت.

bakhsh = 6



# %% 
df_MenuCategory = pd.DataFrame(columns=["restaurantid","MenuCategoryId","Title"])
df_MenuItem = pd.DataFrame(columns=["MenuItemId", 'MenuCategoryId' , 'Name' , 'Description' , 'Price' , 'Likes' , "UserLiked" ,'Image' ])
df_kar = pd.DataFrame(columns=["restaurantid","baze"])
df_tel = pd.DataFrame(columns=["restaurantid","tel"])
# %%
def dfrow_2_url(df , row):
    url = "https://fidilio.com/restaurants/"+df["slug"].loc[row]+"/"+df["name"].loc[row].replace(" ","-")+"/"
    return url
def url_2_suap(url):
    
    response = requests.get(url)
    suap = BeautifulSoup(response.text , "html.parser")
    return suap
def suap_2_foods(suap):
    foods = suap.find("input" , id = "menuObject")
    return foods

# %%

for row in range(bakhsh*500 , ((1+bakhsh)*500)
                ):
    print(row)
    if row == len(df):
        break
    try:
        url = dfrow_2_url(df , row)
        suap = url_2_suap(url)
    except:
        syslogger("yek moshkel ajib radif : "+str(row)+" \nmoshkel dare" )
    try:
        natije = suap.find("div" , class_ = "informations-body")

        natije =natije.find_all("span" , class_ = "note" ) 
    except:
        syslogger("radif\n"+str(row)+"\nghesmat etelaat nadare")
    try:
        df_kar = df_kar.append({"restaurantid":df.loc[row]["id"] ,"baze": natije[2].text.split()[-1]}, ignore_index=True)
    except:
        syslogger("sabt etelat saat kar radif\n"+str(row)+"\nkhata dad")
    try:
        df_tel = df_tel.append({"restaurantid":df.loc[row]["id"] ,"tel": natije[1].text.split()[-1]}, ignore_index=True)
    except:
        syslogger("sabt etelat telephone radif\n"+str(row)+"\nbemoshkel khord")
    
    try:
        foods = suap_2_foods(suap)
        a = foods["value"][1:-1].replace('}]},{"MenuCategoryId":"' , '}]}yek chize ajagh vajagh{"MenuCategoryId":"').split("yek chize ajagh vajagh")
        for i in range(len(a)):
            b = json.loads(a[i])
            df_MenuCategory = df_MenuCategory.append({"restaurantid":df.loc[row]["id"] , "MenuCategoryId": b['MenuCategoryId'], "Title":b['Title']}, ignore_index=True)
            for j in range(len(b["MenuItemes"])):
                c= b["MenuItemes"][j]
                df_MenuItem = df_MenuItem.append(c , ignore_index=True)
    except:
        x = []
        x.append(row)

# print(x)
# %%
# print(x)
df_MenuItem.to_csv(dirname +"/MenuItem"+str(bakhsh)+".csv")

df_MenuCategory.to_csv(dirname +"/MenuCategory"+str(bakhsh)+".csv")
df_kar.to_csv(dirname +"/saat_kari"+str(bakhsh)+".csv")

df_tel.to_csv(dirname +"/telephone"+str(bakhsh)+".csv")


# %%
url = dfrow_2_url(df , 4505)
suap = url_2_suap(url)
suap
# %%
