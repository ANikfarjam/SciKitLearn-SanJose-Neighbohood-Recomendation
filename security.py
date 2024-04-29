import pandas as pd
from getzip import get_zipcodes
from tqdm import tqdm
#import vaex

# Read the CSV file into a pandas DataFrame
crime_df_2024 = pd.read_csv('policecalls2024.csv')
#adjust adresses
def get_strt(street):
    if type(street)==float:
        return None
    new_strt_lst = str(street).split()
    if len(new_strt_lst) > 2 and (new_strt_lst[-3] == '&' or len(new_strt_lst[-3].split('-')) == 2):
        add = ' '.join(new_strt_lst[-2:])
    else: 
        add  = ' '.join(new_strt_lst[-3:])
    return add
crime_df_2024 = crime_df_2024.dropna()
crime_df_2024['ADDRESS'] = crime_df_2024['ADDRESS'].astype(str).apply(get_strt)
#print(crime_df_2024.head())
# Define a function to process addresses and get zip codes
#def process_address(address):
    #address_parts = [address, 'San Jose', 'CA']
    # Join the address parts with a space
    #full_address = ' '.join(address_parts)    
#    current_zip = get_zipcodes(address)
#    return current_zip 

# Apply the process_address function to each row to extract zip codes
#crime_df_2024['zips'] = crime_df_2024.ADDRESS.apply(get_zipcodes)
#since there are more than 300k data it takes 8 days to do this task so im just going to run this on hal of it
copy_df = crime_df_2024.copy()
copy_df = copy_df.iloc[:int(len(copy_df)/20),:]
crime_lst = copy_df.ADDRESS.to_list()
zips = []
with open("extractedZips.txt",'w') as file:
    for i in tqdm(range(len(crime_lst))):
        zipCode = get_zipcodes(crime_lst[i])
        zips.append(zipCode)
        file.write(str(zipCode))
#add_col = crime_df_2024.ADDRESS.to_list()
# Print the head of the DataFrame
copy_df['zipcode'] = zips
print(copy_df.head())
copy_df.to_csv('crime_rates.csv', index=False)