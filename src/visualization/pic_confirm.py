# -*- coding: utf-8 -*-

import plotly
import numpy as np
import pandas as pd
import plotly.figure_factory as ff







df_sample = pd.read_csv('data/county-and-land-06-29-2022.csv') # Read in your data


#plot 2022-6-30 US county Covied comfirmed Percentage ‱
values = (df_sample['Confirmed']/df_sample['Population']*100).tolist() # Read in the values contained within your file
fips = df_sample['FIPS'].tolist() # Read in FIPS Codes


colorscale  =["#a50026","#d32c27","#ef633d","#fdce7c",
          "#9bcde2","#4070b2","#313695"]

endpts = list(np.linspace(0, 15, len(colorscale) - 1)) # Identify a suitable range for your data

fig = ff.create_choropleth(
   fips=fips, values=values, colorscale=colorscale, show_state_data=True, binning_endpoints=endpts, # If your values is a list of numbers, you can bin your values into half-open intervals
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, 
    legend_title='confirmed Percentage ‱', title='2022-6-30 US county Covied comfirmed Percentage ‱'
)
fig.write_image('img/'+'2022-6-29 US county confirmed Percentage ‱.png')
fig.show()
