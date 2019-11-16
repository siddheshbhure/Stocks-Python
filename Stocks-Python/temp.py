import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime as dt
import matplotlib.pyplot as plt

import plotly.graph_objects as go
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import linear_model



def get_stationarity(timeseries):
   
    # Dickey–Fuller test:
    result = adfuller(timeseries['close'])
    print('ADF Statistic: {}'.format(result[0]))
    print('p-value: {}'.format(result[1]))
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t{}: {}'.format(key, value))

    return result[1]

def predict_price(dates,prices,x):
	linear_mod = linear_model.LinearRegression() #defining the linear regression model
	dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
	prices = np.reshape(prices,(len(prices),1))
	linear_mod.fit(dates,prices) #fitting the data points in the model
	predicted_price =linear_mod.predict(np.array(x).reshape(1, 1))
	return predicted_price[0][0],linear_mod.coef_[0][0] ,linear_mod.intercept_[0]

def main():

	data = pd.read_csv('stock_data-AMD.csv')

	data = data.sort_values('timestamp')
	# data = data.set_index('timestamp')
	# data.index = pd.to_datetime(data.index)
	print(data)
	t = data.index.tolist()
	# print(timestamp)
	print(t)
	close = data['close'].tolist()
	
	# model = LinearRegression()
	# model.fit(data.index,data['close'])


	predicted_price, coefficient, constant = predict_price(t,close,-29)  

	
	print ("The stock open price for 29th Feb is:-",str(predicted_price))
	print ("The regression coefficient is ",str(coefficient),", and the constant is ", str(constant))
	print ("the relationship equation between dates and prices is: price = ",str(coefficient),"* date + ",str(constant))
	

if __name__ == "__main__":
	main()






