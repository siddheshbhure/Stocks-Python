# from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as dtl
import datetime as dtm
import requests
import os
import io
import webbrowser

import stocks_util as util
import model_util as mutil
import quandl
import yfinance as yf



def main():

	complist = util.read_availability()
	symbol = 'AAPL'
	symbol = symbol if symbol.isupper() else symbol.upper()
	if not symbol in complist['Symbol'].values:
		print('--'*25)
		print('Stock not found in our repository.')

	else:
		symbol = symbol if symbol.isupper() else symbol.upper()
		file_save = 'data-%s.csv'%symbol

		if not os.path.exists(file_save):

			# # apikey = '6S047KHPDKJ9SI9G'
			# apikey = 'Ye-htV-xy8cmoDMmBzSw'

			# # CSV file with all the stock market data for AAL from the last 20 years
			# # url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s&datatype=csv"%(symbol,apikey)
			# url = 'https://www.quandl.com/api/v3/datasets/FINRA/FNSQ_'+symbol+'.csv?api_key='+apikey
	
			# s = requests.get(url).content
			# data = pd.read_csv(io.StringIO(s.decode('utf-8')),header=0,parse_dates=True)

			data = yf.download(symbol)


			# quandl.ApiConfig.api_key = "Ye-htV-xy8cmoDMmBzSw"
			# data = quandl.get("EIA/AAPL")
			# print(data)
			
			data = data.sort_values('Date')
			data.dropna(inplace = True)
			data.drop_duplicates(inplace = True)
			data.to_csv(file_save)
			
			data.index = pd.to_datetime(data.index)
			data = data.resample('1D').pad()
			# print('Data loading Complete...')
			print('Data loading for '+symbol+' stock Completed...')
			# print('Data loading for '+symbol+' '+complist.loc[(complist['Symbol'] == symbol),'Name'].astype('str')+'stock Completed...')
			print('Data was found for dates '+str(data.index[0])+' to '+str(data.index[-1]))
			print(data)

		else:
			print('yeee in else')
			data = pd.read_csv(file_save)
			data.set_index('Date',inplace = True)

			if dt.strptime(data.index[-1],'%Y-%m-%d').date() == dt.now().date():
				
				data.index = pd.to_datetime(data.index)
				print(data.index[-1])
				
				
			else:
				start = dt.strftime(dt.strptime(data.index[-1],'%Y-%m-%d').date() + dtl(days = 1),'%Y-%m-%d')
				end = dt.now().strftime('%Y-%m-%d')
				print(start)
				print(end)
				data_partial= yf.download(symbol,start = start,end = end)
				print(data_partial)
				data = data.append(data_partial)
				data.index = pd.to_datetime(data.index)
				data.drop_duplicates(inplace = True)
				data.to_csv(file_save)

				print(data)	

			# data = data.resample('1D').pad()
			# print(data)
			# # data['timestamp']
			# print('Data loading for '+symbol+' stock Completed...')
			# # print('Data loading for '+symbol+' '+complist.loc[(complist['Symbol'] == symbol),'Name'].astype('str')+'stock Completed...')
			# print('Data was found for dates '+str(data.index[0])+' to '+str(data.index[-1]))
			# print('--'*25)
	

if __name__ == "__main__":
	main()


# https://www.quandl.com/api/v3/datasets/FINRA/FNSQ_AAPL.csv?api_key=Ye-htV-xy8cmoDMmBzSw
# https://www.quandl.com/api/v3/datasets/FINRA/FNSQ_MSFT.csv?api_key=Ye-htV-xy8cmoDMmBzSw