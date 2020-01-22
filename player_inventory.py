class Inventory:
    """
    Класс, задающий уникальный, но примитивный способ хранения элементов ( предметов )
    в хранилище ( инвентаре ) игрока.
    Описаны следующие методы:
    - Добавить элемент в инвентарь
    - Удалить предмет из инвентаря
    При помощи спец. методов:
    - Проверка на заполненность инвентаря
    - Получение предмета за числом
    - Возвращение уровня заполненности инвентаря
    """
    def __init__(self):

        self._limit = 5

        self.__items = {}

        self.__curr_id = '0'

    def append(self, item):

        self.__items[str(self.__curr_id)] = item

        self.__items = dict(zip(list(map(str, range(1, len(self.__items) + 1))), self.__items.values()))

    def pop(self, id_e):

        try:

            del self.__items[id_e]

            self.__items = dict(zip(list(map(str, range(1, len(self.__items) + 1))), self.__items.values()))

        except KeyError:

            return False

        return True

    def __bool__(self):

        return len(self) != self._limit

    def __len__(self):

        return len(self.__items)

    def __getitem__(self, key):

        return self.__items[key]

    @property
    def get_items(self):

        return self.__items

    @property
    def get_current_id(self):

        return self.__curr_id


class NumericStats:
    """
    Класс, описывающий структуру хранения показатели здоровья и маны игрока.
    Дополнительное свойство описано для возвращения данных класса.
    """
    def __init__(self, hp=0, mp=0):

        self.__stats = {'HP': hp,
                        'MP': mp}

    @property
    def get_numeric(self):

        return self.__stats


if __name__ == '__main__':

    ...
