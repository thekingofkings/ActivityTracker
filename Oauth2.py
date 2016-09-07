"""
Hongjian
9/5/2016

Oauth authentication of AT server.

Use the online registered Oauth2 client ID and secret to authenticate AT server
with the Fitbit Oauth server.
"""

import unittest
from flask_oauthlib.client import OAuth
from base64 import b64encode


def getOauthCredentials():
    """
    Get Oauth credentials from local config file
    """
    credentials = {}
    
    with open("oauth-credentials", "r") as fin:
        credentials['clientId'] = fin.readline().strip()
        credentials['clientSecret'] = fin.readline().strip()
    
    return credentials


def oauthServer(app=None):
    credentials = getOauthCredentials()
    
    oauth = OAuth(app)
    Fitbit = oauth.remote_app(
        name='fitbit',
        consumer_key=credentials['clientId'],
        consumer_secret=credentials['clientSecret'],
        access_token_method='POST',
        access_token_url='https://api.fitbit.com/oauth2/token',
        request_token_params={'scope':'activity heartrate',
                              'expires_in': 2592000},
        access_token_params={'client_id':credentials['clientId']},
        access_token_headers={'Authorization':'Basic '+
            b64encode("{0}:{1}".format(credentials['clientId'], credentials['clientSecret']))},
        authorize_url='https://www.fitbit.com/oauth2/authorize'
        )
    return Fitbit




class Oauth2Test(unittest.TestCase):

    def test_getOauthCredentials(self):
        res = getOauthCredentials()
        assert len(res['clientId']) > 3
        assert len(res['clientSecret']) > 10
        
        
    def test_oauthServer(self):
        Fitbit = oauthServer()
        assert Fitbit.name == 'fitbit'
        
        

if __name__ == '__main__':
    unittest.main()