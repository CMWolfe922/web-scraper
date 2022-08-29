import os, csv
import pandas as pd
import re

# ====================================================== #
# GLOBAL VARIABLES
# ====================================================== #
PATH = os.getcwd()
FILE_NAME = "meeting_details.csv"

FILE = os.path.join(PATH, FILE_NAME)


# ====================================================== #
# PROGRAM FUNCTIONS FOR EXTRACTING DATA:
# ====================================================== #
def sort_meeting_data(file):
	data = pd.read_csv(file, sep="|")
	data.sort_values(by=['zip_code'], inplace=True)
	return data

def display_meeting_data(df, n:int):

	name = df['name']
	address = df['address']
	city = df['city']
	state = df['state']
	zip_code = df['zip_code']
	day = df['day']
	time = df['time']
	info = df['info']

	print(name.head(n))
	print(address.head(n))
	print(city.head(n))
	print(state.head(n))
	print(zip_code.head(n))
	print(day.head(n))
	print(time.head(n))
	print(info.head(n))


if __name__ == '__main__':
	df = sort_meeting_data(FILE)
	# display_meeting_data(df, 20)
	counter = 0 
	for row in df.iterrows():
		if counter == 100:
			break
		else:
			print(row)
			counter += 1

