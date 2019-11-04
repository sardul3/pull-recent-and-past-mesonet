import requests
import time

while True:
	res = requests.get("https://api.darksky.net/forecast/132948145609a81277d9a4cdb4b9a676/39.1836,-96.5717")
	data = res.json()
	last_update = time.ctime(data["currently"]["time"])
	print(last_update)


	f = open("/home/sagar/Desktop/output.txt", "w")
	f.write("Temperature --> "+ str(data["currently"]["temperature"])+"\n")
	f.write("Summary--> "+ str(data["currently"]["summary"])+"\n")
	f.write("Humidity --> "+ str(data["currently"]["humidity"])+"\n")
	f.write("Wind Speed --> "+ str(data["currently"]["windSpeed"])+"\n")
	f.write("Last Updated --> "+last_update+"\n")

	f.close()
	time.sleep(300)











