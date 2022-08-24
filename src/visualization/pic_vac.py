# -*- coding: utf-8 -*-

import plotly
import numpy as np
import pandas as pd
import plotly.figure_factory as ff






df_sample = pd.read_csv('data/county-and-land-06-29-2022.csv') # Read in your data




#plot 2022-6-29 US county fully vacciened rate
values = df_sample['Series_Complete_18PlusPop_Pct'].tolist() # Read in the values contained within your file
fips = df_sample['FIPS'].tolist() # Read in FIPS Codes

colorscale = ["#313695","#4070b2","#9bcde2","#fdce7c",
              "#ef633d","#d32c27","#a50026"]

endpts = list(np.linspace(40, 100, len(colorscale) - 1)) # Identify a suitable range for your data

fig = ff.create_choropleth(
   fips=fips, values=values, colorscale=colorscale, show_state_data=True, binning_endpoints=endpts, # If your values is a list of numbers, you can bin your values into half-open intervals
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, 
    legend_title='fully vaccinated rate %', title='2022-6-29 US county fully vaccinated rate '
)
fig.write_image('img/'+'2022-6-29 US county fully vaccinated rate.png')
fig.show()


