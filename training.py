import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

#importing all datas
#Crimes Represent Safety
crime_df =pd.read_csv('./resultDFs/crimes.csv')
#to make our data homogenious we need to group the df by zip code
crime_df_final = crime_df.groupby(by='zipcode').PRIORITY.mean().reset_index()
crime_df_final = crime_df_final[crime_df_final['zipcode'].apply(lambda x: len(x) == 5)]
crime_df_final.rename(columns={'zipcode':'zip','PRIORITY':'Average Crime'}, inplace=True)
print(crime_df_final.head())

#health care facilities df
health_df = pd.read_csv('resultDFs/HealthCare.csv')
health_df = health_df.drop(columns=['CAPACITY'])
health_df.rename(columns={'ZIP':'zip'},inplace=True)
print(health_df.head())

#rentals
def rentals_prefrences(numberofBeds):
    rental = pd.read_csv('./resultDFs/rentalsSJVisualization.csv')
    rental = rental[rental['Bedrooms'] == numberofBeds]
    rental = rental.groupby(by='Postal Code')['Rental Price'].min().reset_index()
    return rental

student_rental = rentals_prefrences(1)
student_rental.rename(columns={'Postal Code':'zip'},inplace=True)
print(student_rental.head())

master_df = pd.read_csv('zipsdf.csv')
master_df = master_df[['zip']]
master_df['zip'] = master_df['zip'].astype(int)
print(master_df.head())
master_df = pd.concat([master_df, crime_df_final], axis=1, join='inner')
master_df = pd.concat([master_df, health_df], axis=1, join='inner')
master_df = pd.concat([master_df, student_rental], axis=1, join='inner')
master_df = master_df.iloc[:, [0, 2, 4, 6]]
print(master_df.head())
#set up traning data sets
X = master_df.copy()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Perform KMeans clustering
kmeans = KMeans(n_clusters=5, random_state=42)
kmeans.fit(X_scaled)
cluster_labels = kmeans.labels_

# Add cluster labels to the DataFrame
master_df['Cluster'] = cluster_labels

zip_df = pd.read_csv('zipdic.csv')
master_df = pd.concat([master_df, zip_df], axis=1, join='inner') 
print(master_df.head())
#fig = px.scatter(master_df, x="Number of Healthcare Facilities", y="Rental Price", color="Cluster", hover_data=["zip", "Average Crime"])
#fig.update_traces(marker=dict(size=12))  # Set the size of each marker
#fig.update_layout(title="Scatter Plot of Rental Price vs Number of Healthcare Facilities",
#                  xaxis_title="Number of Healthcare Facilities",
#                  yaxis_title="Rental Price")
#fig.show()
fig = go.Figure(data=[go.Scatter3d(
    x=master_df['Number of Healthcare Facilities'],
    y=master_df['Rental Price'],
    z=master_df['Average Crime'],
    mode='markers',
    marker=dict(
        size=12,
        color=master_df['Cluster'],  # Color by cluster
        colorscale='Viridis',  # Choose colorscale
        opacity=0.8
    ),
    text=master_df['Neighborhood Name'],  # Text to be displayed upon hovering
)])
# Update axis labels
fig.update_layout(
    scene=dict(
        xaxis=dict(title='Number of Healthcare Facilities'),
        yaxis=dict(title='Rental Price'),
        zaxis=dict(title='Average Crime')
    )
)
fig.show()
pio.write_image(fig, 'SJClassified.png')