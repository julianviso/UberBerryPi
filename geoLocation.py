from geoip import open_database
from geoip import geolite2
from geopy.geocoders import Nominatim

#geoip version - not accurate enough
match = geolite2.lookup('192.146.101.24')
print match.location

#geopy version
geolocator = Nominatim()
location = geolocator.geocode("221 Barberry Lane Lexington Kentucky")
print location.address
print((location.latitude, location.longitude))
