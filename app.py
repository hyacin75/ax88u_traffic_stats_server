from flask import Flask, render_template_string
from flask_restful import Resource, Api
from os import path
from pathlib import Path
import socket

def uptime():
	try:
		f = open( "/proc/uptime" )
		contents = f.read().split()
		f.close()
	except:
		return "Cannot open uptime file: /proc/uptime"
 
	total_seconds = float(contents[0])
 
	# Helper vars:
	MINUTE  = 60
	HOUR    = MINUTE * 60
	DAY     = HOUR * 24
 
	# Get the days, hours, etc:
	days    = int( total_seconds / DAY )
	hours   = int( ( total_seconds % DAY ) / HOUR )
	minutes = int( ( total_seconds % HOUR ) / MINUTE )
	seconds = int( total_seconds % MINUTE )
 
	# Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
	string = ""
	if days > 0:
		string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
	if len(string) > 0 or hours > 0:
		string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
	if len(string) > 0 or minutes > 0:
		string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
	string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
 
	return string

app = Flask(__name__)
api = Api(app)

class getstats(Resource):
	def get(self, interface):
		headers = {'Content-Type': 'text/html'}
		if not path.exists("/sys/class/net/" + interface):
			page = "<HTML><BODY>ERROR: NO SUCH INTERFACE</BODY></HTML>"
		else:
			inbytes = Path("/sys/class/net/" + interface + "/statistics/rx_bytes").read_text()
			outbytes = Path("/sys/class/net/" + interface + "/statistics/tx_bytes").read_text()
			page = "<HTML><BODY>%s<BR>%s<BR>%s<BR>%s</BODY></HTML>" % (inbytes.rstrip(), outbytes.rstrip(), uptime(), socket.gethostname())
		return render_template_string(page)

api.add_resource(getstats, '/<string:interface>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
