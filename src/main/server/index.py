from main.server.bootstrap.boot import boot
from main.server.app.application import application


def init():
    boot()
    return application()


app = init()
