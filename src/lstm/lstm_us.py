# -*- coding: utf-8 -*-



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow import keras 
from tensorflow.keras import layers, losses, optimizers, Sequential

from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from sklearn.metrics import mean_squared_error
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, Activation
from tensorflow.keras.callbacks import ReduceLROnPlateau
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv('https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

df.drop(columns=['Province/State', 'Lat', 'Long'], inplace=True)
df = df.groupby(['Country/Region']).sum()
df.columns = pd.to_datetime(df.columns)

df_daily = df - df.shift(1, axis=1, fill_value=0)
df_daily_moving = df_daily.rolling(window=7, axis=1).mean()

plt.figure(figsize=(16, 6))

plt.xlabel('Date', fontsize=16)
plt.ylabel('Cases', fontsize=16)
plt.title('Covid-19 confirmed cases (US, India, China)', fontsize=16)

plt.plot(df_daily_moving.loc['US'])
plt.plot(df_daily_moving.loc['India'])
plt.plot(df_daily_moving.loc['China'])

plt.legend(['US', 'India', 'China'])
plt.savefig('img/'+'Three countries daily confirmed case')
plt.show()



country = 'US'
nfeatures = 1
nsteps = 7

feature_1 = df_daily.loc[country]

dataset = np.column_stack([feature_1])

data_len = len(dataset[:, 0])
train_len = int(0.8 * data_len)
test_len = data_len - train_len

train_data = dataset[:train_len, :]
test_data = dataset[train_len:, :]

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))

train_data = scaler.fit_transform(train_data)
test_data = scaler.transform(test_data)

train_x = np.array([train_data[i - nsteps:i, :] for i in range(nsteps, train_len)])
train_y = np.array([train_data[i, 0] for i in range(nsteps, train_len)])

test_x = np.array([test_data[i - nsteps:i, :] for i in range(nsteps, test_len)])
test_y = np.array([test_data[i, 0] for i in range(nsteps, test_len)])





from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

model = Sequential([
    LSTM(units=50, input_shape=(nsteps, nfeatures), return_sequences=True),
    LSTM(units=50),
    Dense(units=25),
    Dense(units=nfeatures)
])

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(x=train_x, y=train_y, batch_size=1, epochs=50)

predictions = model.predict(test_x)
predictions = scaler.inverse_transform(predictions)

plt.figure(figsize=(16, 8))

plt.title(f'Covid-19 daily confirmed cases of {country}', fontsize=18)

time_series = feature_1
train_time_series = time_series.iloc[500:train_len]
test_time_series = time_series.iloc[train_len:]
pred_time_series = pd.Series(data=predictions[:, 0], index=test_time_series.index[nsteps:])

plt.plot(train_time_series)
plt.plot(test_time_series)
plt.plot(pred_time_series)

plt.legend(['train', 'test', 'pred'])
plt.savefig('img/'+'US daily confirmed case prediction')
plt.show()



print(f'Prediction of tomorrow is {int(predictions[-1, 0])}')








