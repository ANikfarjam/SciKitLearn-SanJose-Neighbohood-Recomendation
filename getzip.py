import geopy
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from ratelimiter import RateLimiter
import ssl
import certifi
import time
# from ratelimiter import RateLimiter
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

geolocator = Nominatim(user_agent="ANik")
# geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.5)


@RateLimiter(max_calls=1, period=1)
def get_zipcodes(address):
    try:
        location = geolocator.geocode(address)
        if location:
            # Extract the latitude and longitude from the location
            lat, lon = location.latitude, location.longitude

            # time.sleep(1)
            # Reverse geocode to get the address details
            reverse_location = geolocator.reverse((lat, lon))
            
            if 'address' in reverse_location.raw:
                address_info = reverse_location.raw['address']
                
                # Extract zip code
                zip_code = address_info.get('postcode', None)
                
                return zip_code

    except GeocoderTimedOut:
        return None
    
# print(get_zipcodes('san jose'))