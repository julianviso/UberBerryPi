import flask
import requests
import traceback
from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.client import UberRidesClient


app = flask.Flask(__name__)

SESSION = None
CLIENT = None

CLIENT_ID = "bc4lGGyYwVBxYFgu0E46mplUVpcx-rgt"
PERMISSION_SCOPES = ["profile"]
CLIENT_SECRET = "V2KfgezEsm24-wcqzfvvJnEpcdCNfTVYyIpH4FTx"
REDIRECT_URL = "http://localhost:5000/landing_screen"

MY_LATITUDE = "33.437435"
MY_LONGITUDE = "-84.587303"

DEST_LATITUDE = "38.071423"
DEST_LONGITUDE = "-84.496689"

auth_flow = AuthorizationCodeGrant(
        CLIENT_ID,
        PERMISSION_SCOPES,
        CLIENT_SECRET,
        REDIRECT_URL,
    )

def isClientValid():
    if CLIENT is None:
        return False
    else:
        return True

def isSessionValid():
    if SESSION is None:
        return False
    else:
        return True

@app.route("/")
def root():
    auth_url = auth_flow.get_authorization_url()
    return flask.redirect(auth_url)

@app.route("/landing_screen")
def store_session_client():
    global SESSION
    global CLIENT
    SESSION = auth_flow.get_session(flask.request.url)
    CLIENT = UberRidesClient(SESSION)
    return "Client and Session created"

@app.route("/get_session_valid")
def get_session_valid():
    if isSessionValid():
        return "True"
    else:
        return "False"

@app.route("/get_client_valid")
def get_client_valid():
    if isClientValid():
        return "True"
    else:
        return "False"

@app.route("/get_products")
def get_products():
    if not isClientValid():
        return "Please create an uber session and client at http://localhost:5000\n"
    print "Requesting products from Uber"
    response = CLIENT.get_products(MY_LATITUDE, MY_LONGITUDE)
    print "products recieved"
    return str(response.json)

@app.route("/get_price")
def get_price_estimates():
    if not isClientValid():
        return "Please create an uber session and client at http://localhost:5000\n"
    print "Requesting price estimates from Uber"
    try:
        response = CLIENT.get_price_estimates(MY_LATITUDE, MY_LONGITUDE, DEST_LONGITUDE, DEST_LATITUDE)
    except Exception as e:
        traceback.print_exception(e)
    print "Price estimates recieved"
    return str(response.json)



def getGeoLocation():
    return requests.get('https://api.ipify.org/?format=json').json()["ip"]

if __name__ == "__main__":
    app.run()
