"""
Hongjian Wang
9/5/2016

Activity Tracker (AT) server.

The AT server is implemented in this file. The AT server communicates with the
Fitbit.com server through OAuth2.0 to retrieve and render user activity information
that are collected by Fitbit.
"""


from flask import Flask, session, url_for, redirect, request
from Oauth2 import oauthServer


app = Flask(__name__)
app.secret_key = "activitytracker"


# Go to fitbit.com to authorize user with OAuth, and get access token.
fitbit = oauthServer()


@app.route("/")
def index():
    if "fitbit_token" in session:
        return "Hello! Fitbit user."
    else:
        return redirect(url_for('login'))
        
        
@app.route("/login")
def login():
    print "call fitbit.com authorizer"
    return fitbit.authorize(callback="http://98.235.161.247:9292/oauth_accept")
    
    
@app.route("/oauth_accept")
def oauthAccept():
    res = request.args.get('code')
    if res is None:
        return "Fitbit response is None"
    else:
        session['twitter_token'] = (
            res        
        )
        return res
        

@fitbit.tokengetter
def get_fitbit_token(token=None):
    return session.get('fitbit_token')
    
    


if __name__ == '__main__':
    # The server is running on my local port 192.168.0.6:8080, which is behind
    # my router. Port forwarding has been setup, so that this server is accessible
    # through public IP 98.235.161.247:9292 
    app.run(host="0.0.0.0", port=8080, debug=True)