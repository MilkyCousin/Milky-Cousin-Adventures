import json
import os


class ConfigUploadJSON:

    def __init__(self):

        self.__fields_list = ['FPS', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'OPEN_INV', 'TAKE_PHOTO', 'VOLUME']

        self.__default_values = [60, 119, 115, 97, 100, 105, 107, 1]

        self.__config_dict = dict.fromkeys(self.__fields_list, None)

        self._path = os.path.join(os.getcwd(), 'utility', 'config', 'config.json')

        if not os.path.exists(self._path):

            self.__make_file()

        if not self._without_nulls():

            self.__fill_with_default_values()

    def _without_nulls(self):

        with open(self._path, 'r') as f:

            if None in json.load(f).values():

                return False

        return True

    def __fill_with_default_values(self):

        self.__edit_file(self.__default_values)

    def __make_file(self):

        with open(self._path, 'w') as f:

            json.dump(self.__config_dict, f, indent=4)

    def __edit_file(self, lst):

        for i, value in enumerate(lst):
            if value is not None:
                self.__config_dict[list(self.__config_dict.keys())[i]] = value

        with open(self._path, 'w') as f:
            json.dump(self.__config_dict, f, indent=4)

        self.__config_dict = dict.fromkeys(self.__fields_list, None)

    def upload_modified_data(self):

        return json.load(open(self._path, 'r'))

    def set_default_data(self):

        self.__fill_with_default_values()

    def items_and_values(self, list_of_values):

        self.__edit_file(list_of_values)

    def edit_parameters(self):

        modified = self.upload_modified_data()

        try:

            import parameters as parameters_thing

        except ImportError:

            pass

        finally:

            for key in modified:

                exec('parameters_thing.{} = {}'.format(key, modified[key]))
