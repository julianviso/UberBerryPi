from geopy.geocoders import Nominatim
from geopy import *

geolocator = Nominatim()
location = geolocator.geocode("Lexmark, Lexington, KY")
if location:
	print location.address
	print((location.latitude, location.longitude))
else:
	print "Not able to get address, try again"
