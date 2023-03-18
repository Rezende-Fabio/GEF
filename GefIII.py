from flask import Flask, request
from gevent.pywsgi import WSGIServer
from app import app

if __name__ == "__main__":
    app.run(host = '0.0.0.0')
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
    