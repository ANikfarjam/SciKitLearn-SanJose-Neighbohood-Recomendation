import geopy
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from ratelimiter import RateLimiter
import ssl
import certifi
import pandas as pd
from tqdm import tqdm

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

transportation_df = pd.read_csv('vtageo.csv')

geolocator = Nominatim(user_agent="ANik")

@RateLimiter(max_calls=1, period=1)
def get_zip(lat, long):
    try:
        location = geolocator.reverse((lat, long), exactly_one=True)
        address = location.raw['address']
        # Look for zip code in the address
        if 'postcode' in address:
            return address['postcode']
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

zip_lst = []
if __name__=="__main__":
    for i in tqdm(range(len(transportation_df))):
        lat = transportation_df.loc[i, 'Lat']
        long = transportation_df.loc[i, 'Long']
        zip_code = get_zip(lat, long)
        zip_lst.append(zip_code)
transportation_df['Zip'] = zip_lst
print(transportation_df.head())
transportation_df.to_csv('tsp.csv', index=False)