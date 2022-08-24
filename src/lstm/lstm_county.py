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



df= pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")

df1 = pd.DataFrame(df.values.T,columns = df.index,index = df.columns) 
df1.reset_index(inplace=True)
df1.rename(columns={'index':'Date'})
array_df1 = np.array(df1)  
FIPS = array_df1.tolist()  
FIPS = FIPS[0]         

FIPS=[str(x) for x in FIPS]
df1.columns = FIPS
df1=df1.rename(columns={'UID':'Date'})
data = df1.drop([0,1,2,3,4,5,6,7,8,9,10])
data.head(200)

data['Date'] = pd.to_datetime(data['Date'])

y=data[['Date','84025025']]

data.index=data['Date']

plt.figure(figsize=(16, 6))

plt.xlabel('Date', fontsize=16)
plt.ylabel('Cases', fontsize=16)
plt.title('Covid-19 confirmed cases (suffolk, Worcester, Norfolk)', fontsize=16)

plt.plot(data[["84025025"]].iloc[-365:])
plt.plot(data[['84025027']].iloc[-365:])
plt.plot(data[['84025021']].iloc[-365:])

plt.legend(['suffolk', 'Worcester', 'Norfolk'])
plt.savefig('img/'+'Boston counties confirmed')
plt.show()



dataset = data[['84025025']]
train = dataset.iloc[:600]
test = dataset.iloc[-365:]


def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)


scaler = MinMaxScaler(feature_range=(0, 1))
train = scaler.fit_transform(train)

look_back = 7
trainX, trainY = create_dataset(train, look_back)
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
test = scaler.fit_transform(test)
testx, testy = create_dataset(test, look_back)
testx = np.reshape(testx, (testx.shape[0], 1, testx.shape[1]))

model = Sequential()
model.add(LSTM(150, activation='relu', return_sequences=True, input_shape=(1,7)))
model.add(LSTM(64, activation='relu'))
model.add(Dense(64))
model.add(Dense(1))

model.compile(loss='mean_squared_error',optimizer='adam',metrics=['accuracy'])
reduce_lr = ReduceLROnPlateau(monitor='loss', patience=10, mode='max')
history=model.fit(trainX, trainY, epochs=50, batch_size=1, validation_split=0.33, verbose=2, callbacks=[reduce_lr])

predictions = model.predict(testx)
predictions = scaler.inverse_transform(predictions)

plt.figure(figsize=(16, 8))

plt.title(f'Covid-19 confirmed cases of suffolk county', fontsize=18)

time_series = dataset
train_time_series = time_series.iloc[500:600]
test_time_series = time_series.iloc[-365:]
pred_time_series = pd.Series(data=predictions[:, 0], index=test_time_series.index[7:])

plt.plot(train_time_series)
plt.plot(test_time_series)
plt.plot(pred_time_series)

plt.legend(['train', 'test','pred'])
plt.savefig('img/'+'suffolk county confirmed case prediction.png')
plt.show()




plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model train vs validation loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper right')
plt.savefig('img/'+'validation loss.png')
plt.show()



print(f'Prediction of tomorrow is {int(predictions[-1, 0])}')

