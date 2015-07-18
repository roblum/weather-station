from flask import Flask
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

@sockets.route('/weather_station')
def weather_station(ws):
	while True:
		message = ws.receive()

		if not message is None:
			ws.send(message)
		else:
			return