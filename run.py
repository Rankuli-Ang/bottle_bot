from bottle import run, PasteServer
from src import bot, processor, routes


if __name__ == "__main__":
    run(server=PasteServer, host='localhost', port=8080, debug=True)


