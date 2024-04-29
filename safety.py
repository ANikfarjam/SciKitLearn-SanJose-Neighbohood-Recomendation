#Author Ashkan Nikfarjam
import pandas as pd
crime_rate = pd.read_csv('crime_rates.csv')
#the data frame is the record of police calls in san jose in 2024
#all the calls have been rated based on priority Higher Number represent higher priority
copy_df = crime_rate[['PRIORITY' ,'zipcode']]
result_df = copy_df.value_counts().reset_index()
print(result_df.head())
result_df.to_csv('./resultDFs/crimes.csv')