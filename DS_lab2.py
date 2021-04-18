from spyre import server
import pandas as pd

pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns
# import urllib.request as req
# import json
import DS_lab1

# retrieve data and make dataframe

# for i in range(1, 28):
#     if i in [12, 20]:
#         continue  # not retrieving data for KyivCity and Sevastopol'
#     else:
#         DS_lab1.get_vha_data(i)

df = DS_lab1.files_to_dataframe(r'./')

regions_idx = {'Vinnytsya': 1, 'Volyn': 2, 'Dnipro': 3, 'Donetsk': 4, 'Zhytomyr': 5, 'Zakarpattya': 6, 'Zaporizhya': 7,
               'Frankivsk': 8,
               'Kyiv': 9, 'Kropyvnytskiy': 10, 'Luhansk': 11, 'Lviv': 12, 'Mykolayiv': 13, 'Odesa': 14, 'Poltava': 15,
               'Rivne': 16, 'Sumy': 17,
               'Ternopil': 18, 'Kharkiv': 19, 'Kherson': 20, 'Khmelnytskyi': 21, 'Cherkasy': 22, 'Chernivtsi': 23,
               'Chernihiv': 24, 'Crimea': 25}

df = DS_lab1.switch_indexation(df, regions_idx)

# --------------------------------

regions_dropdown_options = []
for key, value in regions_idx.items():
    regions_dropdown_options.append({'label': key, 'value': value})


# --------------------------------

class WebApp(server.App):
    title = 'Global Vegetation Health Products in Ukraine'
    inputs = [{"type": 'radiobuttons',
               "label": 'Select data',
               "options": [{'label': 'VCI', 'value': 'VCI', 'checked': True},
                           {'label': 'TCI', 'value': 'TCI'},
                           {'label': 'VHI', 'value': 'VHI'}],
               "key": 'data_type',
               "action_id": 'update_data'
               },
              {"type": 'dropdown',
               "label": 'Select region',
               "options": regions_dropdown_options,
               "key": 'region_idx',
               "action_id": "update_data"
               },
              {"type": 'text',
               "key": 'year',
               "label": 'Select year (1981-2020)',
               "value": '2020',
               "action_id": 'update_data'
               },
              {"type": 'text',
               "key": 'week_range',
               "label": 'Week range',
               "value": '1-52',
               "action_id": 'update_data'
               }]

    controls = [{"type": "hidden",
                 "id": "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [{"type": 'plot',
                "id": 'plot',
                "control_id": 'update_data',
                "tab": "Plot"
                },
               {"type": 'table',
                "id": 'table_id',
                "control_id": 'update_data',
                "tab": "Table",
                "on_page_load": True
                }]

    # def getHTML(self, params):
    #     week_range = params["week_range"]
    #     return week_range

    def getData(self, params):
        region_idx = params['region_idx']
        year = params['year']
        week_range = list(map(int, params['week_range'].split('-')))

        idx = str(region_idx)
        dataframe = df[idx][df[idx]['Year'] == str(year)][
                        (df[idx]['Week'] >= week_range[0]) & (df[idx]['Week'] <= week_range[1])]

        return dataframe

    def getPlot(self, params):
        dataframe = self.getData(params)
        data_type = params['data_type']

        plt.figure(figsize=(20, 10))

        sns.set_theme(style='whitegrid')

        fig = sns.barplot(x='Week', y=data_type, data=dataframe)

        plt.xlabel("Week")
        plt.ylabel(data_type)
        return fig


app = WebApp()
app.launch()
