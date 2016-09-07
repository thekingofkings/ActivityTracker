"""
Hongjian Wang
9/5/2016

Activity Tracker (AT) server.

The AT server is implemented in this file. The AT server communicates with the
Fitbit.com server through OAuth2.0 to retrieve and render user activity information
that are collected by Fitbit.
"""


from flask import Flask, session, url_for, redirect, request
from Oauth2 import oauthServer, authorizationHeader
import requests


app = Flask(__name__)
app.secret_key = "activitytracker"


# Go to fitbit.com to authorize user with OAuth, and get access token.
fitbit = oauthServer(app)


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
    res = fitbit.authorized_response()
    if res is None:
        return "Access denied. reason: {0}".format(request.args['errors'])
    else:
        session['fitbit_token'] = (res['access_token'])
        session['user_id'] = res['user_id']
        return "User ID: {0}. Access token: {1}".format(
                res['user_id'], res['access_token']            
            )


@fitbit.tokengetter
def get_fitbit_token(token=None):
    return session.get('fitbit_token')


@app.route("/activity/<dateStr>")
def get_user_activity(dateStr):
    """
    Get user activities.
    
    User id is stored in the session variable.
    date is a string with format 'yyyy-MM-dd'
    """
    if 'user_id' not in session:
        return redirect(url_for("login"))
    else:
        url = "https://api.fitbit.com/1/user/{0}/activities/date/{1}.json".format(session['user_id'], dateStr)
        print url
        header = {"Authorization":"Bearer {0}".format(session['fitbit_token'])}
        return requests.get(url, headers=header).content
    


if __name__ == '__main__':
    # The server is running on my local port 192.168.0.6:8080, which is behind
    # my router. Port forwarding has been setup, so that this server is accessible
    # through public IP 98.235.161.247:9292 
    app.run(host="0.0.0.0", port=8080, debug=True)