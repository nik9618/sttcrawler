import SimpleHTTPServer
import SocketServer

class HTTPServ():

	def __init__(self):
		PORT = 8000
		Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
		httpd = SocketServer.TCPServer(("", PORT), Handler)
		print "serving at port", PORT
		httpd.serve_forever()

