# %%

import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy
import time
import os
# %%
dirname = os.path.dirname(__file__)
# https://foodism.app/api/Places/search
url = "https://foodism.app/api/Places/search"


# %%
data = {"page":2,"limit":12,"cityId":"9","text":"","sort":"2"}


# %%
session = requests.Session()
#                              https://foodism.app/places/search/%D9%85%D8%B4%D9%87%D8%AF?&text=&sort=2
first_response = requests.get("https://foodism.app/places/search/%D9%85%D8%B4%D9%87%D8%AF?&text=&sort=2")
#                         Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0
headers = {
"Cookie":"{ga_SGCEF1CY0Q=GS1.1.1675277650.5.0.1675277656.0.0.0; _ga=GA1.2.1340966966.1674936768; analytics_campaign={%22source%22:%22direct%22%2C%22medium%22:null}; analytics_token=4c030105-60b1-6f5a-9e87-9f32bcc2b86b; _yngt=acbb633b-1609-4413-a825-3bf1985d5415; _yngt_match={%22sabavision%22:1}; _gid=GA1.2.25091541.1675277657; _gat_UA-20656454-1=1; analytics_session_token=d7567841-6c92-ed90-878d-78af8954e343; yektanet_session_last_activity=2/1/2023; _yngt_iframe=1}",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
"Connection":"keep-alive",
"Token":"ad5f26d8f12cdc16cdbc6cf185ec50cd",
'X-Requested-With':'XMLHttpRequest',
"Host":"foodism.app",
"Origin":"https://foodism.app",
"Referer":"https://foodism.app/",
"Sec-Fetch-Dest":"empty",
"Sec-Fetch-Mode":"cors",
"Sec-Fetch-Site":"same-origin",
"TE":"trailers",
"Content-Length":"55",
"Content-Type":"application/json"}
response = session.post(url, headers=headers,
                        json=data)
# %%
print("asli :  ",response.status_code)
# %%
print("avali : ",first_response.status_code)
# %%
cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))
# %%
f = open(dirname+"/first_scraped_page.html" , "w")
f.write(first_response.text)
f.close()
# %%
f = open(dirname+"/scraped_page.html" , "w")
f.write(response.text)
f.close()
# %%
