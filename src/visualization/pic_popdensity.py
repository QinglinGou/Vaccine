# -*- coding: utf-8 -*-

import plotly
import numpy as np
import pandas as pd
import plotly.figure_factory as ff

# plot the population density in US by county
df_sample = pd.read_csv("data/Land.csv")# Read in your data
values = df_sample['Population Density'].tolist() # Read in the values contained within your file
fips = df_sample['FIPS'].tolist() # Read in FIPS Codes

colorscale = ["#313695","#4070b2","#9bcde2","#fdce7c",
              "#ef633d","#d32c27","#a50026"]
endp= [1.0,20,90,500,2000]
endp=list(endp)
endpts= endp
fig = ff.create_choropleth(
   fips=fips, values=values, colorscale=colorscale, show_state_data=True, binning_endpoints=endpts, # If your values is a list of numbers, you can bin your values into half-open intervals
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, 
    legend_title='Population Density', title='2020 US county Population Density (people per squre mile)'
)
fig.write_image('img/'+'2020 US county Population Density (people per squre mile).png')
fig.show()




