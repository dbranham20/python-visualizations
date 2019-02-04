import pandas as pd 
import plotly.plotly as py
import plotly
import plotly.figure_factory as ff
import numpy as np
from collections import Counter
plotly.tools.set_credentials_file(username='USERNAME', api_key='KEY')

# Colors for map
scl = [[0.0, 'rgb(41, 46, 73)'],[0.2, 'rgb(70, 78, 97)'],[0.4, 'rgb(99, 111, 122)'],\
            [0.6, 'rgb(128, 144, 147)'],[0.8, 'rgb(157, 177, 172)'],[1.0, 'rgb(187, 210, 197)']]

def prepareDF(states, stateAVG, stateNum):
	totalsDF = pd.DataFrame(states.flatten())
	totalsDF.columns = ['State']
	totalsDF['AVG'] = 0
	totalsDF['numSAT'] = 0
	totalsDF['text'] = ""

	for index, row in totalsDF.iterrows():
		totalsDF.at[index, 'AVG'] = stateAVG[row['State']]
		totalsDF.at[index, 'numSAT'] = stateNum[str(row['State'])]
		totalsDF.at[index, 'text'] = "Averages Reported: " + str(stateNum[str(row['State'])])

	return totalsDF

def produceMap(totalsDF):
	data = [ dict(
			type='choropleth',
			colorscale = scl,
			autocolorscale = False,
			locations = totalsDF['State'],
			z = totalsDF['AVG'],
			locationmode = 'USA-states',
			text = totalsDF['text'],
			marker = dict(
				line = dict (
					color = 'rgb(255,255,255)',
					width = 2
				) ),
			colorbar = dict(
				title = "SAT Score")
			) ]

	layout = dict(
			title = 'Average SAT Scores by State, 2000-2016',
			geo = dict(
				scope='usa',
				projection=dict( type='albers usa' ),
				showlakes = True,
				lakecolor = 'rgb(255, 255, 255)'),
				)
		
	fig = dict( data=data, layout=layout )
	py.plot( fig, filename='d3-cloropleth-map' )


for year in range(2001,2017):
	# print("Starting large file for " + str(year) + "...")
	# DF = pd.read_csv(str(year)+ ".csv", low_memory=False)
	# DF= DF.astype(str)
	# replaceDF = DF.replace({'nan' : None})
	# replaceDF.dropna(axis=1, how="all", inplace=True)
	# replaceDF.to_csv("new" + str(year) + ".csv")

	specificDF = pd.DataFrame(columns=['State','SAT','Total','Num','AVG'])

	print("Starting small file for " + str(year) + "...")
	DF = pd.read_csv("new" + str(year) + ".csv", low_memory=False)

	specificDF['SAT'] = DF['SAT_AVG']
	specificDF['State'] = DF['STABBR']
	specificDF.dropna(axis=0, how="any", subset=['SAT'], inplace=True)


	if(year == 2001):
		print("Initializing dictionaries...")
		
		#get list of states
		states = specificDF['State'].unique()

		# set each states scores to 0
		stateTotal = dict((el,0) for el in states)
		stateNum = dict((el,0) for el in states)
		stateAVG = dict((el,0) for el in states)

	for index, row in specificDF.iterrows():
		stateTotal[row['State']] += float(row['SAT'])
		stateNum[row['State']] += 1
	
print("Math...")
stateAVG={x:int(stateTotal[x])/stateNum[x] for x in stateTotal}


DF = prepareDF(states, stateAVG, stateNum)

DF =DF.drop([51,52])
produceMap(DF)