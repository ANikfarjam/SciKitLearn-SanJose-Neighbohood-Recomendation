#Author: Ashkan Nikfarjam
import pandas as pd
import plotly.express as px
# sjsu zip code is 95192
#some srounding neighborhoods are  95112 North,  95126 Dridon station, and 95113

#Plan is to create a list and get the transportaion that goeas this way
sjsu_zips =[95112, 95126, 95113]
sj_trp = pd.read_csv('tsp.csv')
print('before',sj_trp.shape)
#available transportation
avT = sj_trp[sj_trp['Zip'].isin(sjsu_zips)]
print(avT.head())
print('after',avT.shape)

fig = px.scatter_mapbox(avT, 
                    lat='Lat',
                    lon='Long',
                    #size= size_column,
                    color= 'rbs_routesserved',
                    mapbox_style="carto-positron",
                    center={"lat": avT['Lat'].mean(), "lon": avT['Long'].mean()},
                    zoom=5,
                    #color_continuous_scale="YlOrRd",  # Yellow to Red color scale
                    height=1000
                    )

#fig.show()

result = avT.Zip.value_counts().reset_index()
print(result.head())
result.to_csv("./resultDFs/tsp.csv", index= False)