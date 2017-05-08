# import json
#
# import urllib3
# from pandas import Series
# from pandas import DataFrame
#
#
# class EIA_Data:
#     def __init__(self):
#         self.base_url = 'http://www.eiayuanyoukucun.com'
#         self.weekly_data = 'index.php?g=app&m=Index&a=getrdata'
#         self.http = urllib3.PoolManager()
#         self.save_path = '../STATIC/EIA_data.csv'
#
#     def get_weekly_series(self, Id):
#         url = '/'.join([self.base_url, self.weekly_data])
#         res = self.http.request('post', url, fields={'id': Id})
#         return Series(json.loads(res.data))
#
#     def get_data_as_dataframe(self):
#         data = []
#         Id = 0
#         index = 0
#         while index != 2:
#             Id += 1
#             info = self.get_weekly_series(Id)
#             if 'error' in info:
#                 index += 1
#             else:
#                 data.append(info)
#         return DataFrame(data)
#
#     def sava_data_as_csv(self):
#         self.get_data_as_dataframe().to_csv(self.save_path, encoding='utf-8')
#
# eia = EIA_Data()
#
# eia.sava_data_as_csv()
#

import json

import urllib3
from pandas import Series
from pandas import DataFrame


class EIA_Data:
    def __init__(self):

        self.base_url = 'http://www.cnoil.com/calendar'
        self.weekly_data = 'ajaxHistroy?'
        self.http = urllib3.PoolManager()
        self.save_path = '../STATIC/EIA_data_2.csv'

        self.id = 665
        self.pages = self.get_pages()

    def get_pages(self):
        url = '/'.join([self.base_url, ''.join([self.weekly_data, 'page=0&id=' + str(self.id)])])
        return json.loads(self.http.request('get', url).data)['pages']

    def get_data_page(self, page):
        url = '/'.join([self.base_url, ''.join([self.weekly_data, 'page=' + str(page) + '&id=' + str(self.id)])])
        return json.loads(self.http.request('get', url).data)['data']

    def get_data_as_dataframe(self):
        data = []
        for arr in [[Series(temp) for temp in self.get_data_page(index)] for index in range(1, self.pages + 1)]:
            data.extend(arr)
        return DataFrame(data)

    def sava_data_as_csv(self):
        self.get_data_as_dataframe().to_csv(self.save_path, encoding='utf-8')

api = EIA_Data()

api.sava_data_as_csv()

