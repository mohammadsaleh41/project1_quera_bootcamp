# یک آزمایش‌ها و محاسبات سر انگشتی انجام دادم هر ۱۰ کیلومتر حدودا 0.1 اون مقیاس درجه جغرافیایی هست. پس اگر ما بخوایم مرکز مختصات رو 50 کیلومتر به هر سمتی حرکت بدیم بردار تغییرات اون طول و عرض جغرافیایی هم باید 0.5 درجه باشه.
# %%
import numpy as np
# %% 
def two_corner(up = 39.7748 , left = 44.0224 , down = 25.0038 , right = 63.4845):
    l_lat = np.array([])
    l_lon = np.array([])
    latitude = up
    longitude = left
    while latitude> down and longitude < right:
        
        l_lat = np.append(l_lat , latitude)
        l_lon = np.append(l_lon , longitude)
        latitude-=0.5
        if latitude < down and longitude < right:
            latitude = up
            longitude += 0.5
        
    return l_lat , l_lon
