import zomatopy
import json
import pandas as pd


def display_response(df):
	response = ''
	if df.count() != 0 :
		response = "Showing you top rated restaurants:" + "\n"
		for index, row in df.iterrows():
			if index < 5:
				response = response + "\t" + row['Name'] + " With Address: " + row['Address'] + " . Average price for 2 people is: " + str(row['Average_cost']) + "\n"
	return (response)

def email_response(df):
	response = ''
	if df.count() != 0 :
		for index, row in df.iterrows():
			if index < 10:
				response = response + row['Name'] + " " + row['Address'] + " " + str(row['Ratings']) + " " + str(row['Average_cost']) + "\n"
	return (response)
		

f = open('tier_1.txt', 'r+')
tier_1 = f.read().lower()
tier_1 = tier_1.split(', ')
f = open('tier_2.txt', 'r+')
tier_2 = f.read().lower()
tier_2 = tier_2.split(', ')

config={ "user_key":"8f026e381186d0b58ad18fb4f2d75a88"}
zomato = zomatopy.initialize_app(config)
loc = 'london'#tracker.get_slot('location')
cuisine = 'chinese'#tracker.get_slot('cuisine')
average_cost = 'Lesser than Rs. 300'#tracker.get_slot('cuisine')

response = 'We do not operate in that area yet.'
if (loc in tier_1) | (loc in tier_2):
	location_detail=zomato.get_location(loc, 1)
	d1 = json.loads(location_detail)
	lat=d1["location_suggestions"][0]["latitude"]
	lon=d1["location_suggestions"][0]["longitude"]
	cuisines_dict={'bakery':5,'chinese':25,'cafe':30,'italian':55,'biryani':7,'north indian':50,'south indian':85}
	results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 1000)

	d = json.loads(results)
	response = []
	if d['results_found'] == 0:
		response= "no results"
	else:
		for restaurant in d['restaurants']:
			#print(restaurant['restaurant']['user_rating']['aggregate_rating'])
			data = (restaurant['restaurant']['name'], restaurant['restaurant']['location']['address'], restaurant['restaurant']['user_rating']['aggregate_rating'], restaurant['restaurant']['average_cost_for_two'])
			response.append(data)

	#df = pd.DataFrame(data,columns=['Name','Address', 'Ratings', 'Average_cost'])
	labels = ['Name', 'Address', 'Ratings', 'Average_cost']
	df = pd.DataFrame.from_records(response, columns=labels)

	if average_cost == 'Lesser than Rs. 300':
		df = df.loc[df['Average_cost'] < 300]
	elif average_cost == 'Rs. 300 to 700':
		df = df.loc[(df['Average_cost'] >= 300) & (df['Average_cost'] <= 700)]
	else :
		df = df.loc[df['Average_cost'] > 700]

	df = df.sort_values(by='Ratings', ascending=0)

	response = ''
	#for index, row in df.iterrows():
	#	response = response + row['Name'] + " " + row['Address'] + " " + str(row['Ratings']) + " " + str(row['Average_cost']) + "\n"
	response = display_response(df)
	if response == '':
		response = 'No Restaurants found for this criteria'


print(response)