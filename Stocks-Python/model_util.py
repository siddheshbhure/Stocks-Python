import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
from statsmodels.tsa.stattools import adfuller

from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn import linear_model

#gets the P value for Ad Fuller
def get_stationarity(timeseries):
   
    # Dickey–Fuller test:
    result = adfuller(timeseries['Close'])
    # print('ADF Statistic: {}'.format(result[0]))
    # print('p-value: {}'.format(result[1]))
    # print('Critical Values:')
    # for key, value in result[4].items():
    #     # print('\t{}: {}'.format(key, value))

    return result[1]

def getPredictionLIN(dataslice):

	try:

		dataslice_lin = dataslice.copy()
		dataslice_lin.reset_index()
		dataslice_lin.index = range(len(dataslice_lin))

		dates = dataslice_lin.index.tolist()
		prices = dataslice_lin['Close'].tolist()
		
		linear_mod = linear_model.LinearRegression() #defines the linear reg. model
		dates = np.reshape(dates,(len(dates),1)) # converts to an n * 1 matrix to provide to the function
		prices = np.reshape(prices,(len(prices),1))
		linear_mod.fit(dates,prices) #fits the data points into model
		

		pred_fl = True
		while pred_fl:
			pred_date = input('Enter a date in YYYY-MM-DD format for which you would like stock prediction. \'0\' to go back to previous menu.\n')
			if pred_date != '0':
				diff = (dt.strptime(pred_date,'%Y-%m-%d') - dataslice.index[0]).days
				print('diff = '+str(diff))

				predicted_price =linear_mod.predict(np.array(diff).reshape(1, 1))

				# return predicted_price[0][0],linear_mod.coef_[0][0] ,linear_mod.intercept_[0]

				# predicted_price, coeff, constant = predict_price(dataslice,diff)
				print('--'*25)
				print()
				print ('The stock Close price for'+ pred_date +' is = ',str(predicted_price[0][0]))
				print ('The regression coefficient is ',str(linear_mod.coef_[0][0]),", and the constant is = ", str(linear_mod.intercept_[0]))
				print ('Equation between dates and prices is: price = ',str(linear_mod.coef_[0][0]),'* date + ',str(inear_mod.intercept_[0]))
				print()
				print('--'*25)
			else:
				pred_fl = False



	except Exception as e:
		print('--'*25)
		print(e)
		print('--'*25)


	
	# print(dataslice_lin)
	# predicted_price, coeff, constant = predict_price(dataslice_lin.index.tolist(),dataslice_lin['Close'].tolist(),diff)

	
	
	


# Incorportes ARIMA model to provide stock value prediction for date entered
def getPredictionARIMA(dataslice):

	print('Making Data Stationary...')
	dataslice_log = np.log(dataslice)
	p_val = get_stationarity(dataslice)
	# print(p_val)
	
	d = 0
	# makes data stationary before as required for applying ARIMA
	while p_val > 0.05:
		
		d=d+1
		
		rolling_mean = dataslice_log.rolling(window=15).mean()
		dataslice_log_minus_mean = dataslice_log - rolling_mean
		dataslice_log_minus_mean.dropna(inplace=True)

		dataslice_log = dataslice_log_minus_mean.copy()

		p_val = get_stationarity(dataslice_log_minus_mean)

	d = d if d > 0 else 1

	print('Selected Diffentiating Order is ='+str(d))
	print('Applying Model on Training Data...')
	print('--'*25)

	steps = -30				#Forecasts the value for last month to obtain RMSE

	y_truth = dataslice[int(steps):]
	
	# print(dataslice)
	model = SARIMAX(dataslice['Close'], trend = 'c',order=(2,d,2))
	model_results = model.fit(disp = False)

	dynamic_forecast = model_results.get_prediction(start=int(steps))
	mean_forecast = dynamic_forecast.predicted_mean 
	conf_interval = dynamic_forecast.conf_int()

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


	pred_fl = True
	while pred_fl:
		pred_date = input('Enter a date in YYYY-MM-DD format for which you would like stock prediction. \'0\' to go back to previous menu.\n')
		if pred_date != '0':
			try:
				diff = (dt.strptime(pred_date,'%Y-%m-%d') - dataslice.index[-1]).days
				# print('diff = '+str(diff))

				# print(dataslice)
				if not diff <= 0 :

					forecast = model_results.get_forecast(steps = diff,dynamic = False).predicted_mean

					
					# print(forecast)

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

					print('cant predict past date out of training sample..\n Use linear regression..')
					
					
				
			except Exception as e:
				print('--'*25)
				print(e)
				print('--'*25)
		else:
			pred_fl = False

	return model_results


def prediction(data):
	
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

				ch_fl = True
				while  ch_fl:
					ch = input('1. ARIMA Model \n2. Linear Regression \n0. Previous Menu \nPlease choose Option:')
					if ch == '1':
						tr_fl = False
						getPredictionARIMA(dataslice)
					elif ch == '2':
						tr_fl = False
						getPredictionLIN(dataslice)
					elif ch == '0':
						ch_fl = False
					else:
						print('--'*25)
						print('Invalid Choice Please select from above option numbers only.')
			else:
				raise Exception('Training period must be greater than 3 months.')


		except ValueError as v:
			print('--'*25)
			print('Please select a valid training period (e.g. 6, 12, 24, etc.)... ')
			print(v)
			print('--'*25)

		except Exception as e:
			print('--'*25)
			print(e)
			print('--'*25)


# Applying the model to calculate predicted value based on user provided training window
	

	

	