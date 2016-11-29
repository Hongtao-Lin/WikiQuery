# -×- coding: utf-8 -*-
from flask.ext.script import Manager, Server
from app import app
from app.models import Message

manager = Manager(app)

manager.add_command("runserver",
                    Server(host='localhost',
                           port=22027,
                           use_debugger=True))
@manager.command
def save_msg():
    m = Message(author="defshine", content="my first msg",)
    m.save()

if __name__ == '__main__':
    manager.run()