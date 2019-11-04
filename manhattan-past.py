import requests
import time


def get_average_temp(station_name, start_date):
	uri_string = "http://mesonet.k-state.edu/rest/stationdata/?stn=" + station_name +"&int=day&t_start=" + str(start_date) + "&t_end=20190101013000&vars=TEMP2MAVG,PRECIP"
	print(uri_string)	
	res = requests.get(uri_string)
	returned_data = res.text

	temp_array = []
	for line in returned_data.splitlines()[1:]:
		temp = float(line.split(",")[2])
		print(line)
		print(temp)
		temp_array.append(temp)
	print(sum(temp_array))    



def calculate_skips(interval, initial_time):
	interval_itr = 0
	num_of_itrs = 1
	time_set = 1
	next_start_date = ""
	if interval == "one day":
		interval_itr = 365
		time_set  = 24*60
	elif interval == "one hour":
		interval_itr = 365 * 24
		time_set = 60
	elif interval == "five minutes":
		interval_itr = 365 * 24 * 12
		time_set = 5	
	arr = []
	dates_arr = []

	year = initial_time[:4]	
	month = initial_time[4:6]

	if interval_itr>3000:
		num_of_itrs = (interval_itr / 3000) + 1
		seconds_elapsed, hours_elapsed, days_elapsed, minutes_elapsed = 0, 0, 0, 0
		months_elapsed = month
		print(months_elapsed)
		for itr in range(interval_itr):

			seconds_elapsed =  time_set * 60 * itr
			
			months_elapsed = seconds_elapsed // (30 * 86400)
			seconds_elapsed = seconds_elapsed - (months_elapsed * (30 * 86400))
	
			days_elapsed = seconds_elapsed // 86400
			seconds_elapsed = seconds_elapsed - (days_elapsed * 86400)

			hours_elapsed = seconds_elapsed // 3600
			seconds_elapsed = seconds_elapsed - (hours_elapsed * 3600)

			minutes_elapsed = seconds_elapsed // 60
			seconds_elapsed = seconds_elapsed - (minutes_elapsed * 60)	
			
			dates_arr.append(str(months_elapsed)+ " " + str(days_elapsed)+ " " + str(hours_elapsed)+ " " + str(minutes_elapsed) + " " + str(seconds_elapsed))
	
		arr.append(str(months_elapsed))
		arr.append(str(days_elapsed))
		arr.append(str(hours_elapsed))
		arr.append(str(minutes_elapsed))
		arr.append(str(seconds_elapsed))
	
	new_format_arr = []
	for dates in dates_arr:
		new_format = ""
		for d in dates.split(" "):
			if len(d)<2:
				d = "0" + d
			new_format+= d
		new_format_arr.append(new_format)
	return new_format_arr

def format_date_year(dates_array):
	final_date_arr = []
	for date in dates_array:
		date = "2018" + date
		final_date_arr.append(date)
	print(final_date_arr)
	return final_date_arr

rest_calls = format_date_year(calculate_skips("one hour", "20180101000000"))

def rest_call(station_name, rest_calls):	
	for calls in range(len(rest_calls)):		
		get_average_temp(station_name, rest_calls[calls])
		
rest_call("Manhattan", rest_calls)
	


	

	






