# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import imageio.v2 as iio
import os

url="https://api.census.gov/data/2020/dec/pl?get=NAME,P1_001N&for=county"
county=pd.read_json(url)
county = pd.DataFrame(county)
County=county
county.columns=["1","2","3","4"]
county["5"]=county["3"]+county["4"]
county=county.drop(columns=["3","4"])
county.columns=["County","Population","FIPS"]

county = county.drop([0])
county["Population"]=county["Population"].apply(int)

county=county[["FIPS","Population"]].dropna()


land = pd.read_csv('data/LND01.csv')
land = land[["STCOU","LND110210D"]]
land.columns=["FIPS","Land_area"]


county=county.astype(int)
county_land=pd.merge(county,land,on=["FIPS"])
county_land["Population Density"]=county_land["Population"]/county_land["Land_area"]
county_land

def readit(filename):
    """This is a function that reads in a csv from a URL and returns a dataframe. It 
    removes any entries for which the FIPS code is entry.
    Parameters:
        filename: str
    Returns:
        pandas dataframe
    """
    # Read CSV while keeping FIPS as a string
    # Base URL for JHU data repo
    base = "https://raw.githubusercontent.com/"
    base += "CSSEGISandData/COVID-19/master/csse_covid_19_data/"
    base += "csse_covid_19_daily_reports/"
    df = pd.read_csv(base + filename + ".csv", converters={'FIPS': str})
    # df.dropna()  # This doesn't do anything because missing data are not NaN when FIPS is read as a string
    # This eliminates rows without a FIPS (i.e., foreign countries)
    return df[df['FIPS'] != ""]

def get_death_number_JHU(start, end):
    """This is a function that returns a dataframe that contain Fips and the death number from start to end (two dates passed as strings), and create a csv file in data 
    Parameters: 
        start: str , write it in form "05-01-2021.csv",
        end: str,
    """
    data = {}

    df_deaths = readit(end)
    for i, row in df_deaths.iterrows():
        fips = row['FIPS']
        if len(fips) == 4:
            fips = "0" + fips
        data[fips] = row["Deaths"]
    # print(data)
    df_deaths = readit(start)
    for i, row in df_deaths.iterrows():
        fips = row['FIPS']
        if len(fips) == 4:
            fips = "0" + fips
        data[fips] -= row["Deaths"]

    # Write dictionary to a CSV file
    filename = "./data/deaths" + \
               start[:2] + '-' + start[3:5] + "-" + start[6:10] + "-to-" + \
               end[:2] + '-' + end[3:5] + "-" + end[6:] + ".csv"

    with open(filename, 'w') as file:
        file.write("FIPS,Deaths\n")  # header
        for key, value in data.items():
            file.write(",".join([key, str(value)]) + "\n")
    df = pd.read_csv(filename)
    return df

def get_confirm_number_JHU(start, end):
    """This is a function that returns the confirmed number from start_date to end_date
    Parameters: 
        start_date:str , write it in form "05-01-2021.csv",
        end_date: str,
    """
    data = {}

    df_confirmed = readit(end)
    for i, row in df_confirmed.iterrows():
        fips = row['FIPS']
        if len(fips) == 4:
            fips = "0" + fips
        data[fips] = row["Confirmed"]
    # print(data)
    df_confirmed = readit(start)
    for i, row in df_confirmed.iterrows():
        fips = row['FIPS']
        if len(fips) == 4:
            fips = "0" + fips
        data[fips] -= row["Confirmed"]

    # Write dictionary to a CSV file
    filename = "data/confirmed-" + \
               start[:2] + '-' + start[3:5] + "-" + start[6:10] + "-to-" + \
               end[:2] + '-' + end[3:5] + "-" + end[6:] + ".csv"

    with open(filename, 'w') as file:
        file.write("FIPS,Confirmed\n")  # header
        for key, value in data.items():
            file.write(",".join([key, str(value)]) + "\n")
    df = pd.read_csv(filename)
    print()
    return df

def create_death_number_JHU():
    """This function writes death number into 7 (month) csv files, each file document death number from 05-01 to the end of this month
    Please create a JHU file in ../data First, Or this function will give error. 
    If you don't want to wast time to input augument to create csv file for every month please run following function
    """
    start = "01-01-2022"
    ends = [
        "01-31-2022",
        "02-28-2022",
        "03-31-2022",
        "04-30-2022",
        "05-31-2022",
        "06-29-2022",
        "07-27-2022"
    ]
    for end in ends:
        get_death_number_JHU(start, end)
        get_confirm_number_JHU(start, end)

if __name__ == "__main__":
    create_death_number_JHU()

def vaccines(desired_date):
    """Sample one date from the source dataset and write it to an intermediate file
    Parameters:
        desired_date: str, date to be sampled for vaccine completedness
    """
    input_filename = "data/cdc.gz"
    df = pd.read_csv(input_filename,compression="gzip", converters={'FIPS' : str})
    cdc = df
    print("START:", df.shape)
    
    # Filter by date
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
    desired_date = desired_date.replace("-", "/")
    df = df[df["Date"] == desired_date]

   
    columns = ["FIPS", "Recip_County", "Recip_State", "Series_Complete_18PlusPop_Pct", "Census2019_18PlusPop"]
    df = df[columns]


    # Clean the dataset (removes 62 rows for 11/30/2021)
    print("BEFORE:", df.shape)
    df = df.dropna()
    print("AFTER:", df.shape)

    # Output
    output_filename = "./data/vaccinations-" + desired_date[:2] + '-' + \
                    desired_date[3:5] + "-" + desired_date[6:11] + ".csv"

    # Write filtered dataframe to a file
    df.to_csv(output_filename, index=False)
    return df

def create_vaccines():
    """This function generates vaccination data for seven different dates.
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
        vaccines(date)

if __name__ == "__main__":
    create_vaccines()

def merge(date):
    """
    This function return a dataframe that contains merge data. It use dataframes merge option that Prof. Bogden mentioned
    scatterplot team can use it to get the dataframe they want
    But please make sure that the csv to merge are already in in the ..data/JHU and ..data/CDC
    Parameters: 
        date : str, The last date of each month.  form date = "11-30-2021"
    """
    base_CDC = "data/"
    base_JHU = "data/"
    df = pd.read_csv(base_CDC + "vaccinations-" + date + ".csv",
                     converters={'FIPS': str})
    deaths = pd.read_csv(
        base_JHU + "deaths01-01-2022-to-"+date+".csv", converters={'FIPS': str})

    # Add the deaths data to the dataframe
    return df.merge(deaths, on='FIPS')

def write_merge_data_to_csv(date):
    """This function write a csv to directory data/Merge. 
    Parameters: 
        date: str, The last date of each month.  form date = "11-30-2021"
    """
    base_Merge = "./data/"
    df = merge(date)
    # print(df)
    df.to_csv(base_Merge+"vaccinations-and-deaths-"+date+'.csv', index=False)

def create_merge_data():
    """This function write 7 csvs to directory data/Merge. 
    Please make sure that the csv to merge are already in in the ..data/JHU and ..data/CDC
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
        write_merge_data_to_csv(date)

if __name__ == "__main__":
    create_merge_data()

def merge(date):
    """
    This function return a dataframe that contains merge data. It use dataframes merge option that Prof. Bogden mentioned
    scatterplot team can use it to get the dataframe they want
    But please make sure that the csv to merge are already in in the ..data/JHU and ..data/CDC
    Parameters: 
        date : str, The last date of each month.  form date = "01-31-2022"
    """
    base_CDC = "data/"
    base_JHU = "data/"
    df = pd.read_csv(base_CDC + "vaccinations-and-deaths-" + date + ".csv",
                     converters={'FIPS': str})
    confirmed = pd.read_csv(
        base_JHU + "confirmed-01-01-2022-to-"+date+".csv", converters={'FIPS': str})

    # Add the deaths data to the dataframe
    return df.merge(confirmed, on='FIPS')

def write_merge_data_to_csv(date):
    """This function write a csv to directory data/Merge. 
    Parameters: 
        date: str, The last date of each month.  form date = "11-30-2021"
    """
    base_Merge = "./data/"
    df = merge(date)
    # print(df)
    df.to_csv(base_Merge+"vaccinations-and-confirmed-"+date+'.csv', index=False)

def create_merge_data():
    """This function write 7 csvs to directory data/Merge. 
    Please make sure that the csv to merge are already in in the ..data/JHU and ..data/CDC
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
        write_merge_data_to_csv(date)

if __name__ == "__main__":
    create_merge_data()

county_land.to_csv("./data/Land.csv",index=False)

def merge(date):
    """
    This function return a dataframe that contains merge data. It use dataframes merge option that Prof. Bogden mentioned
    scatterplot team can use it to get the dataframe they want
    But please make sure that the csv to merge are already in in the ..data/JHU and ..data/CDC
    Parameters: 
        date : str, The last date of each month.  form date = "01-31-2022"
    """
    base_CDC = "data/"
    base_JHU = "data/"
    df = pd.read_csv(base_CDC + "vaccinations-and-confirmed-" + date + ".csv",
                     converters={'FIPS': str})
    Land = pd.read_csv(
        base_JHU + "Land.csv", converters={'FIPS': '{:0>5}'.format})

        

    # Add the deaths data to the dataframe
    return df.merge(Land, on='FIPS')

def write_merge_data_to_csv(date):
    """This function write a csv to directory data/Merge. 
    Parameters: 
        date: str, The last date of each month.  form date = "01-31-2022"
    """
    base_Merge = "./data/"
    df = merge(date)
    # print(df)
    df.to_csv(base_Merge+"county-and-land-"+date+'.csv', index=False)

def create_merge_data():
    """This function write 7 csvs to directory data/Merge. 
    Please make sure that the csv to merge are already in in the ..data/JHU and ..data/CDC
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
        write_merge_data_to_csv(date)

if __name__ == "__main__":
    create_merge_data()





















