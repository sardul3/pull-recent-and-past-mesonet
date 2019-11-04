from datetime import datetime, date, time, timedelta
import requests
from matplotlib import pyplot as plt
import numpy as np

def convert_time(date_string):
	date_format = "%Y%m%d%H%M%S"
	formatted_date = datetime.strptime(date_string, date_format)
	return formatted_date

def rest_call_annual_data(station_name, interval, start_date, end_date):
	dates = calculate_new_date(start_date, end_date, interval)
	i = 0
	while i < len(dates):
		if i == len(dates)-1:
			break
		base_url = "http://mesonet.k-state.edu/rest/stationdata/?stn=%s&int=%s&t_start=%s&t_end=%s&vars=TEMP2MAVG,PRECIP" % (station_name, interval, dates[i], dates[i+1])
		i+=1
		res = requests.get(base_url)
		returned_data = res.text
		print(returned_data)
		f = open("./%s_%s_data.txt" % (station_name, interval), "w")
		f.write(returned_data)
		f.close()

def rest_call_average_temperature(station_name, interval, start_date, end_date, variable1, variable2):
	dates = calculate_new_date(start_date, end_date, interval)
	i = 0
	while i < len(dates):
		if i == len(dates)-1:
			break
		base_url = "http://mesonet.k-state.edu/rest/stationdata/?stn=%s&int=%s&t_start=%s&t_end=%s&vars=%s,%s" % (station_name, interval, dates[i], dates[i+1], variable1, variable2)
		i+=1
		res = requests.get(base_url)
		returned_data = res.text
		print(returned_data)
		f = open("./%s_%s_%s_data.txt" % (station_name, "10meter and 2meter", interval), "w")
		f.write(returned_data)

		ten_meter_array = []
		two_meter_array = []
		for line in returned_data.splitlines()[1:]:
			two_meter_temp = float(line.split(",")[2])
			ten_meter_temp = float(line.split(",")[3])
			ten_meter_array.append(ten_meter_temp)
			two_meter_array.append(two_meter_temp)
		average_ten_meter_temp = sum(ten_meter_array)/len(ten_meter_array)
		average_two_meter_temp = sum(two_meter_array)/len(two_meter_array)  
		
		f.write("\nAverage temperature for 10 meters --> %s" % (average_ten_meter_temp))
		f.write("\nAverage temperature for 2 meters --> %s" % (average_two_meter_temp))
		f.write("\nDifference --> %s" % (average_ten_meter_temp - average_two_meter_temp))
		f.close()
		return average_ten_meter_temp - average_two_meter_temp

def rest_call_frequency_calculate(station_name, interval, start_date, end_date, variable1, variable2):
	dates = calculate_new_date(start_date, end_date, interval)
	i = 0
	while i < len(dates):
		if i == len(dates)-1:
			break
		base_url = "http://mesonet.k-state.edu/rest/stationdata/?stn=%s&int=%s&t_start=%s&t_end=%s&vars=%s,%s" % (station_name, interval, dates[i], dates[i+1], variable1, variable2)
		i+=1
		res = requests.get(base_url)
		returned_data = res.text
		print(returned_data)
		f = open("./%s_%s_%s_frequency_check_data.txt" % (station_name, "10meter and 2meter", interval), "w")
		f.write(returned_data)

		ten_greater_than_two = []
		total_entries = 0
		count_ten_greater_than_two = 0
		for line in returned_data.splitlines()[1:]:
			two_meter_temp = float(line.split(",")[2])
			ten_meter_temp = float(line.split(",")[3])
			if(ten_meter_temp > two_meter_temp):
				count_ten_greater_than_two+=1
				ten_greater_than_two.append(line)
			total_entries+=1
		frequency = (float(count_ten_greater_than_two)/float(total_entries))*100.00
		f.write("\nPercentage of the entries where 10m is greater than 2m temp --> %d%s" % (frequency,"%"))
		return frequency

def rest_call_latest_frequency(station_name):
	current_datetime = datetime.now()
	start_datetime = current_datetime - timedelta(hours=25)
	end_datetime = current_datetime.replace(microsecond=0,second=0,minute=0)
	converted_start_date = parse_datetime(start_datetime)
	converted_end_date = parse_datetime(end_datetime)
	base_url = "http://mesonet.k-state.edu/rest/stationdata/?stn=%s&int=hour&t_start=%s&t_end=%s&vars=TEMP2MAVG,TEMP10MAVG" % (station_name, converted_start_date, converted_end_date)
	res = requests.get(base_url)
	returned_data = res.text

	ten_greater_than_two = []
	two_meter_arr = []
	ten_meter_arr = []
	time_hour_arr = []
	percent_diff_arr = []
	total_entries = 0
	count_ten_greater_than_two = 0
	for line in returned_data.splitlines()[1:]:
		two_meter_temp = (float(line.split(",")[2]) * (9.0/5.0)) + 32
		ten_meter_temp = (float(line.split(",")[3]) * (9.0/5.0)) + 32
		print(ten_meter_temp, two_meter_temp)
		percent_diff = (ten_meter_temp - two_meter_temp) 
		print(percent_diff)
		percent_diff_arr.append(percent_diff)
		time_hour = line.split(",")[0][8:10] + ":"+ line.split(",")[0][11:13]
		two_meter_arr.append(two_meter_temp)
		ten_meter_arr.append(ten_meter_temp)
		time_hour_arr.append(time_hour)
		if(ten_meter_temp > two_meter_temp):
			count_ten_greater_than_two+=1
			ten_greater_than_two.append(line)
			print('\x1b[0;30;43m' + line + '\x1b[0m' + '\n')
		else:
			print(line + '\n')
		total_entries+=1

	frequency = (float(count_ten_greater_than_two)/float(total_entries))*100.00
	
	dev_x = time_hour_arr
	dev_y = two_meter_arr
	py_dev_y = ten_meter_arr
	plt.plot(dev_x, dev_y, label="Two Meter Temperature", marker="o")
	plt.plot(dev_x, py_dev_y, label="Ten Meter Temperature", marker=".")
	plt.locator_params(axis='y', nbins=10)

	plt.xlabel("Time periods during the last 24 hours")
	plt.ylabel("Temperature")
	plt.title("Comparision of temperature at 2 meters and 10 meters for %s \n (%s%s)" % (station_name, round(frequency,1) , "% of the times 10m temp > 2m temp"))
	plt.legend()
	plt.grid()
	plt.tight_layout()
	figure = plt.gcf() # get current figure
	figure.set_size_inches(14, 12)
	plt.savefig('24_hr_10v2m_comp.png', dpi=100)
	plt.show()

	y_pos = range(len(time_hour_arr))
	plt.bar(y_pos, percent_diff_arr, align='center', alpha=0.5)
	plt.xticks(y_pos, time_hour_arr)
	plt.xlabel("Date and Hours during the last 24 hour period")
	plt.ylabel("Difference in 10m and 2m temperature")
	plt.title("10m vs 2m difference in temperature for %s" % (station_name))

	for i in range(len(time_hour_arr)):
		plt.text(i, percent_diff_arr[i], round(percent_diff_arr[i],2), horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight':500, 'size':12})
	
	plt.tight_layout()
	figure = plt.gcf() # get current figure
	figure.set_size_inches(14, 12)
	plt.savefig('24_hr_10v2m_comp_bar_graph_%s.png' % (station_name), dpi=100)
	plt.show()

	return frequency

def calculate_break_time(time_interval):	
	if(time_interval=="5min"):
		break_time = 900000
	elif(time_interval=="hour"):
		break_time = 3000 * 60 * 60
	elif(time_interval=="day"):
		break_time= 864000 * 300
	return break_time

def calculate_seconds_elapsed(start_date, end_date):
	converted_start_date = convert_time(start_date)
	converted_end_date = convert_time(end_date)
	diff_time = converted_end_date - converted_start_date
	diff_seconds = diff_time.total_seconds()
	return diff_seconds

def parse_datetime(datetime_obj):
	year = datetime_obj.year
	month = datetime_obj.month
	day = datetime_obj.day
	hour = datetime_obj.hour
	minute = datetime_obj.minute
	second = datetime_obj.second
	parsed_date = "%s%02d%02d%02d%02d%02d" % (year, month, day, hour, minute, second)
	return parsed_date	

def calculate_new_date(start_date, end_date, time_interval):
	converted_start_date = convert_time(start_date)
	converted_end_date = convert_time(end_date)
	seconds_elapsed= calculate_break_time(time_interval)	
	formatted_start_dates = []
	while(converted_start_date <= convert_time(end_date)):
		formatted_start_dates.append(parse_datetime(converted_start_date))
		converted_start_date = converted_start_date + timedelta(seconds=seconds_elapsed)
		if converted_start_date>=convert_time(end_date):
			break
	formatted_start_dates.append(parse_datetime(converted_end_date))
	return formatted_start_dates


rest_call_latest_frequency("Manhattan")	
#rest_call_annual_data("Manhattan","day","20160101000000", "20170101000000")
#rest_call_average_temperature("Manhattan","day","20180101000000", "20190101000000", "TEMP10MAVG", "TEMP2MAVG")
#rest_call_frequency_calculate("Manhattan","hour","20180101000000", "20180102000000", "TEMP10MAVG", "TEMP2MAVG")



