import requests
import pandas as pd
import re
url = "https://apartments-com1.p.rapidapi.com/properties"

querystring1 = {"location":"San Jose","minRent":"100","minBed":"1","maxRent":"2000","page":"1","maxBed":"3","maxBath":"3","minBath":"1","sort":"default"}

headers = {
	"X-RapidAPI-Key": "5847527b5bmshe2f2f4e69370c30p1a3ec9jsn659fda58c155",
	"X-RapidAPI-Host": "apartments-com1.p.rapidapi.com"
}

response1 = requests.get(url, headers=headers, params=querystring1)

querystring2 = {"location":"San Jose","minRent":"100","minBed":"1","maxRent":"2000","page":"2","maxBed":"3","maxBath":"3","minBath":"1","sort":"default"}
response2 = requests.get(url, headers=headers, params=querystring2)

querystring3 = {"location":"San Jose","minRent":"100","minBed":"1","maxRent":"2000","page":"3","maxBed":"3","maxBath":"3","minBath":"1","sort":"default"}
response3 = requests.get(url, headers=headers, params=querystring3)

#print(response1.json())
#print(response2.json())
#print(response3.json())

# Initialize lists to store extracted data
bedrooms = []
#city = []
price = []
address = []

# Iterate through each result in the JSON data
for result in response1.json()['data']:
    # Extract desired features from each result
    bedrooms.append(result['bedRange'])
    #city.append(result['city'])
    price.append(result['rentRange'])
    address.append(result['address'])
    
for result in response2.json()['data']:
    # Extract desired features from each result
    bedrooms.append(result['bedRange'])
    #city.append(result['city'])
    price.append(result['rentRange'])
    address.append(result['address'])
for result in response3.json()['data']:
    # Extract desired features from each result
    bedrooms.append(result['bedRange'])
    #city.append(result['city'])
    price.append(result['rentRange'])
    address.append(result['address'])

final_df = pd.DataFrame({'Bedrooms':bedrooms, 'Rental Price': price, 'address':address})
print(final_df.shape)

#it seams like the addrress has a dictionary structure 
#we are extracting long lat and zip code
def extract_info(address):
	lat = re.findall(r"'latitude':\s*([-+]?\d*\.\d+|\d+),", str(address))
	long = re.findall(r"'longitude':\s*([-+]?\d*\.\d+|\d+),", str(address))
	postal_code = re.findall(r"'postalCode':\s*'(\d+)',", str(address))
	return lat, long, postal_code
final_df['Latitude'], final_df['Longitude'], final_df['Postal Code'] = zip(*final_df['address'].apply(extract_info))
final_df.drop(columns='address',inplace=True)


print(final_df.head())
final_df.to_csv("./resultDFs/rentals.csv", index=False)