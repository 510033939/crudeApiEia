import json

import urllib3
from pandas import Series
from pandas import DataFrame


class API_Data:
    def __init__(self):

        self.base_url = 'http://www.cnoil.com/calendar'
        self.weekly_data = 'ajaxHistroy?'
        self.http = urllib3.PoolManager()
        self.save_path = '../STATIC/API_data.csv'

        self.id = 663
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

api = API_Data()

api.sava_data_as_csv()

