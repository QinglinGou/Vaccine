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
fig.show()


df_sample = pd.read_csv('data/county-and-land-06-29-2022.csv') # Read in your data


# plot 2022-6-29 US county deaths-confirmed rate
values=(df_sample["Deaths"]/df_sample["Confirmed"]*1000).tolist() # Read in the values contained within your file
fips = df_sample['FIPS'].tolist() # Read in FIPS Codes

colorscale = ["#313695","#4070b2","#9bcde2","#fdce7c",
              "#ef633d","#d32c27","#a50026"]

endpts = list(np.linspace(0, 30, len(colorscale) - 1)) # Identify a suitable range for your data

fig = ff.create_choropleth(
   fips=fips, values=values, colorscale=colorscale, show_state_data=True, binning_endpoints=endpts, # If your values is a list of numbers, you can bin your values into half-open intervals
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, 
    legend_title='deaths-confirmed rate %', title='2022-6-29 US county deaths-confirmed rate '
)
fig.show()

# plot 2022-6-30 US county Covied deaths Percentage ‱
values = (df_sample['Deaths']/df_sample['Population']*10000).tolist() # Read in the values contained within your file
fips = df_sample['FIPS'].tolist() # Read in FIPS Codes


colorscale = ["#a50026","#d32c27","#ef633d","#fdce7c",
          "#9bcde2","#4070b2","#313695"]

endpts = list(np.linspace(0, 20, len(colorscale) - 1)) # Identify a suitable range for your data

fig = ff.create_choropleth(
   fips=fips, values=values, colorscale=colorscale, show_state_data=True, binning_endpoints=endpts, # If your values is a list of numbers, you can bin your values into half-open intervals
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, 
    legend_title='Deaths Percentage ‱', title='2022-6-30 US county Covied deaths Percentage ‱'
)
fig.show()


#plot 2022-6-29 US county fully vacciened rate
values = df_sample['Series_Complete_18PlusPop_Pct'].tolist() # Read in the values contained within your file
fips = df_sample['FIPS'].tolist() # Read in FIPS Codes

colorscale = ["#313695","#4070b2","#9bcde2","#fdce7c",
              "#ef633d","#d32c27","#a50026"]

endpts = list(np.linspace(40, 100, len(colorscale) - 1)) # Identify a suitable range for your data

fig = ff.create_choropleth(
   fips=fips, values=values, colorscale=colorscale, show_state_data=True, binning_endpoints=endpts, # If your values is a list of numbers, you can bin your values into half-open intervals
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, 
    legend_title='fully vacciened rate %', title='2022-6-29 US county fully vacciened rate '
)
fig.show()

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
fig.show()
