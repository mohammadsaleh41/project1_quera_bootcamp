# %%
import json
import requests
import os
import pandas as pd
from mokhtasat import two_corner
import time
import random
# تابع تبدیل ریسپانس به دیتا فریم
# این دیتا فریم تمیز نشده و روی خروجیش باید توابع add_type و add_style رو اضافه کنیم.
def api_fidilio_to_DataFrame(response):
    agahi_ha = json.loads(response.text)["results"]
    dict_ = {}
    dict_["id"] = []
    dict_["name"] = []
    dict_["image"] = []
    dict_["types"] = []
    dict_["styles"] = []
    dict_["latitude"] = []
    dict_["longitude"] = []
    dict_["isSpecialPin"] = []
    dict_["rating"] = []
    dict_["priceClass"] = []
    dict_["address"] = []
    dict_["hasOffer"] = []
    dict_["city"] = []
    dict_["isClubMember"] = []
    dict_["slug"] = []
    dict_["HasReservation"] = []
    

    for n in range(len(agahi_ha)):
        dict_["id"].append(agahi_ha[n]["id"])
        dict_["name"].append(agahi_ha[n]["name"])
        dict_["image"].append(agahi_ha[n]["image"])
        
        dict_["types"].append(agahi_ha[n]["types"])
        dict_["styles"].append(agahi_ha[n]["styles"])
        dict_["latitude"].append(agahi_ha[n]["latitude"])
        dict_["longitude"].append(agahi_ha[n]["longitude"])
        dict_["isSpecialPin"].append(agahi_ha[n]["isSpecialPin"])
        dict_["rating"].append(agahi_ha[n]["rating"])
        dict_["priceClass"].append(agahi_ha[n]["priceClass"])
        dict_["address"].append(agahi_ha[n]["address"])
        dict_["city"].append(agahi_ha[n]["city"])
        dict_["hasOffer"].append(agahi_ha[n]["hasOffer"])
        dict_["isClubMember"].append(agahi_ha[n]["isClubMember"])
        dict_["slug"].append(agahi_ha[n]["slug"])
        dict_["HasReservation"].append(agahi_ha[n]["HasReservation"])
        
    df_ = pd.DataFrame(dict_).set_index("id")
    #print(dict_["عنوان"])
    return df_

def add_style(df):
    style_list = []

    for i in range(len(df)):
        if type(df.loc[i]["styles"]) == list:
            d = df.loc[i]["styles"]
            for x in d:
                style_list.append(x)
        else:

            d = df.loc[i]["styles"][2:-2].split("', '")
            
            for x in d:
                style_list.append(x)
    
    style_list = list(dict.fromkeys(style_list))
    
    
    for i in range(len(style_list)):
        if len(style_list[i]) == 0:
            
            style_list.pop(i)
            break
        
    for i in style_list:
        
        df[i] = 0
    for i in range(len(df)):
        if type(df.loc[i]["styles"]) == list:
            d = df.loc[i]["styles"]
        else:

            d = df.iloc[i]["styles"][2:-2].split("', '")
        for x in d:
            df.loc[[i],[x]] = 1
    return df
def add_types(df):
    df["type_1"] = 0
    df["type_2"] = 0
    df["type_3"] = 0
    df["type_4"] = 0
    df["type_5"] = 0
    df["type_6"] = 0
    df["type_7"] = 0
    df["type_8"] = 0
    
    for i in range(len(df)):
        if type(df.iloc[i]["types"]) == list:
            l = df.iloc[i]["types"]
        else:
            l = df.iloc[i]["types"][1:-1].split(", ")
            l = [int(x) for x in l]
        
        if 1 in l :
            df.loc[[i],["type_1"]] = 1
        if 2 in l :
            df.loc[[i],["type_2"]] = 1
        if 3 in l :
            df.loc[[i],["type_3"]] = 1
        if 4 in l :
            df.loc[[i],["type_4"]] = 1
        if 5 in l :
            df.loc[[i],["type_5"]] = 1
        if 6 in l :
            df.loc[[i],["type_6"]] = 1
        if 7 in l :
            df.loc[[i],["type_7"]] = 1
        if 8 in l :
            df.loc[[i],["type_8"]] = 1

    return df
# %%
dirname = os.path.dirname(__file__)
# https://foodism.app/api/Places/search
url = "https://fidilio.com/api/map/GetSearchData"


# %%
def request_location(latitude ,longitude ):
    data = {"Radius":"50000" , "SortBy":"1","latitude":str(latitude),"longitude":str(longitude),"PageSize":"1000","PageNumber":"0","firstObjectLatEnabled":"true","query":"","isSpecialList":"false"}


    headers1 = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    }
    headers2 = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0",
    }
    headers = random.choice([headers1 , headers2])
    session = requests.Session()
    response = session.post(url, headers=headers2,
                            json=data)
    return response
# %%

if "data.csv" not in os.listdir(dirname):
    df = pd.DataFrame(columns=["id" , "name" , "image" , "types", "styles","type_1","type_2","type_3","type_4","type_5","type_6","type_7","type_8", "latitude", "longitude", "isSpecialPin", "rating", "priceClass", "address", "city", "hasOffer", "isClubMember", "slug", "HasReservation"])
else:
    df = pd.read_csv(dirname+"/data.csv")
df = add_style(df)

# %%
# داخل این حلقه اطلاعات لوکیشن‌های مختلف ایران استخراج می‌شه.
l_lat , l_lon = two_corner()
for i in range(len(l_lat)):
    response = request_location(l_lat[i], l_lon[i])
    df_ = api_fidilio_to_DataFrame(response)
    df_ = df_.reset_index()
    df_ = add_types(df_)
    df_ = add_style(df_)
    # df.drop(columns='Unnamed: 0' , inplace=True)
    #df.drop(columns='Unnamed: 0' , inplace=True)
    df = pd.concat([df, df_], ignore_index=True, axis=0).drop_duplicates(["id"] , keep='last')
    df.to_csv("data.csv")
# %%

    df.to_csv(dirname+"/data.csv" ,index=False )
    df_.to_csv(dirname+"/datas/data_"+str(i)+".csv")
    print(" بخش" , i," بخش انجام شد.")