from bottle import run, PasteServer
from src import processor, routes, bot


if __name__ == "__main__":
    run(server=PasteServer, host='localhost', port=8080, debug=True)
