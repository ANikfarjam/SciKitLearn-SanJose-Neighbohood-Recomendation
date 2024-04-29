#author: Ashkan Nikfarjam
#source: US Hospitals API
#an api for california medical facilities directory

#import requests
import pandas as pd

hospitals_df = pd.read_csv('health_facility_locations.csv')
#print(hospitals_df.head())
sj_df = hospitals_df[hospitals_df['CITY']=='SAN JOSE']
sj_df = sj_df[['FACNAME', 'CAPACITY', 'ZIP']]
copy_df = sj_df.copy()
num_df = copy_df.ZIP.value_counts().reset_index()
cap_df = copy_df.groupby(by='ZIP').CAPACITY.sum().reset_index()
merged_df = pd.merge(num_df, cap_df, on='ZIP')
print(num_df.shape)
print(cap_df.shape)
merged_df.rename(columns={'count':'Number of Healthcare Facilities'}, inplace=True)
print(merged_df.head())
merged_df.to_csv('./resultDFs/HealthCare.csv', index=False)