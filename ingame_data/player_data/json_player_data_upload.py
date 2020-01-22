import base64
import datetime as dt
import json
import os
import pygame as pg
import parameters as parameters_thing


class PlayerDataJSON:

    def __init__(self):

        self._path = os.path.join(os.getcwd(), 'ingame_data', 'player_data', 'player_data.txt')

        self._fields = ['MAP',
                        'TOP_LEFT_COORDINATES',
                        'DATE',
                        'HP',
                        'MP',
                        'INVENTORY',
                        'LOG']

        self._default = ['tutorial0',
                         [32, 32],
                         dt.datetime.today().strftime("%d-%m-%Y, %H:%M:%S"),
                         100,
                         100,
                         {},
                         []]

        self._dict = dict(zip(self._fields, self._default))

    def form_data(self, data=None):

        if data is not None:
            s = json.dumps(dict(zip(self._fields, data)), indent=4).encode()
        else:
            s = json.dumps(self._dict, indent=4).encode()

        with open(self._path, 'wb') as f:

            f.write(base64.b16encode(s))  # Защита уровня Microsoft Defender

    def upload(self):

        parameters_thing.BOOL = True

        parameters_thing.NEXT_MAP = self.get_data

    def transform_to_dict(self, data: list):

        return dict(zip(self._fields, data))

    def __bool__(self):

        return os.path.exists(self._path)

    @property
    def get_time(self):

        if not self:

            self.form_data()

        with open(self._path, 'rb') as f:

            return json.loads(base64.b16decode(f.read().decode()))['DATE']

    @property
    def get_data(self):

        if not self:

            self.form_data()

        with open(self._path, 'rb') as f:

            return json.loads(base64.b16decode(f.read().decode()))
