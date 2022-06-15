# Milky-Cousin-Adventures

<p align="center">
  <img src=https://user-images.githubusercontent.com/45886410/173920445-09f3a94a-4a03-4455-af72-ea479dce0351.gif alt="animated">
</p>

<p align="center">
<i>How about some magic, combined with linear algebra and penguins?</i>
</p>

## English version

In progress.. Briefly, it is badly written tile-based game in python.

## Ukrainian version

Цей репозиторій містить простеньку гру під назвою "Пригоди молочного кузена", що була запропонована в якості програмного проекту з дисципліни "Прикладне програмування" на другому курсі бакалаврату. Додатково наводиться реалізація елементарного серверу на основі wsgi, що містить певні літературні "подвиги" автора. Програмний проект був написаний на колінці, за одну ніч напередодні дедлайну, тому містить багато промахів, які варто виправити (от, наприклад, про підхід зберігання даних про гру).

Пакети, що використовувалися у проекті за виключенням стандартних: Pillow, pygame, numpy та openpyxl.

Прогрес користувача зберігається у відповідному JSON файлі, що ''зашифровується''. Рівні (мапи) зберігаються в таблицях MS Excel. Описи істот, предметів теж задаються у форматі JSON. У такому стилі, напевно, простіше ''оновлювати'' гру новим контентом, однак практично це виглядає досить специфічно.

Структура гри віддалено нагадує ігри в RPG-стилі. Персонаж подорожує мапами, збирає усілякий мотлох, бореться проти містичних створінь, розв'язуючи задачі з лінійної алгебри.

<p align="center">
  <img src=https://user-images.githubusercontent.com/45886410/173909541-ede913d9-f51f-4d34-a1bb-44eb796d31b2.png>
</p>

Файл **main.py** реалізує головне вікно та головне меню гри. З головного меню відходить п'ять шляхів:

- **Start Game** -- безпосередньо розпочати гру. Якщо попередньо зберігалася гра, то корисувачу пропонується або відновити попередній результат, або все заново розпочати.
- **Settings** -- базові налаштування гри. Здебільшого присвячується налаштуванню клавіш керування персонажем. Також є налаштування аудіо та кількості передачі кадрів в секунду (FPS).

<p align="center">
  <img src=https://user-images.githubusercontent.com/45886410/173922352-53b5cf79-e406-44b6-b5b2-6ef2cc2af09e.png>
</p>

- **Game Manual** -- короткі відомості про гру: про що вона, що треба робити та навіщо. У двох словах описана загальна техніка бою з містичними створіннями.

<p align="center">
  <img src=https://user-images.githubusercontent.com/45886410/173926557-7672abc4-85a3-45f6-ba15-97c29c604c18.gif alt="animated">
</p>

- **Visit developer's website** -- посилає користувача на сторінку (https://milkycousin.pythonanywhere.com/) з короткими розповідями від розробника, на основі яких *безспосередньо* "основана" сама гра.

Файл **sprites_env.py** реалізує підвантаження мап, персонажів на основі зчитування JSON, Excel файлів. **player_inventory.py** є "ключем", що імплементує інвентар головного персонажа -- зберігання, використання тих чи інших речей. Незмінні параметри (які, справді кажучи, можна змінити) зберігаються у **parameters.py**. Підвантаження даних користувача та даних про предметі та істоти беруть на себе скрипти **utility/json_config_uploader.py**, **ingame_data/player_data/json_player_data_upload.py** та **ingame_data/json_data_upload.py**.

Процесор для випадкового створення задач з лінійної алгебри реалізується у файлах **problem_generator.py** (безпосередньо сам процесор) та **randomizer.py** (випадкова компонента процесора). Задачі здебільшого на обчислення: знаходження власних чисел симетричної матриці, обчислення норми вектора або скалярного добутку векторів, визначника матриці тощо. Складність полягає у більших розмірностях векторів чи матриць, в залежності від "складності" ворога.

Вікна для боїв з істотами та для інвентарю персонажа описані у **/project_gui/battle_gui.py** та **/project_gui/inventory_gui.py** відповідно.

Серверна частина роботи (так звана сторінка розробника) лежить у файлі **webserver/app.py**. Досить проста реалізація за допомогою cgi.
