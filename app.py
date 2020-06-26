from alpha_vantage.timeseries import TimeSeries
import math
from datetime import datetime
import pytz
import time


# define variables

init_money_total = 1000
money_total = 1000
bought = False
sold = False
run = True
ts = TimeSeries(key='JY8G0X0SXPCGYXWU', output_format='pandas')




# GET US TIME

def get_current_us_time():
	eastern = pytz.timezone('US/Eastern')
	us_time = datetime.now(eastern)
	current_time = us_time.strftime('%H:%M')
	return current_time



# GET current price (tested = yes)

def get_price_buy():
	
	data, meta_data = ts.get_intraday(symbol='IBM', interval='5min', outputsize='compact')
	values = data['4. close']

	price = values[0]
	
	return price


# HIGH AVERAGE (tested = yes)

def h_average():
	global av_data, meta_data


	av_data, meta_data = ts.get_daily(symbol='IBM', outputsize='compact')
	high_values = av_data['2. high']

	sum_high = 0
	n = 0

	for i in range(14):
		sum_high += high_values[i]
		n += 1

	high_average = float(sum_high)/n

	return high_average



# LOW AVERAGE (tested = yes)

def l_average():
	

	low_values = av_data['3. low']

	sum_low = 0
	n = 0

	for i in range(14):
		sum_low += low_values[i]
		n += 1

	low_average = float(sum_low)/n

	return low_average

# trade (tested = yes)



def trade(init_price_usd, high_avarage, low_average):
	global money_total
	global n_buy
	global bought
	global sold
	global printed_buy_msg

	if init_price_usd <= low_average and bought == False:
		
		n_buy = math.floor(money_total/init_price_usd)
		
		
		shares_bought = n_buy*init_price_usd
		
		money_total = money_total - shares_bought
		
		
		bought = True

		printed_buy_msg = False
		
		return money_total

	elif init_price_usd >= high_avarage and bought == True:
		
		shares_sold = n_buy*init_price_usd
		money_total = money_total + shares_sold
		
		
		bought = False
		
		
		sold = True
		
		return money_total
	else:
		return 'passed'



# RUN THE TRADE


def get_result(current_time):
	global sold
	global n_buy
	global printed_buy_msg

	

	init_price_usd = get_price_buy()

	high_avarage = h_average()

	low_avarage = l_average()

	tots = trade(init_price_usd, high_avarage, low_avarage)
	

	if sold is True:
		print('sold {} shares at {}, total money = {}'.format(n_buy, current_time, tots))
		n_buy = 0
		profit = tots - init_money_total
		profit_pc = (profit/init_money_total)*100
		result = '\n' + str(date) + ',' + str(init_price_usd) + ',' + str(tots) + ',' + str(profit_pc) + '%'
		with open("result.csv", "a") as file:
			file.write(result)
			file.close()
		sold = False

	elif bought is True and printed_buy_msg is False:
		print('Bought {} shares at {}, total money = {}\n'.format(n_buy, current_time, tots))
		printed_buy_msg = True

	elif bought is True and printed_buy_msg is True:
		print('waiting for sale {}\n h_average = {} | l_average = {} | price = {}\n'.format(current_time, high_avarage, low_avarage, init_price_usd))






while run == True:

	current_time = get_current_us_time()

	get_result(current_time)

	if current_time == '16:00':
		run = False
		print('End at {}: Done\n{}'.format(current_time, money_total))

	time.sleep(300)  # change to 300


	



		










