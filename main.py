import flask
import requests
from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.client import UberRidesClient
from json import load


app = flask.Flask(__name__)

CLIENT_ID = "bc4lGGyYwVBxYFgu0E46mplUVpcx-rgt"
PERMISSION_SCOPES = ["profile"]
CLIENT_SECRET = "V2KfgezEsm24-wcqzfvvJnEpcdCNfTVYyIpH4FTx"
REDIRECT_URL = "http://localhost:5000/landing_screen"

auth_flow = AuthorizationCodeGrant(
        CLIENT_ID,
        PERMISSION_SCOPES,
        CLIENT_SECRET,
        REDIRECT_URL,
    )

@app.route("/")
def hello():
    
    auth_url = auth_flow.get_authorization_url()
    return flask.redirect(auth_url)

@app.route("/landing_screen")
def display_token():
    session = auth_flow.get_session(flask.request.url)
    client = UberRidesClient(session)
    credentials = session.oauth2credential
    #client.get_products()
    return getGeoLocation() 

def getGeoLocation():
    return requests.get('https://api.ipify.org/?format=json').json()["ip"]

if __name__ == "__main__":
    app.run()
