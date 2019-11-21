import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
from statsmodels.tsa.stattools import adfuller

from statsmodels.tsa.statespace.sarimax import SARIMAX
import plotly.graph_objects as go

def OHLC(data,symbol):
	try:

		fig = go.Figure(data=[go.Candlestick(x=data.index,open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
		fig.update_layout(title='OHLC Graph for '+symbol, yaxis_title=symbol+' Stock Value',xaxis_rangeslider_visible=False)
		fig.show()

	except Exception as e:
		print(e)

def user_manual():
	print('This program lets you perform descriptive and predictive analysis on a stock of your choice, that is available on NASDAQ.')
	print("""Here's what we got on the Main Menu:

	Option (1) will help you with stock tickers in case you don/'t know them. Once you know the symbol, go ahead to Option (2) and explore!
	Option (2) is where the treasure lies- Information & Insights on the stock that's up your mind!.
	Option (3) got you here :)
	Option (4) will help you exit the program.

	Upon entering Stock Analysis and providing a valid ticker, you will be able to-

	> View OLHC Graphs --> This will open default browser window and show OHLC graph along with some UI controls.
	> Time Series Information -->  This will ask for TO and FROM datea and give you basic statistical information 
	like Mean ,Standard Deviation, Range, Quartiles, etc.
	> Forecast values --> This will ask for the duration for which you want to train the model and the date 
	for which you want a prediction for a stock value.
	> Previous Menu  --> This will take you back to the previous menu.

	To make things easy, we give you the range of data we've found and let you pick between using all the available data for training 
	the output or choosing your own window - remember more data, the merrier.
	Go ahead, view graphs and gain insights before you invest.

	Hit (0) to go back to previous menu and explore.""")

def open_window():
	a_website = "https://www.nasdaq.com/market-activity/stocks/screener/"
	# Open url in a new window of the default browser, if possible
	return webbrowser.open_new(a_website)
	

def read_availability():
	# Loads master file to check for user provided stock
	complist = pd.read_csv('companylist.csv')
	return complist

def check_validity(fr):	#
	dt.datetime.strptime(fr,'%Y-%m-%d')


def plot_timeseries(dataslice,title,xlabel,ylabel):

	pd.plotting.register_matplotlib_converters()
	plt.figure(figsize=(16,5))
	plt.plot(dataslice.index,dataslice['Close'],color='tab:blue',label = 'Stock Price')
	plt.grid(True)
	# plt.xticks(range(0,dataslice.shape[0],100),dataslice['timestamp'].loc[::100],rotation=45)
	# # plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
	# # plt.show()
	plt.xlabel('Date',fontsize=18)
	plt.ylabel('Close Price',fontsize=18)
	# plt.xscale('log')
	plt.legend(loc=2)
	plt.show()


	# plt.figure(figsize = (18,9))
	
	# plt.xticks(range(0,dataslice.shape[0],500),dataslice['timestamp'].loc[::500],rotation=45)
	# plt.xlabel('Date',fontsize=18)
	# plt.ylabel('Close Price',fontsize=18)
	# plt.show()
    
#Calculates the Moving Avg, Weighte Moving Avg, MACD plots based on window provided by user
def plotMA(dataslice):
	winfl = True
	while winfl == True:
		try:
			win = input('Please Enter window size for calculating moving average. \'0\' to go back to previous menu\n')

			if win != '0':

				if int(win) < len(dataslice.index):

					dataslice['SMA'] = ''
					dataSMA = dataslice.iloc[:,3].rolling(window=int(win)).mean()
					dataslice['SMA'] = dataSMA

					
					weights = np.arange(1,int(win)+1)
					dataWMA = dataslice.iloc[:,3].rolling(window=int(win)).apply(lambda wts: np.dot(wts, weights)/weights.sum(), raw=True)
					dataslice['WMA'] = dataWMA

				# print(dataslice)
				
					dataslice['26EMA']=dataslice['Close'].ewm(span=26).mean()
					dataslice['12EMA']=dataslice['Close'].ewm(span=12).mean()

					
					dataslice['MACD'] = dataslice['12EMA']-dataslice['26EMA']

					# print(dataslice)

					plt.figure(figsize=(16,6))
					plt.subplot(3,1,1)
					plt.grid(True)
					plt.plot(dataslice.index,dataslice['Close'],label='data')	
					plt.legend(loc=2)
					plt.xlabel('Date',fontsize=15)
					plt.ylabel('Close Price',fontsize=15)

					plt.subplot(3,1,2)
					plt.grid(True)
					plt.plot(dataslice.index,dataslice['SMA'],label='SMA')
					plt.plot(dataslice.index,dataslice['WMA'],label='WMA')
					plt.legend(loc=2)
					plt.xlabel('Date',fontsize=15)
					plt.ylabel('Averages',fontsize=15)
					

					plt.subplot(3,1,3)
					plt.grid(True)
					plt.plot(dataslice.index,dataslice['MACD'],label='MACD')
					plt.legend(loc=2)
					plt.xlabel('Date',fontsize=15)
					plt.ylabel('MACD',fontsize=15)
					plt.show()

				else:
					print('--'*25)
					print('window size is greater than data')		#Ensures window size is valid
					print('--'*25)

			else:
				winfl = False

		except ValueError as v:
			print('--'*25)
			print('Invalid window size...')
			print(v)
			print('--'*25)

		except Exception as e:
			print('--'*25)
			print(e)

	# print(dataslice)


#Shows basic statistics
def stats_desc(dataslice):

	print('--'*25)
	print('Basic Statistics.')
	print('--'*25)
	# Minimum
	stock_min = dataslice['Close'].min()
	print('Stock Minimum:-',stock_min)

	#Maximum
	stock_max = dataslice['Close'].max()
	print('Stock Maximum:-',stock_max)

	# Mean
	mean = np.round(dataslice['Close'].mean(),decimals = 3)
	print("Mean:", mean)
	print()

	# Quartile
	print("First quantile:", np.quantile(dataslice['Close'], .25))
	print("Second quantile:", np.quantile(dataslice['Close'], .50))
	print("Third quantile:", np.quantile(dataslice['Close'], .75))
	print()

	# Range
	range = np.round(np.max(dataslice['Close'], axis=0) - np.min(dataslice['Close'], axis=0),decimals = 3)
	print("Range of the Stock: ", range)

	# Standard Deviation
	stdvar = np.round(np.std(dataslice['Close']),decimals = 3)
	print("Variation:", stdvar) 

	# Coefficient of Variation
	cov = np.round(stdvar/mean,decimals = 3)
	print("Coeff of Variation:", cov)
	print('--'*25)

	# Plots the time series graph
	plot_timeseries(dataslice,'Times Series','Date','Close Price')

	print('Advanced Statistics')
	print('--'*25)

	#Advanced Statistics
	plotMA(dataslice)
	
#Get specific time range data and handles incorrect time formats
def get_timerange_graph(data):
	dtfl = True
	while dtfl:
		print('--'*25)
		fr = input('Please Enter the FROM date in yyyy-mm-dd format \n\'A\' For Fetch Entire Data \n\'0\' to go back to previous menu \n')
		if fr not in ['0','A']:

			print('--'*25)
			to = input('Please Enter the TO date in yyyy-mm-dd format \n\'0\' to go back to previous menu\n')

			if to != '0':

				try:

					ll = dt.strptime(fr,'%Y-%m-%d')
					ul = dt.strptime(to,'%Y-%m-%d')
					
					dtfl = False
								
					dataslice = data[(data.index >= fr) & (data.index <= to)].copy()
					
					# Checks for empty data
					# print(dataslice)
					if dataslice.empty:
						print('--'*25)
						raise Exception("Data Empty")
					
					stats_desc(dataslice)
				except ValueError:
					print('--'*25)
					print('Either From or To Date were found invalid. Retry in the format suggested.')
					
				except Exception as e:
					print(e)
			else:

				dtfl = False
		elif fr == 'A':
			dtfl = False
			dataslice = data.copy()
			stats_desc(dataslice)
		else:
			dtfl = False