import json
import requests
from Utils.variable import API_URL
from Utils.observable import Observable


class AltevistaDB:
    def __init__(self, API_URL: str = API_URL):
        self.API_URL = API_URL
        self.DB_maps = Observable()

    def get_maps(self):

        maps_datas = None

        response = requests.post(
            url=API_URL,
            data=json.dumps({
                'action': 'GetMaps',
                'data': {}
            })
        )

        if response.status_code == 200:
            maps_datas = response.json()['Data']
            self.DB_maps.set(maps_datas)

        return maps_datas

    def get_map(self, map_name: str) -> dict[str, str]:

        response = requests.post(
            url=self.API_URL,
            data=json.dumps({
                'action': 'GetMap',
                'data': {
                    'map_name': map_name
                }
            })
        )

        map_data = response.json()

        # print(map_data)

        return map_data

    def add_map(self, map_data):

        response = requests.post(
            url=self.API_URL,
            data=json.dumps({
                'action': 'AddMap',
                'data': map_data
            })
        )

        print(response.text)
        # print(response.json())

    def edit_map(self, map_data):

        print(map_data)

        response = requests.post(
            url=self.API_URL,
            data=json.dumps({
                'action': 'EditMap',
                'data': map_data
            })
        )

        if response.json()['Status'] == 1:
            print(response.json()['Data'])
            raise Exception('Error while updating map')
