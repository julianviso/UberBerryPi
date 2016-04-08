import flask
import requests
import traceback
from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.client import UberRidesClient

from uber_requests import UberRequest


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

@app.route("/get_access_token")
def get_access_token():
    return SESSION.oauth2credential.access_token

@app.route("/get_products")
def get_products():
    if not isClientValid():
        return "Please create an uber session and client at http://localhost:5000\n"
    print "Requesting products from Uber"
    response = CLIENT.get_products(MY_LATITUDE, MY_LONGITUDE)
    print "products recieved"
    print str(CLIENT)+ "\n"

    return str(response.json)

#Bugged Call to SDK /v1/estimates/price

@app.route("/Xget_priceX")
def get_price_estimates():
    if not isClientValid():
        return "Please create an uber session and client at http://localhost:5000\n"
    print "Requesting price estimates from Uber"
    try:
        response = CLIENT.get_price_estimates(MY_LATITUDE, MY_LONGITUDE, DEST_LATITUDE, DEST_LONGITUDE)
    except Exception as e:
        print traceback.format_exc()
    print "Price estimates recieved"
    return str(response.json)

@app.route("/custom_price")
def get_custom_price_estimates():
    headers = {'Authorization': 'Bearer {0}'.format(SESSION.oauth2credential.access_token)}
    params = {"start_latitude": MY_LATITUDE,
    "start_longitude": MY_LONGITUDE,
    "end_latitude": DEST_LATITUDE,
    "end_longitude": DEST_LATITUDE}
    try:
        r = requests.get("https://{0}/v1/estimates/price".format(CLIENT.api_host), params=params,  headers=headers)
    except Exception as e:
        print traceback.format_exc()
    return r.text

@app.route("/get_price")
def get_price():
    price_estimates_request = UberRequest.price_estimates(CLIENT.api_host, SESSION, MY_LATITUDE, MY_LONGITUDE, DEST_LATITUDE, DEST_LONGITUDE)
    price_estimates_request.make_request()
    return price_estimates_request.response.text


def getGeoLocation():
    return requests.get('https://api.ipify.org/?format=json').json()["ip"]

if __name__ == "__main__":
    app.run()
