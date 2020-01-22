import tkinter as tk


class InformationWindow:

    def __init__(self, top, text_info='', title='', *button_args):

        self.master = top

        self.text_info = text_info

        self.buttons = button_args

        self.master.title(title)

        self.master.geometry('320x64')

        self.master.resizable(False, False)

        self._loop()

    def _loop(self):

        self._show_information()

        self.master.mainloop()

    def _quit(self, ev=None):

        self.master.destroy()

    def _show_information(self):

        label_info = tk.Label(self.master, text=self.text_info)

        label_info.pack(side=tk.TOP, fill='x')

        button_exit = tk.Button(self.master, text=self.buttons[0], command=self._quit)

        button_exit.pack(side=tk.TOP)


class ChestContainsWindow(InformationWindow):

    def __init__(self, top, text_info='', *button_args):

        InformationWindow.__init__(self, top, text_info, 'Находка в сундуке', *button_args)


class SignWindow(InformationWindow):

    def __init__(self, top, text_info=''):

        InformationWindow.__init__(self, top, text_info, 'Табличка', 'Закрыть')


class SavePlayerDataWindow(InformationWindow):

    def __init__(self, top):
        ...


    def _locate_widgets(self):
        ...


    def loop(self):

        self._top.mainloop()
