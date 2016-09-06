"""
Hongjian Wang
9/5/2016

Activity Tracker (AT) server.

The AT server is implemented in this file. The AT server communicates with the
Fitbit.com server through OAuth2.0 to retrieve and render user activity information
that are collected by Fitbit.
"""


from flask import Flask
print __name__
app = Flask(__name__)


@app.route("/")
def index():
    return "Hello! This is ActivityTracker server."
    

if __name__ == '__main__':
    # The server is running on my local port 192.168.0.6:8080, which is behind
    # my router. Port forwarding has been setup, so that this server is accessible
    # through public IP 98.235.161.247:9292 
    app.run(host="0.0.0.0", port=8080)