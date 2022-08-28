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
def get_csv_data(file):
	data = pd.read_csv(file, sep="|")
	address = data['address'].head(20)
	city = data['city'].head(20)
	print(address, city)



if __name__ == '__main__':
	get_csv_data(FILE)
