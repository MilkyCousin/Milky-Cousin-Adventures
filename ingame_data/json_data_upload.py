import json
import os

from random import randint


class ItemDataUploadJSON:

    def __init__(self):

        self._converter = {0: 'COMMON',
                      1: 'RARE',
                      2: 'UNIQUE_UPGRADES',
                      3: 'FROM_BOSSES'}

        self.__path = os.path.join(os.getcwd(), 'ingame_data', 'items', 'items.json')

        self.__dict = None

    def _load_data(self):

        with open(self.__path, 'r') as f:

            self.__dict = {dick['TYPE']: dick['ITEMS'] for dick in json.load(f)}

    def load_data_by_type(self, type_key):

        self._load_data()

        return self.__dict[self._converter[type_key]]

    def get_random_item_by_type(self, type_key):

        data = self.load_data_by_type(type_key)

        return data[randint(0, len(data)-1)]

    def get_specific_rare_item(self, index):

        data = self.load_data_by_type(1)

        return data[index] if 0<=index<=len(data)-1 else data[0]

    def get_specific_boss_item(self, index):

        data = self.load_data_by_type(3)

        return data[index] if 0<=index<=len(data)-1 else data[0]

    @property
    def load_data(self):

        self._load_data()

        return self.__dict


class EntityDataUploadJSON:

    def __init__(self):

        self.__path = os.path.join(os.getcwd(), 'ingame_data', 'mob_data', 'mobs.json')

        self.__data_list = None

    def _load_data(self):

        with open(self.__path, 'r') as f:

            self.__data_list = json.load(f)

    def load_data(self):

        self._load_data()

    def get_mob_by_id(self, index):

        self._load_data()

        return self.__data_list[index]
