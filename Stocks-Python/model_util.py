import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
from statsmodels.tsa.stattools import adfuller

from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn import linear_model


def get_stationarity(timeseries):
   
    # Dickey–Fuller test:
    result = adfuller(timeseries['Close'])
    # print('ADF Statistic: {}'.format(result[0]))
    # print('p-value: {}'.format(result[1]))
    # print('Critical Values:')
    # for key, value in result[4].items():
    #     # print('\t{}: {}'.format(key, value))

    return result[1]

def predict_price(dates,prices,x):

	
	linear_mod = linear_model.LinearRegression() #defining the linear regression model
	dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
	prices = np.reshape(prices,(len(prices),1))
	linear_mod.fit(dates,prices) #fitting the data points in the model
	predicted_price =linear_mod.predict(np.array(x).reshape(1, 1))
	return predicted_price[0][0],linear_mod.coef_[0][0] ,linear_mod.intercept_[0]


def getPredictionARIMA(dataslice,d,steps):

	y_truth = dataslice[int(steps):]
	
	# print(dataslice)
	model = SARIMAX(dataslice['Close'], trend = 'c',order=(2,d,2))
	model_results = model.fit(disp = False)


	# print(model_results.fittedvalues)
	# print(model_results.)

	dynamic_forecast = model_results.get_prediction(start=int(steps))
	mean_forecast = dynamic_forecast.predicted_mean 
	conf_interval = dynamic_forecast.conf_int()

	# print(y_truth)
	# print('-------------------------------')
	# print(mean_forecast)


	mse = np.round(((mean_forecast - y_truth['Close']) ** 2).mean(),decimals = 3)
	rmse = np.round(np.sqrt(mse),decimals = 3)
	
	print('--'*25)
	print("Model Created with following Parameter.")
	print('MSE -> ',mse)
	print('RMSE -> ',rmse)
	print('--'*25)


	pd.plotting.register_matplotlib_converters()
	plt.figure(figsize=(16,5))
	plt.grid(True)
	plt.plot(dataslice.index,dataslice['Close'],label = 'observed')
	plt.plot(mean_forecast.index,mean_forecast,color = 'r',label= 'forecast')
	plt.xlabel('Date',fontsize = 18)
	plt.ylabel('Stock Price - Close USD',fontsize = 18)
	plt.legend()
	plt.show()

	return model_results


def prediction(data):
	# print('How would you like to continue analysis on all the data available or ')
	print('--'*25)
	tr_fl = True
	while tr_fl:

		tr = input("Select Training period in number of months (must be greater than 3 months)\n")

		try:
			if not int(tr) <= 3:

				dataslice = data.last(str(tr)+'M').loc[:,['Close']]
				

				# print(dataslice)
				print('--'*25)
				print('Training Data Loaded...')
				print('Making Data Stationary...')


				dataslice_log = np.log(dataslice)

				p_val = get_stationarity(dataslice)
				# print(p_val)
				
				d = 0

				while p_val > 0.05:
					
					d=d+1
					
					rolling_mean = dataslice_log.rolling(window=15).mean()
					dataslice_log_minus_mean = dataslice_log - rolling_mean
					dataslice_log_minus_mean.dropna(inplace=True)

					dataslice_log = dataslice_log_minus_mean.copy()

					p_val = get_stationarity(dataslice_log_minus_mean)
					# print(p_val)
					# print('d='+str(d))

				d = d if d > 0 else 1

				print('Selected Diffentiating Order is ='+str(d))
				print('Applying Model on Training Data...')
				print('--'*25)

				# model = SARIMAX(dataslice, trend = 'c',order=(2,d,2))
				# model_results = model.fit(disp = False)

				steps = -30

				model_results = getPredictionARIMA(dataslice,d,steps)
				tr_fl = False

			else:

				raise Exception('Training period must be greater than 3')


		except ValueError as v:
			print('--'*25)
			print('select proper training period...')
			print(v)
			print('--'*25)

		except Exception as e:
			print('--'*25)
			print(e)
			print('--'*25)






	pred_fl = True
	while pred_fl:
		pred_date = input('Enter a date in YYYY-MM-DD format for which you would like stock prediction. \'0\' to go back to previous menu.\n')
		if pred_date != '0':
			try:
				diff = (dt.strptime(pred_date,'%Y-%m-%d') - dataslice.index[-1]).days
				# print('diff = '+str(diff))

				if not diff <= 0 :

					forecast = model_results.get_forecast(steps = diff,dynamic = False).predicted_mean
					# print(forecast)

					# print('yeee...')
					fin_forecast = pd.DataFrame(forecast,columns = ['Close'])
					# print(fin_forecast)

					print('--'*25)
					print('The Stock Close price for '+pred_date+' is = '+str(fin_forecast.Close[-1]))


					dataslice = dataslice.append(fin_forecast)
					# print(dataslice)

					plt.figure(figsize=(16,5))
					plt.grid(True)
					plt.plot(dataslice.index,dataslice,label = 'observed')
					plt.plot(fin_forecast.index,fin_forecast,color = 'r',label= 'forecast')
					plt.xlabel('Date',fontsize=18)
					plt.ylabel('Stock Price - Close USD',fontsize=18)
					plt.legend()
					plt.show()
				
				else:
					
					
					dataslice_lin = dataslice.copy()
					dataslice_lin.reset_index()
					dataslice_lin.index = range(len(dataslice_lin))

					# print(dataslice_lin)
					predicted_price, coeff, constant = predict_price(dataslice_lin.index.tolist(),dataslice_lin['Close'].tolist(),diff)

					
					
					print('--'*25)
					print()
					print ('The stock Close price for'+ pred_date +' is = ',str(predicted_price))
					print ('The regression coefficient is ',str(coeff),", and the constant is = ", str(constant))
					print ('Equation between dates and prices is: price = ',str(coeff),'* date + ',str(constant))
					print()
					print('--'*25)

			except Exception as e:
				print('--'*25)
				print(e)
				print('--'*25)
		else:
			pred_fl = False

	

	