import pandas as pd 
import plotly.plotly as py
import plotly
import plotly.figure_factory as ff
import numpy as np
import json

with open('../key.json') as json_key:  
  data = json.load(json_key)
  key = data["key"]


DF = pd.read_csv("power_plants.csv")

energyList = DF['fuel1'].unique().tolist()
energyList = ['Country Code'] + ['Percent Clean'] + energyList
energyList.remove('Other')
energyList.remove(np.nan)
energyList.remove('Cogeneration')
energyList.remove('Storage')
print(energyList)

countryList = DF['country'].unique().tolist()
cleanEnergyList = ['Hydro', 'Wind', 'Nuclear', 'Solar', 'Biomass', 'Wave and Tidal', 'Geothermal']

newDF = pd.DataFrame(columns=energyList)
newDF['Country Code'] = countryList


for index,row in newDF.iterrows():
  print('Calculating...' + str(row['Country Code']))
  
  for column in newDF:
    country = DF.loc[DF['country'] == row['Country Code']] 
    energy = country.loc[country['fuel1'] == column]
    newDF.loc[row['Country Code'], column] = energy['fuel1'].count()
    # newDF.loc[row['Country Code'], column] = country.loc[country['fuel1'] == column].sum()

newDF.to_csv('stats.csv')
statsDF = pd.read_csv('stats.csv')
'''

data = [go.Choropleth(
    locations = df['CODE'],
    z = df['GDP (BILLIONS)'],
    text = df['COUNTRY'],
    colorscale = [
        [0, "rgb(5, 10, 172)"],
        [0.35, "rgb(40, 60, 190)"],
        [0.5, "rgb(70, 100, 245)"],
        [0.6, "rgb(90, 120, 245)"],
        [0.7, "rgb(106, 137, 247)"],
        [1, "rgb(220, 220, 220)"]
    ],
    autocolorscale = False,
    reversescale = True,
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(180,180,180)',
            width = 0.5
        )),
    colorbar = go.choropleth.ColorBar(
        tickprefix = '$',
        title = 'GDP<br>Billions US$'),
)]

layout = go.Layout(
    title = go.layout.Title(
        text = 'Percent Clean Energy'
    ),
    geo = go.layout.Geo(
        showframe = False,
        showcoastlines = False,
        projection = go.layout.geo.Projection(
            type = 'equirectangular'
        )
    ),
    annotations = [go.layout.Annotation(
        x = 0.55,
        y = 0.1,
        xref = 'paper',
        yref = 'paper',
        text = '',
        showarrow = False
    )]
)

fig = go.Figure(data = data, layout = layout)
py.iplot(fig, filename = 'd3-world-map')
'''