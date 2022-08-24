import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

month = [
        "01-31-2022",
        "02-28-2022",
        "03-31-2022",
        "04-30-2022",
        "05-31-2022",
        "06-29-2022",
        "07-27-2022"]
    


urban_x=[]
urban_y=[]
rural_x=[]
rural_y=[]

for i in month:  
  df = pd.read_csv('data/county-and-land-'+i+'.csv')
  df["death_per"]=df["Deaths"]/df["Population"]*100000
  df2=df[df["Population Density"]>500]
  urban_pop = df2[["Population Density","death_per"]].mean()
  urban_vacc = df2[["Series_Complete_18PlusPop_Pct","death_per"]].mean()
  df3=df[df["Population Density"]<=500]
  rural_pop = df3[["Population Density","death_per"]].mean()
  rural_vacc=df3[["Series_Complete_18PlusPop_Pct","death_per"]].mean()
  urban_x.append(urban_vacc[0])
  urban_y.append(urban_vacc[1])
  rural_x.append(rural_vacc[0])
  rural_y.append(rural_vacc[1])
  
  
  
fig = plt.figure(figsize = (10, 5)) 
X_axis = np.arange(len(month))
  
plt.bar(X_axis - 0.2, urban_y, 0.4, label = 'Urban')
plt.bar(X_axis + 0.2, rural_y, 0.4, label = 'Rural')


plt.xticks(X_axis, month)
plt.xlabel("Date")
plt.ylabel("Average number of Deaths per 100K")
plt.title("Average Deaths number in each month")
plt.legend()
plt.savefig('img/'+'Average Deaths number in each month.png')
plt.show()



fig = plt.figure(figsize = (10, 5))
X_axis = np.arange(len(month))  
plt.bar(X_axis - 0.2, urban_x, 0.4, label = 'Urban')
plt.bar(X_axis + 0.2, rural_x, 0.4, label = 'Rural')

plt.xticks(X_axis, month)
plt.xlabel("Date")
plt.ylabel("Average fully vaccinated rate")
plt.title("Average fully vaccinated rate")
plt.legend()
plt.savefig('img/'+'Average fully vaccinated rate.png')
plt.show()
