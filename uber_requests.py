__author__ = 'jeshall'

import requests
import traceback
from uber_rides.utils.request import build_url

class UberRequest:

    def __init__(self,
                 api_host,
                 session,
                 method,
                 path,
                 requests_module = requests,
                 args=None):
        self.requests = requests_module
        self.api_host = api_host
        self.session = session
        self.method = method
        self.path = path
        self.args = args
        self.response=None
        self._build_auth_header()

    def _build_auth_header(self, session=None):

        if not session:
            session = self.session

        token_type = self.session.token_type

        if session.server_token:
            token = session.server_token
        else:
            token = session.oauth2credential.access_token
        self.headers = {'Authorization': ' '.join([token_type, token])}

    def make_request(self):
        try:
            url = build_url(self.api_host, self.path)
            self.response = requests.request(self.method, url, headers=self.headers, params=self.args)
        except:
            print traceback.format_exc()

    @classmethod
    def price_estimates(cls, api_host, session, start_latitude, start_longitude, end_latitutde, end_longitude):
        args = {"start_latitude": start_latitude,
        "start_longitude": start_longitude,
        "end_latitude": end_latitutde,
        "end_longitude": end_longitude}
        return cls(api_host, session, 'get', 'v1/estimates/price', args=args)