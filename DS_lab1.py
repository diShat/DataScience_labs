import urllib.request as req
from datetime import datetime as dt


# defining function to retrieve data from website
def get_vha_data(index):
    url = 'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2020&type=Mean'.format(
        index)
    page = req.urlopen(url)
    data = page.read()

    now = dt.now()
    download_time = now.strftime("%d%m%Y%H%M%S")

    file_name = 'NOAA_ID{}_{}.csv'.format(index, download_time)
    out = open(file_name, 'wb')
    out.write(data)
    out.close()
    print('File {} retrieved.'.format(index))


for i in range(1, 28):
    if i in [12, 20]:
        continue  # not retrieving data for KyivCity and Sevastopol'
    else:
        get_vha_data(i)


# -------------------------------------------
import pandas as pd
import os


# importing data from separate files to dataframe
def files_to_dataframe(path):
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']

    df = {}

    for filename in os.listdir(path):  # iterating over all files in given directory
        if filename.endswith('.csv'):
            index = str(filename).split('_')[1][2:]  # getting region index from filename
            # print(index)
            df[index] = pd.read_csv(filename, header=1, names=headers)
            df[index] = df[index].drop(df[index].loc[df[index]['VHI'] == -1].index)  # cleaning all empty data
            df[index] = df[index].drop(index=2078)  # deleting weird last row
            df[index] = df[index].drop(columns=['empty'])

    return df


def switch_indexation(df_dict, new_pairs_dict):
    old_pairs = {'Cherkasy': 1, 'Chernihiv': 2, 'Chernivtsi': 3, 'Crimea': 4, 'Dnipro': 5, 'Donetsk': 6, 'Frankivsk': 7,
                 'Kharkiv': 8,
                 'Kherson': 9, 'Khmelnytskyi': 10, 'Kyiv': 11, 'Kropyvnytskiy': 13, 'Luhansk': 14, 'Lviv': 15,
                 'Mykolayiv': 16, 'Odesa': 17,
                 'Poltava': 18, 'Rivne': 19, 'Sumy': 21, 'Ternopil': 22, 'Zakarpattya': 23, 'Vinnytsya': 24,
                 'Volyn': 25, 'Zaporizhya': 26,
                 'Zhytomyr': 27}

    oldnew_pairs = [(old_pairs[name], new_pairs_dict[name]) for name in old_pairs.keys()]
    # print(oldnew_pairs)

    new_dict = {}
    for pair in oldnew_pairs:
        new_dict[str(pair[1])] = df_dict[str(pair[0])]
    df_dict.clear()

    return new_dict


# -------------------------------------------
df = files_to_dataframe(r'./')
print(df.keys())
# df['1'].head()

new_pairs = {'Vinnytsya': 1, 'Volyn': 2, 'Dnipro': 3, 'Donetsk': 4, 'Zhytomyr': 5, 'Zakarpattya': 6, 'Zaporizhya': 7,
             'Frankivsk': 8,
             'Kyiv': 9, 'Kropyvnytskiy': 10, 'Luhansk': 11, 'Lviv': 12, 'Mykolayiv': 13, 'Odesa': 14, 'Poltava': 15,
             'Rivne': 16, 'Sumy': 17,
             'Ternopil': 18, 'Kharkiv': 19, 'Kherson': 20, 'Khmelnytskyi': 21, 'Cherkasy': 22, 'Chernivtsi': 23,
             'Chernihiv': 24, 'Crimea': 25}

df = switch_indexation(df, new_pairs)
print(df.keys())
df['1'].head()


# -------------------------------------------
def get_year_vhi(region_idx, year):
    idx = str(region_idx)

    return df[idx][df[idx]['Year'] == str(year)]['VHI']


result = get_year_vhi(16, 2002).tolist()
print("VHI for region {} in a {}".format(16, 2002))
print(result)


# -------------------------------------------
def get_year_extr(region_idx, year):
    idx = str(region_idx)
    min_v = df[idx][df[idx]['Year'] == str(year)]['VHI'].min()
    max_v = df[idx][df[idx]['Year'] == str(year)]['VHI'].max()
    return min_v, max_v


result = get_year_extr(16, 2002)
print("VHI for region {} in a {}:".format(16, 2002))
print("min: {}\tmax: {}".format(result[0], result[1]))

# ------------------------------------------
import numpy as np


def get_extreme_drought_years(region_idx):
    idx = str(region_idx)
    df_drought = df[idx][df[idx].VHI <= 15]
    years = np.unique(df_drought['Year'])
    return (years)


result = get_extreme_drought_years(25)
print("Years with extreme drought level in region {}:".format(25))
for year in result:
    print(year)


# -------------------------------------------
def get_moderate_drought_years(region_idx):
    idx = str(region_idx)
    df_drought = df[idx][df[idx].VHI <= 35]
    years = np.unique(df_drought['Year'])
    return (years)


result = get_moderate_drought_years(16)
print("Years with moderate drought level in region {}:".format(16))
for year in result:
    print(year)
