#bottle_bot

Training project for studying Python web development with WSGI framework Bottle.

In this program, it starts the server, creates a bot, to which the client can transmit coordinates for movement. 

How to run:
  -download all files
  -run main.py

To GET coordinates of the bot:
  -curl http://localhost:8080/coordinates

To POST new coordinates for bot move:
  -curl -X POST http://localhost:8080/coordinates/10/15
  -use Postman or another API
