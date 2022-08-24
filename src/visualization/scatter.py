# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import imageio.v2 as iio
import os
import sys


def scatter(month):
  cou = pd.read_csv('data/county-and-land-'+month+'.csv', converters={'FIPS' : str})
  cou["Classification"]=pd.cut(cou["Population Density"],[0,500,100000],labels=["Rural","Urban"])
  cou["Deaths_Per_1e5"]=(cou['Deaths']/cou['Population']*100000)
  xlabel = 'Series_Complete_18PlusPop_Pct'
  ylabel = 'Deaths_Per_1e5'
  x = cou[xlabel]
  y = cou[ylabel]
  fig, ax = plt.subplots()
  ax.set_xlabel("Percent of Population (+18) Considered Fully Vaccinated")
  ax.set_ylabel("Deaths per 100K")
  ax.set_xlim(0,100)
  ax.set_ylim(0,400) #[KR] changed from 500 limit to 400 limit
  ax.set_title("Vaccine Effectiveness Snapshot as of: ")
  fig.set_size_inches(8,6)
  ax.spines['top'].set_visible(False) #[MR] Removes top spine
  ax.spines['right'].set_visible(False) #[MR] Removes right spine
  ax.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.6) #[MR] Adds gridlines
  area = cou['Census2019_18PlusPop']/1e6 



  m, b = np.polyfit(x, y, 1)
  plt.plot(x, m*x + b, alpha=0.8, c='dimgray')
  plot_scl = 100
  colors={"Urban":"red","Rural":"green"}
  regions={"Urban":"red","Rural":"green"}

  scatter = ax.scatter(x, y, s=area*plot_scl, alpha=0.5,c=cou['Classification'].map(colors), edgecolor='white')
  markers = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='') for color in regions.values()]
  leg = plt.legend(markers, regions.keys(), numpoints=1, loc=(1.05,0), title="Region")
  ax.add_artist(leg)

  for area_scl in [0.5, 2, 4]:
    ax.scatter([], [], s = plot_scl*area_scl, c = "gray", alpha = 0.5, label = str(area_scl) + 'M')
  ax.legend(loc = (1.05, 0.3), title="Population (Millions)", labelspacing = 1.5, borderpad = 1)
  plt.tight_layout()
  plt.savefig('img/'+month+'.png')
def create_scatters():
    """This function creates seven scatter plots based on the merged data.
    """
    dates = [
        "01-31-2022",
        "02-28-2022",
        "03-31-2022",
        "04-30-2022",
        "05-31-2022",
        "06-29-2022",
        "07-27-2022"
    ]
    for date in dates:
        # print(date)
        scatter(date)

if __name__ == "__main__":
    create_scatters()





def create_gif(filename_save):
    """This function creates a gif animation from a folder of png images
    Parameters:
        filename_save: str, the filename to save the gif as
    """
    #makes a list of im NumPy arrays based on a list of .png images (read from folder)
    images = list()

    #this part looks at the img directory and reads in all the files that end with .png (only going to bring in those)
    for filename in sorted(os.listdir('img')):
        if filename[-4:] == '.png' and not filename == 'comparison.png':
            f = os.path.join('img',filename)
            im = iio.imread(f)
            images.append(im)

    #making the gif from the pngs
    iio.mimsave(filename_save,images,duration = 1)

if __name__ == "__main__":
    create_gif('animation.gif')



















