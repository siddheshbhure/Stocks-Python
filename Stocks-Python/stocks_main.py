# from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as dtl
import requests
import os
import io

import stocks_util as util
import model_util as mutil
import yfinance as yf
from pandas_datareader import data as pdr




def read_stock():
	#Checks ticker availability
	complist = util.read_availability()

	fl = True
	while fl == True:
		print('--'*25)		
		symbol = input('Please Enter stock name to proceed or \'0\' To Go back to Previous Menu..\n')
		# symbol = symbol.isupper()?symbol:symbol.upper()
		if symbol != '0':
			
			# print(symbol)
			# print(complist['Symbol'].values)

			symbol = symbol if symbol.isupper() else symbol.upper()

			if not symbol in complist['Symbol'].values:
				print('--'*25)
				print('Stock not found in our repository.')

			else:
				symbol = symbol if symbol.isupper() else symbol.upper()
				file_save = 'stock_data-%s.csv'%symbol
				tick = yf.Ticker(symbol)

				if not os.path.exists(file_save):

					# apikey = '6S047KHPDKJ9SI9G'
					# newkey = 'Ye-htV-xy8cmoDMmBzSw'

					# # CSV file with all the stock market data for AAL from the last 20 years
					# url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s&datatype=csv"%(symbol,apikey)

					# # Save data to this file
					# s = requests.get(url).content
					# data = pd.read_csv(io.StringIO(s.decode('utf-8')),header=0,parse_dates=True)

					data = yf.download(symbol)

					
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


				else:

					data = pd.read_csv(file_save)
					data.set_index('Date',inplace = True)
					pd.to_datetime(data.index)

					if dt.strptime(data.index[-1],'%Y-%m-%d').date() == dt.now().date():
						
						print('Using Existing Data...')
						# print(data.index[-1])
						print('--'*25)
						data.index = pd.to_datetime(data.index)
						print('Data loading for '+symbol+' stock Completed...')
					
						print('Data was found for dates '+str(data.index[0])+' to '+str(data.index[-1]))

						
						
					else:
						# print('in else')
						print('Loading partial data...')
						start = dt.strftime(dt.strptime(data.index[-1],'%Y-%m-%d').date() ,'%Y-%m-%d')
						end = dt.now().strftime('%Y-%m-%d')
						
						data_partial= yf.download(symbol,start = start,end = end)						
						
						# print(data_partial)
						data = data.append(data_partial)
						data.index = pd.to_datetime(data.index)
						data.sort_values('Date',inplace = True)
						data = data.reset_index().drop_duplicates(subset ='Date' ,keep = 'first').set_index('Date')

						
						
						data.to_csv(file_save)
						
						data = data.resample('1D').pad().copy()

						print(data)	

					
						print('Data loading for '+symbol+' stock Completed...')
						# print('Data loading for '+symbol+' '+complist.loc[(complist['Symbol'] == symbol),'Name'].astype('str')+'stock Completed...')
						print('Data was found for dates '+str(data.index[0])+' to '+str(data.index[-1]))
						print('--'*25)
					
				slfl = True
				while slfl == True:
					
					print('--'*25)
					print('1. OHLC Graph \n2. Time Range \n3. Forecast \n0. Previous Menu')

					choice = input("Please choose option: ")

					if choice == '1':
						util.OHLC(data,symbol)
					elif choice == '2':
						util.get_timerange_graph(data)
					elif choice == '3':
						mutil.prediction(data)
					elif choice == '0':
						slfl = False
					else:
						print('--'*25)
						print('Invalid Choice Please select from above option numbers only.')
					
		else:
			fl = False


def main():
	# print("yeee...")
	flag = True
	while flag == True:
		print('--'*25)
		
		print('Welcome to the Stock Analysis Pro.')
		print('1. View Stock List \n2. Analyse Stock \n3. User Manual \n4. Quit')
		
		choice = input("Please choose option: ")

		if choice == '2':
			read_stock()
		elif choice == '1':
			pass
		elif choice == '3':
			pass
		elif choice == '4':
			flag = False
		else:
			print('--'*25)
			print('Invalid Choice Please select from above option numbers only.')


if __name__ == "__main__":
	main()