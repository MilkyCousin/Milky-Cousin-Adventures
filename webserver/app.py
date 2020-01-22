import cgi
import os
import re

from wsgiref.simple_server import make_server


START_PAGE = os.path.join(os.getcwd(), 'index.html')

FOLDER = os.path.join(os.getcwd(), 'stories')


class ServerApp:

    def __init__(self):

        self.commands = {
            '':             self.start,
            'open_text':    self.text
        }

    def __call__(self, environ, start_response):

        command = environ.get('PATH_INFO', '').lstrip('/')

        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        body = None

        error = False

        if command in self.commands:

            body = self.commands[command](form)

            if body:

                start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

            else:

                error = True

        if error:

            start_response('404 NOT FOUND', [('Content-type', 'text/plain')])

            body = 'Even Archmage can\'t achieve this page, but you did'

        return [bytes(body, encoding='utf-8')]

    def start(self, form=None):

        with open(START_PAGE) as f:

           lines = f.readlines()

        opt_pattern = '<option value="{v}">{v}</option>\n'

        value = '<option value="Выберите главу" disabled>Выберите главу</option>\n'

        value += ''.join([opt_pattern.format(v=re.sub('.txt', '', element))
                          for element in sorted(os.listdir(FOLDER))])

        key = "{text_selector}"

        for i, line in enumerate(lines):

            if key in line:

                j = line.find(key)

                lines[i] = line[:j] + value + line[j+len(key):]

        return ''.join(lines)

    def text(self, form):

        file = form['text'].value + '.txt'

        return '<br>'.join(open(FOLDER + os.sep + file, 'r').readlines())

if __name__ == '__main__':

    print('SERVER')

    controller = ServerApp()

    server = make_server('localhost', 1930, controller)

    server.serve_forever()