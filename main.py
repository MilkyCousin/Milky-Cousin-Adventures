from sprites_env import *

from utility.json_config_uploader import *

from tkinter import *

import os

import codecs

import webbrowser


# TODO: Случайное перемещение монстров


class MainMenuWindow:
    """
    Окно запуска программы.
    С ним связаны следующие события:
    - Начало игры, т.е. создание или загрузка данных об игроке
    - Настройки управления
    - Руководство по игре
    - Загрузка сайта разработчика программы
    """
    def __init__(self):

        self._configure_json = ConfigUploadJSON()

        self._master = Tk()

        self._map_processor = MapProcessor()

        self._window_set(self._master, 'Main', (480, 240))

        self._set_widgets()

        self._mainloop()

    def _set_icon(self, window):

        from platform import system as platform_system

        window.iconbitmap({'Windows': os.path.join(os.getcwd(), 'misc', 'icon_main.ico'),
                           'Linux': '@' + os.path.join(os.getcwd(), 'misc', 'icon_main.xbm')}[platform_system()])

    def _goto_web(self):

        webbrowser.open('http://milkycousin.pythonanywhere.com/')

    def _window_set(self, window, string, w_h):

        window.resizable(False, False)

        window.geometry('%ix%i' % w_h)

        window.pack_propagate(0)

        window.title("{}".format(string))

        self._set_icon(window)

    def _restart_program(self):

        python_exec = sys.executable

        os.execl(python_exec, python_exec, *sys.argv)

    def _init_game(self):

        if PlayerDataJSON():

            if messagebox.askquestion('Внимание',
                                   'Вы хотите загрузить данные из последней записи ({date})\n'
                                   'или желаете начать новую игру?'.format(date=PlayerDataJSON().get_time)) == 'no':

                PlayerDataJSON().form_data()

        self._master.destroy()

        self._map_processor.json_data_load(PlayerDataJSON().get_data)

        PyGameWindow(self._configure_json, self._map_processor)

        self._restart_program()

    def get_key(self, e, label, t):

        try:

            key = {'ASCII': ord(e.char)}

            self.label_box[int(t) - 1].configure(text=key['ASCII'])

            self.top_key.destroy()

        except TypeError:

            label.configure(text='Нажмите другую клавишу...')

    def _top_level_set_key(self, t, ev=None):

        self.top_key = Toplevel(self.settings_frame)

        self.top_key.grab_set()

        self.top_key.title('KeyDetect')

        label = Label(self.top_key, text='Нажмите любую клавишу...')

        label.pack()

        self.top_key.bind('<KeyPress>', lambda e: self.get_key(e, label, t))

    def _controls_frame(self):

        self.settings_frame = Frame(self.settings_window,
                                    relief=RIDGE, bd=2)

        self.settings_frame.grid(row=1, column=0, rowspan=10, columnspan=8, sticky=EW)

        Label(self.settings_frame, text='Control settings:').grid(row=0, column=0, columnspan=8, sticky=EW)

        params_list = ['Move upwards', 'Move downwards', 'Move to the left', 'Move to the right',
                       'Open inventory', 'Take a screenshot']

        self.label_box = []

        for i, param_name in enumerate(params_list):

            Label(self.settings_frame, text=param_name).grid(row=2*i+1, column=0, columnspan=4, sticky=NSEW)

        self.button_box = []

        for i in range(1, 7):

            self.button_box.append(Button(self.settings_frame, text=str(i),
                                          command=lambda t=str(i): self._top_level_set_key(t)))

            self.button_box[i-1].grid(row=2*i - 1, column=4, columnspan=4, sticky=NSEW)

            self.label_box.append(Label(self.settings_frame, text='::key::'))

            self.label_box[i-1].grid(row=2*i, column=0, columnspan=4, sticky=NSEW)

    def _video_frame(self):

        self.video_settings_frame = Frame(self.settings_window,
                                    relief=RIDGE, bd=2)

        self.video_settings_frame.grid(row=11, column=0, rowspan=2, columnspan=8, sticky=EW)

        params_list = ['Frames Per Second']

        for i, param_name in enumerate(params_list):
            Label(self.video_settings_frame, text=param_name).grid(row=i, column=0, columnspan=4, sticky=NSEW)

        variable = IntVar()

        self.scale_video = Scale(self.video_settings_frame, variable=variable, orient=HORIZONTAL,
                                 from_=15, to=60, length=240)

        self.scale_video.grid(row=1, column=0, columnspan=8, sticky=NSEW)

    def _audio_frame(self):

        self.audio_settings_frame = Frame(self.settings_window,
                                          relief=RIDGE, bd=2)

        self.audio_settings_frame.grid(row=13, column=0, rowspan=2, columnspan=8, sticky=EW)

        params_list = ['Audio Volume']

        for i, param_name in enumerate(params_list):
            Label(self.audio_settings_frame, text=param_name).grid(row=i, column=0, columnspan=4, sticky=NSEW)

        variable = IntVar()

        self.scale_audio = Scale(self.audio_settings_frame, variable=variable, orient=HORIZONTAL, length=240)

        self.scale_audio.grid(row=1, column=0, columnspan=8, sticky=NSEW)

    def _settings(self):

        def _s_quit(self, params):

            self._configure_json.items_and_values(params)

            self.settings_window.destroy()

        self.settings_window = Toplevel(self._master)

        self.settings_window.grab_set()

        self._window_set(self.settings_window, 'Settings', (252, 532))

        self.label_fr = Frame(self.settings_window, relief=RIDGE, bd=2)

        self.label_fr.grid(row=0, column=0, columnspan=8, sticky=EW)

        Label(self.label_fr, text="Settings:", fg="purple", font=("Arial", 12)).grid(row=0, column=0,
                                                                                      columnspan=8, sticky=EW)

        self._controls_frame()

        self._video_frame()

        self._audio_frame()

        parameters = self._configure_json.upload_modified_data()

        print(parameters)

        for i, elem in enumerate(list(parameters.values())[1:-1]):

            self.label_box[i].configure(text=elem)

        self.scale_video.set(parameters['FPS'])
        self.scale_audio.set(parameters['VOLUME'] * 100)

        Button(self.settings_window, text="Close",
               command=lambda : _s_quit(self,
                                        [self.scale_video.get(),
                                         self.label_box[0]['text']] +     # піймав баг, гыг
                                        [int(self.label_box[i]['text']) for i in range(len(self.label_box))][1:] +
                                        [self.scale_audio.get() / 100])).grid(row=16, column=0, columnspan=8, sticky=EW)

    def _guide(self):

        guide_window = Toplevel(self._master)

        guide_window.grab_set()

        self._window_set(guide_window, 'Guide', (320, 200))

        def _g_quit():
            guide_window.destroy()

        def format(text_widget):

            text_widget.configure(state=NORMAL)

            #text_widget.insert('1.0', open(os.path.join(os.getcwd(), 'misc', 'guide.txt'), 'r', encoding='utf-8').read())
            text_widget.insert('1.0', codecs.open(os.path.join(os.getcwd(), 'misc', 'guide.txt'),
                                                  "r",
                                                  "utf_8_sig").read())

            text_widget.configure(state=DISABLED)

        Label(guide_window, text="Game Manual", fg="purple", font=("Arial", 12)).pack(fill='x')

        scrollbar = Scrollbar(guide_window)

        Button(guide_window, text="Quit", command=_g_quit).pack(side='bottom', padx=5, pady=2, fill='x')

        scrollbar.pack(side=RIGHT, fill='y')

        text = Text(guide_window, height=8, wrap=WORD, state=DISABLED, yscrollcommand=scrollbar.set)

        format(text)

        text.pack(side='top', padx=5, pady=2, fill='x')

        scrollbar.config(command=text.yview)

    def _quit(self):

        exit()

    def _set_widgets(self):

        for elements in [["Milky Cousin Adventures", "purple", ("Arial", 16), "top"],
                         ["with love from danielthehuman", "black", ("Arial", 8), "bottom"]]:

            Label(self._master, text=elements[0], fg=elements[1], font=elements[2]).pack(fill='x',
                                                                                         side=elements[3])

        for elements in [["Start Game",self._init_game, "top"],
                      ["Settings",self._settings, "top"],
                      ["Game Manual", self._guide, "top"],
                      ["Quit", self._quit, "bottom"],
                      ["Visit developer's website", self._goto_web, "bottom"]]:

            Button(self._master, text=elements[0], command=elements[1]).pack(side=elements[2], padx=5, pady=2, fill='x')

    def _mainloop(self):

        self._master.mainloop()


class PyGameWindow:
    """
    Класс, отвечающий за инициализацию игрового окна.
    Взаимодействует с остальными компонентами проекта.
    В нём описана поддержка игрового процесса вплоть до закрытия программы.
    """
    def __init__(self, config_json: ConfigUploadJSON, map_processor: MapProcessor):

        pg.init()

        self.config_json = config_json

        self.map_processor = map_processor

        self.screen = pg.display.set_mode((parameters_thing.WIDTH, parameters_thing.HEIGHT))

        self.clock = pg.time.Clock()

        self._executable = True

        pg.display.set_caption('Milky Cousin Adventures')

        pg.display.set_icon(pg.image.load(os.path.join(os.getcwd(), 'misc', 'icon_main.ico')))

        self._run()

    def _draw_operations(self):

        self.screen.fill(BLACK)

        all_sprites_group.draw(self.screen)

        layered.draw(self.screen)

        pg.display.flip()

    def _update_sprite_states(self):

        all_sprites_group.update()

    def _handle_events(self):

        for ev in pg.event.get():

            if ev.type == pg.QUIT:

                self._executable = False

    def _run(self):

        self.config_json.edit_parameters()

        self.map_processor.set_volume()

        while self._executable:

            self.clock.tick(parameters_thing.FPS)

            self._handle_events()

            self._update_sprite_states()

            self._draw_operations()

            if parameters_script.BOOL:

                for sprite in all_sprites_group:

                    if isinstance(sprite, Player):

                        info = sprite.get_data

                        self.map_processor.clean_surface()

                        try:

                            self.map_processor.current_data_upload(PlayerDataJSON().transform_to_dict(info))

                        except TypeError as e:

                            print(e)  # 4st

                parameters_script.BOOL = False

                parameters_script.NEXT_MAP = None

            if parameters_thing.DEATH:

                self.map_processor.clean_surface()

                self.map_processor.json_data_load(PlayerDataJSON().get_data)

                parameters_thing.DEATH = False

            if parameters_thing.SCREENSHOT:

                import utility.randomizer as randomizer

                pg.image.save(self.screen, os.path.join(os.getcwd(), 'screenshots', randomizer.str_random() + '.png'))

                parameters_thing.SCREENSHOT = False

        pg.quit()


if __name__ == '__main__':

    MainMenuWindow()
