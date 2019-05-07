import pandas as pd 
import plotly.plotly as py
import plotly
import plotly.figure_factory as ff
import numpy as np
import json


with open('../key.json') as json_key:  
  data = json.load(json_key)
  key = data["key"]

print(key)