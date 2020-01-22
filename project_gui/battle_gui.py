import tkinter as tk

from tkinter import messagebox, TclError

from PIL import ImageTk, Image

import os

from utility.problem_generator import *


MAX_STATS = (100,) * 2


class BattleGUI:

    def __init__(self, master, stats, inv, enemy_stats):

        self.master = master

        self.victory = False

        self._player_stats_form(stats, inv)

        self._enemy_stats_form(enemy_stats)

        self._window_set(self.master, 'Battle!', (400, 242))

        self._set_widgets()

    def loop(self):

        self.master.mainloop()

        # TODO: Выдать плюшку

        return self.victory

    def _player_stats_form(self, max_hp_and_mp, inventory):

        self.stats = max_hp_and_mp

        self.inv = inventory

    def _show_results(self):

        if self.victory:

            messagebox.showinfo('Результат сражения',
                                'Игрок сразил противника {}!\nПобеда.'.format(self.enemy_name))

        else:

            messagebox.showinfo('Результат сражения',
                                'Игрок потерял сознание!\nПоражение.')

        self.master.destroy()

    def _enemy_stats_form(self, dct):

        self.enemy_name = dct['NAME']

        self.catchphrase = dct['CATCHPHRASE']

        self.enemy_curr_hp = self.enemy_max_hp = dct['MAXHP']

        self.enemy_atk, self.enemy_prob = dct['ATK'], dct['PROB']

        self.enemy_img = os.path.join(os.getcwd(), os.sep.join(dct['IMG']))

        self._enemy_tier = dct['TIER']

    def _check_player_numeric(self):

        if self.stats['HP'] <= 0:

            self._show_results()

        else:

            if self.stats['MP'] < 0:

                self.stats['MP'] = 0

    def _player_attack(self, damage):

        self.enemy_curr_hp -= damage

        self._enemy_attack(appendix='Герой наносит урон в {} ед.!'.format(damage))

        self._update_enemy_numeric()

    def _enemy_attack(self, appendix='', def_coefficient=None):

        d = 1

        if def_coefficient:

            d = def_coefficient

        if appendix:

            appendix += '\n\n'

        if self.enemy_curr_hp > 0:

            rand_coefficient = np.random.randint(0, 17)

            damage = int(d * 0.1 * rand_coefficient * self.enemy_atk)

            if np.random.binomial(1, self.enemy_prob):

                if not damage:

                    self._edit_text(appendix + '{} мало ел каши в детстве!'.format(self.enemy_name), True)

                else:

                    self.stats['HP'] -= damage

                    if rand_coefficient > 10:

                        self._edit_text(
                            appendix + '{} наносит коллосальный урон в {} ед. !'.format(self.enemy_name, damage), True)

                    else:

                        self._edit_text(appendix + '{} наносит урон в {} ед.'.format(self.enemy_name, damage), True)

            else:

                self._edit_text(appendix + '{} промахнулся!'.format(self.enemy_name), True)

            self._update_numeric()

            self._check_player_numeric()

        else:

            self.victory = True

            self._show_results()

    def _stats_w(self):

        stats_frame = tk.Frame(self.master, relief=tk.SUNKEN, bd=2)

        stats_frame.grid(row=0, column=0, rowspan=2, columnspan=2, sticky=tk.EW)

        tk.Label(stats_frame, text='HP:', fg='red').grid(row=0, column=0, sticky=tk.E)

        self.lbl_hp = tk.Label(stats_frame)

        self.lbl_hp.grid(row=0, column=1, columnspan=2, sticky=tk.W)

        tk.Label(stats_frame, text='MP:', fg='blue').grid(row=1, column=0, sticky=tk.E)

        self.lbl_mp = tk.Label(stats_frame)

        self.lbl_mp.grid(row=1, column=1, columnspan=2, sticky=tk.W)

        self._update_enemy_numeric()

        self._update_numeric()

    def _act_w(self):

        action_frame = tk.Frame(self.master, relief=tk.SUNKEN, bd=2)

        action_frame.grid(row=2, column=0, rowspan=3, columnspan=2, sticky=tk.EW)

        self.button_attack = tk.Button(action_frame, text='Атаковать', command=self._on_ev_atk_b)

        self.button_attack.grid(row=0, columnspan=3, sticky=tk.EW, padx=20)

        self.button_defend = tk.Button(action_frame, text='Оборониться', command=self._on_ev_def_b)

        self.button_defend.grid(row=1, columnspan=2, sticky=tk.EW, padx=20)

        self.button_inv = tk.Button(action_frame, text='Инвентарь', command=self._on_ev_inv_b)

        self.button_inv.grid(row=2, columnspan=2, sticky=tk.EW, padx=20)

    def _list_w(self):

        info_frame = tk.Frame(self.master, relief=tk.SUNKEN, bd=2)

        info_frame.grid(row=5, column=0, rowspan=3, columnspan=2)

        self.info_listbox = tk.Listbox(info_frame, height=5, width=20, state=tk.DISABLED)

        self.info_listbox.grid(row=0, sticky=tk.EW)

        self.info_listbox.config(state=tk.NORMAL)

        for item in self.inv:

            if self.inv[item] is not None:

                self.info_listbox.insert(tk.END, self.inv[item]['NAME'])

        self.info_listbox.config(state=tk.DISABLED)

        self.info_listbox.bind('<<ListboxSelect>>', self._selected_lstbox_inv)

        self.info_listbox.bind('<Double-Button>', self._on_clicked_item_ev)

    def _info_w(self):

        info_frame = tk.Frame(self.master, relief=tk.SUNKEN, bd=2)

        info_frame.grid(row=5, column=2, rowspan=3, columnspan=4)

        scrollbar = tk.Scrollbar(info_frame)

        scrollbar.grid(row=0, column=6, sticky=tk.NS)

        self.info_text = tk.Text(info_frame, font=('Arial', 10), height=5, width=30,
                              wrap=tk.WORD, state=tk.DISABLED, yscrollcommand=scrollbar.set)

        self.info_text.grid(row=0, columnspan=6, sticky=tk.NSEW)

        self._edit_text(self.catchphrase[np.random.randint(0, len(self.catchphrase) - 1)],
                        appendix='Начинается поединок между героем и противником {}!'.format(self.enemy_name))

        scrollbar.config(command=self.info_text.yview)

    def _image_w(self):

        img_frame = tk.Frame(self.master, relief=tk.SUNKEN, bd=2)

        img_frame.grid(row=0, column=2, rowspan=3, columnspan=5)

        pic = Image.open(self.enemy_img)

        img = ImageTk.PhotoImage(pic)

        self.panel = tk.Label(img_frame, image=img)

        self.panel.image = img

        self.panel.grid(row=0, column=1, sticky=tk.EW)

    def _edit_text(self, string, bold=None, appendix=''):

        if appendix:

            appendix += '\n\n'

        self.info_text.config(state=tk.NORMAL)

        self.info_text.delete('1.0', tk.END)

        self.info_text.insert(tk.END, appendix + string)

        if bold:

            self.info_text.config(font=('Arial', 10, 'bold'))

        else:

            self.info_text.config(font=('Arial', 10))

        self.info_text.config(state=tk.DISABLED)

    def _update_listbox(self):

        self.info_listbox.config(state=tk.NORMAL)

        self.info_listbox.delete(0, tk.END)

        for item in self.inv:

            if self.inv[item] is not None:

                self.info_listbox.insert(tk.END, self.inv[item]['NAME'])

        self.info_listbox.config(state=tk.DISABLED)

    def _update_stats(self):

        self._update_numeric()

        self._update_listbox()

    def _update_numeric(self):

        self.lbl_hp.config(text='{} | {}'.format(self.stats['HP'], MAX_STATS[0]))

        self.lbl_mp.config(text='{} | {}'.format(self.stats['MP'], MAX_STATS[-1]))

    def _update_enemy_numeric(self):

        try:
            self.master.title(
                'Противник: {} | HP: {} / {}'.format(self.enemy_name, self.enemy_curr_hp, self.enemy_max_hp))
        except TclError:
            pass

    def _selected_lstbox_inv(self, ev=None):

        try:
            self._edit_text(self.inv[list(self.inv.keys())[self.info_listbox.curselection()[0]]]['INFO'])
        except IndexError:
            pass

    def _on_closing_atk(self):

        res = self.entry.get()

        if res:

            try:
                res = list(map(float, res.split(' ')))

            except ValueError:

                self._enemy_attack(appendix='Пользователь оказался слепым, чтобы набрать правильный ответ.'.format())

            else:

                if res == self._task[1]:

                    dmg = np.random.randint(0, 4) + 10

                    self._player_attack(dmg)

                else:

                    self._enemy_attack(appendix='Герой слишком косой, чтобы попать по врагу..'.format())

        else:

            self._enemy_attack(appendix='Герой слишком косой, чтобы попать по врагу..'.format())

        try:
            self.attack_window.destroy()
        except TclError:
            pass

    def _on_closing_def(self):

        res = self.entry.get()

        if res:

            try:
                res = list(map(float, res.split(' ')))

            except ValueError:

                self._enemy_attack(appendix='Герой упустил свой шанс оборониться,'
                                            ' ибо неправильные заклинания применяет..'.format())

            else:

                if res == self._task[1]:

                    mana_power = np.random.randint(10, 21)

                    self.stats['MP'] += mana_power

                    self._chk_stats()

                    self._enemy_attack(appendix='Герой оборонился и повысил запасы маны на {} ед.!'.format(mana_power),
                                       def_coefficient=0.5)

                else:

                    self._enemy_attack(appendix='Герой упустил свой шанс оборониться,'
                                                ' ибо что-то неправильное прошептал себе под нос..'.format())

        else:

            self._enemy_attack(appendix='Герой упустил свой шанс оборониться..'.format())

        self.defense_window.destroy()

    def _mana_power(self):

        if self.stats['MP'] >= 25:

            self.stats['MP'] -= 25

            dmg = np.random.randint(4, 7) + 10

            self._player_attack(dmg)

        else:

            messagebox.showinfo('Неудача', 'Недостаточно маны для завершения заклинания!')

        try:
            self.attack_window.destroy()
        except TclError:
            pass

    def _on_ev_atk_b(self):

        self.attack_window = tk.Toplevel(self.master)  # TODO: Если открыто, блокировать виджеты главного!

        self.attack_window.grab_set()

        self._window_set(self.attack_window, 'Атака', (228, 296))

        self._task = ProblemGenerator(self._enemy_tier).get_task

        scrollbar = tk.Scrollbar(self.attack_window)

        scrollbar.grid(row=0, column=4, sticky=tk.NS)

        self.text_box = tk.Text(self.attack_window, width=26, height=12,
                             wrap=tk.WORD, state=tk.DISABLED, yscrollcommand=scrollbar.set)

        self.text_box.grid(row=0, column=0, sticky=tk.EW)

        self.text_box.config(state=tk.NORMAL)

        self.text_box.insert('1.0', self._task[0])

        self.text_box.config(state=tk.DISABLED)

        self.entry = tk.Entry(self.attack_window)

        self.entry.grid(row=1, columnspan=8)

        tk.Button(self.attack_window, text='Ответить', command=self._on_closing_atk).grid(row=2,
                                                                                           columnspan=8,
                                                                                           sticky=tk.EW)

        tk.Button(self.attack_window, text='Применить заклинание!', command=self._mana_power).grid(row=3,
                                                                                           columnspan=8,
                                                                                           sticky=tk.EW)


        self.attack_window.protocol("WM_DELETE_WINDOW", self._on_closing_atk)

    def _on_ev_def_b(self):

        self.defense_window = tk.Toplevel(self.master)

        self.defense_window.grab_set()

        self._window_set(self.defense_window, 'Оборона', (228, 264))

        self._task = ProblemGenerator(self._enemy_tier + 1).get_task

        scrollbar = tk.Scrollbar(self.defense_window)

        scrollbar.grid(row=0, column=4, sticky=tk.NS)

        self.text_box = tk.Text(self.defense_window, width=26, height=12,
                             wrap=tk.WORD, state=tk.DISABLED, yscrollcommand=scrollbar.set)

        self.text_box.grid(row=0, column=0, sticky=tk.EW)

        self.text_box.config(state=tk.NORMAL)

        self.text_box.insert('1.0', self._task[0])

        self.text_box.config(state=tk.DISABLED)

        self.entry = tk.Entry(self.defense_window)

        self.entry.grid(row=1, columnspan=8)

        tk.Button(self.defense_window, text='Ответить', command=self._on_closing_def).grid(row=2,
                                                                                           columnspan=8,
                                                                                           sticky=tk.EW)

        self.defense_window.protocol("WM_DELETE_WINDOW", self._on_closing_def)

    def _on_ev_inv_b(self, ev=None):

        if self.info_listbox['state'] == tk.DISABLED:

            self._edit_text('Выберите предмет', True)

            self.info_listbox.config(state=tk.NORMAL)

        else:

            self.info_listbox.config(state=tk.DISABLED)

            self._edit_text(self.catchphrase[np.random.randint(0, len(self.catchphrase))])

    def _chk_stats(self):

        lst = list(self.stats.keys())

        for i, stat in enumerate(lst):

            if self.stats[stat] > MAX_STATS[i]:
                self.stats[stat] = MAX_STATS[i]

    def _on_clicked_item_ev(self, ev=None):

        if self.info_listbox['state'] == tk.NORMAL:

            item = list(self.inv.keys())[self.info_listbox.curselection()[0]]

            item_name = self.inv[item]['NAME'].lower()

            if self.inv[item]['USE']:

                self.stats['HP'] += self.inv[item]['HP']

                self.stats['MP'] += self.inv[item]['MP']

                self._chk_stats()

                del self.inv[item]

                self._update_stats()

                self._enemy_attack(appendix='Использован предмет {}'.format(item_name))

            else:

                self._edit_text('Предмет {} нельзя использовать в бою!'.format(item_name), True)

    def _set_widgets(self):

        self._stats_w()

        self._act_w()

        self._list_w()

        self._info_w()

        self._image_w()

    def _window_set(self, window, string, w_h):

        window.resizable(False, False)

        window.geometry('%ix%i' % w_h)

        window.grid_propagate(0)

        window.title(string)
