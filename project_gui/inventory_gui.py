from tkinter import *

from tkinter import messagebox

MAX_STATS = (100,) * 2

# FIXME: Разобраться с артхаусом в окне


class InventoryGUI:

    def __init__(self, master, player_stats):

        self.master = master

        self._window_set(self.master, 'Инвентарь', (480, 184))

        self._set_player_data(player_stats)

        self._set_widgets()

    def _set_player_data(self, player_stats):

        self._inv = player_stats['INVENTORY']

        self._stats = player_stats['NUMERIC']

    def _set_widgets(self):

        self._title_w()

        self._inv_f_w()

        self._info_w()

        self._butts()

    def _title_w(self):

        stats_frame = Frame(self.master, relief=RAISED, bd=2)

        stats_frame.grid(row=0, columnspan=5, sticky=NSEW)

        Label(stats_frame, text='Информация о герое:', font=('Arial', 12), fg='purple').grid(row=0, columnspan=5,
                                                                                            sticky=NSEW)

        numeric_stats_frame = Frame(self.master, relief=RAISED, bd=2)

        numeric_stats_frame.grid(row=0, column=6, columnspan=6, sticky=EW)

        Label(numeric_stats_frame, text='HP:', font=('Arial', 12), fg='red').grid(row=0, sticky=EW)

        self.lbl_hp = Label(numeric_stats_frame, font=('Arial', 12))

        self.lbl_hp.grid(row=0, column=1, sticky=EW)

        Label(numeric_stats_frame, text='MP:', font=('Arial', 12), fg='blue').grid(row=0, column=2, sticky=EW)

        self.lbl_mp = Label(numeric_stats_frame, font=('Arial', 12))

        self.lbl_mp.grid(row=0, column=3, sticky=EW)

        self._update_numeric()

    def _update_numeric(self):

        self.lbl_hp.config(text='{} | {}'.format(self._stats['HP'], MAX_STATS[0]))

        self.lbl_mp.config(text='{} | {}'.format(self._stats['MP'], MAX_STATS[-1]))

    def _butts(self):

        butts_frame = Frame(self.master)

        butts_frame.grid(row=8, columnspan=16, sticky=EW)

        self.button_use = Button(butts_frame, text='Использовать', command=self._on_use)

        self.button_toss = Button(butts_frame, text='Выбросить', command=self._on_toss)

        self.button_quit = Button(butts_frame, text='Закрыть инвентарь', command=self._on_quit)

        self.button_use.grid(row=0, column=0, columnspan=2, sticky=EW)

        self.button_toss.grid(row=0, column=2, columnspan=4, sticky=EW)

        self.button_quit.grid(row=0, column=6, columnspan=4, sticky=EW)

    def _on_use(self):

        selection = self.items_list.curselection()

        if selection:

            id = list(self._inv.keys())[selection[0]]

            name = self._inv[id]['NAME']

            if self._inv[id]['USE']:

                self._stats['HP'] += self._inv[id]['HP']

                self._stats['MP'] += self._inv[id]['MP']

                lst = list(self._stats.keys())

                for i, stat in enumerate(lst):

                    if self._stats[stat] > MAX_STATS[i]:

                        self._stats[stat] = MAX_STATS[i]

                del self._inv[id]

                self._update_item_info(text='Предмет {} был использован.'.format(name))

                self._update_numeric()

                self._update_item_list()

            else:

                self._update_item_info(text='Предмет {} нельзя применить!'.format(name))

    def _on_toss(self):

        selection = self.items_list.curselection()

        if selection:

            id = list(self._inv.keys())[selection[0]]

            name = self._inv[id]['NAME']

            msg_ask = messagebox.askquestion('Предупреждение',
                                             'Вы действительно хотите выбросить предмет {}?'.format(name))

            if msg_ask == 'yes':

                del self._inv[id]

                self._update_item_info(text='Предмет {} был выброшен из инвентаря.'.format(name))

                self._update_item_list()

    def _on_quit(self):

        self.master.destroy()

    def _info_w(self):

        info_frame = Frame(self.master, relief=GROOVE, bd=2)

        info_frame.grid(row=1, column=6,
                        columnspan=6, rowspan=6,
                        sticky=EW)

        Label(info_frame, text='Описание предмета', font=('Arial', 11)).grid(row=0, sticky=EW)

        scrollbar = Scrollbar(info_frame)

        scrollbar.grid(row=1, column=6, sticky=NS, rowspan=5)

        self.info_text = Text(info_frame, height=5, width=36,
                              wrap=WORD, state=DISABLED, yscrollcommand=scrollbar.set)

        self.info_text.grid(row=1, columnspan=6, rowspan=5)

    def _inv_f_w(self):

        inventory_field = Frame(self.master, relief=GROOVE, bd=2)

        inventory_field.grid(row=1, columnspan=6, rowspan=6, sticky=EW)

        Label(inventory_field, text='Список предметов', font=('Arial', 11)).grid(row=0, sticky=EW)

        self.items_list = Listbox(inventory_field, height=5, font=('Arial', 11))

        self.items_list.grid(row=1, columnspan=6, rowspan=5, sticky=EW)

        self.items_list.bind('<<ListboxSelect>>', self._on_select_ev)

        self._update_item_list()

    def _on_select_ev(self, ev=None):

        item = self._inv[list(self._inv.keys())[self.items_list.curselection()[0]]]

        self._update_item_info(item=item['NAME'], text=item['INFO'])

    def _update_item_list(self):

        self.items_list.delete(0, END)

        for id_e in self._inv:
            self.items_list.insert(END, self._inv[id_e]['NAME'])

    def _update_item_info(self, item='', text=''):

        if text:

            if item:

                item += '\n\n'

            self.info_text.config(state=NORMAL)

            self.info_text.delete('1.0', END)

            self.info_text.insert(END, item + text)

            self.info_text.config(state=DISABLED)

    def _window_set(self, window, string, w_h):

        window.resizable(False, False)

        window.geometry('%ix%i' % w_h)

        window.grid_propagate(0)

        window.title("{}".format(string))

    def loop(self):

        self.master.mainloop()


if __name__ == '__main__':

    PLAYER_STATS = {'HP': 50, 'MP': 50}

    PLAYER_INV = {'1': {'NAME': 'Ананас',
                        'HP': 0,
                        'MP': 45,
                        'USE': True,
                        'INFO': 'Когда ты ешь его, он поедает тебя.\nПрибавляет 45 ед. маны.'},
                  '2': {'NAME': 'Молоко',
                        'HP': 50, 'MP': 0,
                        'USE': True,
                        'INFO': 'Амброзия кузена. Прибавляет 50 ед. здоровья'},
                  '3': {'NAME': 'Таумономикон',
                        'HP': 0, 'MP': 0,
                        'USE': False,
                        'INFO': 'Никому не доверяй'},
                  '4': {'NAME': 'Манговый нектар',
                        'HP': 25, 'MP': 45,
                        'USE': True,
                        'INFO': 'Не злоупотребляйте.\n+45 MP; +25 HP'},
                  '5': {'NAME': 'Виски',
                        'HP': -45, 'MP': 0,
                        'USE': True,
                        'INFO': 'Вредит здоровью.\n-30 HP'}}

    PLAYER = {'NUMERIC': PLAYER_STATS,
              'INVENTORY': PLAYER_INV}

    top = Tk()

    InventoryGUI(top, PLAYER).loop()