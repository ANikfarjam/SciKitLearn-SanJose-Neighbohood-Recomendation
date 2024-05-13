import pandas as pd
import plotly.express as px

# Read data
df = pd.read_csv('helthMap.csv')

# Plot map
fig2 = px.scatter_mapbox(df, 
                        lat='LATITUDE',
                        lon='LONGITUDE',
                        color='CAPACITY',
                        mapbox_style="carto-positron",
                        center={"lat": df['LATITUDE'].mean(), "lon": df['LONGITUDE'].mean()},
                        zoom=20, 
                        size_max =15,
                        height=1000
                        )
# Show plot
fig2.show()
