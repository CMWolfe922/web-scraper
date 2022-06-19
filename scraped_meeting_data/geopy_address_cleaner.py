from geopy.geocoders import Nominatim
import pandas as pd
import csv

# csv file
csv_file = './csv_files/meetings.csv'

# CLEAN RAW ADDRESS DATA FROM FIRST CSV FILE:
def create_list_from_column_data(csv_filename, column):
    """
    :description: Create a list from a CSV column's data. To do this I will use the with open()
    context manager and open the csv file that was passed to this function as an argument.
    ----------------------------------------------------------------------------------------------------
    :param csv_filename:-> This is the name of the CSV file containing the column data I want to extract
    to create a list.
    :param column:-> This is the column name or number to extract data from in the CSV file.
    ----------------------------------------------------------------------------------------------------
    :return:-> A list of strings/integers/float/datetypes from a CSV file.
    """
    # now create an empty list to append data to:
    data_list = []
    with open(csv_filename, 'r') as f:
        csv_reader = csv.reader(f)
        _column = next(csv_reader)
        columnIndex = _column.index(column)
        # loop through CSV file and append to address_list
        for line in csv_reader:
            all_data = line[columnIndex]
            data_list.append(all_data)
    return data_list




# USE EMAIL FOR FREE MAPS API
geolocator = Nominatim(user_agent="cmwolfe.dev@gmail.com")

def extract_clean_address(addresses):
    try:
        location = geolocator.geocode.OpenStreetMap(addresses, api_key='GOh7tfINgq3AUEcEzj2OAL42EHrI7U4L0QuJtvvK')
        return location.address
    except:
        return ''

if __name__ == '__main__':
	address_list = create_list_from_column_data(csv_file, 'address')
	messy_addresses = pd.DataFrame(address_list)
	messy_addresses['cleaned_addresses'] = messy_addresses.apply(lambda x: extract_clean_address(x[0]) , axis =1  )
	print(messy_addresses['cleaned_addresses'])