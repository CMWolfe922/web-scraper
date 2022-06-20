from geopy.geocoders import Nominatim
import pandas as pd
import csv
from collections import deque
from loguru import logger
import time

# csv file
csv_file = './meetings.csv'


# Function to access csv file data:
def create_list_from_column_data(csv_file, column):
    """
    :description: Create a list from a CSV column's data. To do this I will use the with open()
    context manager and open the csv file that was passed to this function as an argument.
    ----------------------------------------------------------------------------------------------------
    :param csv_file:-> This is the name of the CSV file containing the column data I want to extract
    to create a list.
    :param column:-> This is the column name or number to extract data from in the CSV file.
    ----------------------------------------------------------------------------------------------------
    :return:-> A list of strings/integers/float/datetypes from a CSV file.
    """
    # now create an empty list to append data to:
    data_list = []
    with open(csv_file, 'r') as f:
        csv_reader = csv.reader(f)
        _column = next(csv_reader)
        column_index = _column.index(column)
        # loop through CSV file and append to address_list
        for line in csv_reader:
            all_data = line[column_index]
            data_list.append(all_data)
    return data_list


# Clean the address data from csv_file
def extract_clean_address(addresses):
    # USE EMAIL FOR FREE MAPS API
    geolocator = Nominatim(user_agent="sobering")
    location = geolocator.geocode(addresses)
    return location.address


if __name__ == '__main__':
    start = time.time()
    # Build the log file:
    log_file_path = './data/address_cleaner.log'
    rotation = "10 MB"
    logger.add(log_file_path, rotation=rotation, level="INFO",
               format="[<green>{time: MMM D YYYY HH:mm:ss.SS}</>] | {file} took {elapsed} to execute | <level>{message}</>", backtrace=True,
               diagnose=True)
    name_list = create_list_from_column_data(csv_file, 'name')
    address_list = create_list_from_column_data(csv_file, 'address')
    nq = deque(name_list)
    aq = deque(address_list)
    count = 0
    try:
        while aq:
            try:
                address = aq.popleft()
                name = nq.popleft()
                cleaned_address = extract_clean_address(address)
                logger.info("<blue>[+] {} address cleaned: [{}]</> | <yellow>Index: [{}]</>", name, cleaned_address, count)
                count += 1

            except Exception as e:
                address = aq.popleft()
                name = nq.popleft()
                logger.error("<red>[-] {}'s address: [{}] NOT CLEANED</> | <yellow>Index: [{}]</>", name, address, count)
                count += 1

        end = time.time()
        timer = (end - start) / 60
        logger.success("<<<<<<<<<< Program Completed in {} minutes >>>>>>>>>>", timer)
    except StopIteration as si:
        logger.error("<red>[-] Queue has been exhausted</>")
    except Exception as e:
        logger.error("<red>Exception Raised: {}</> @ <yellow>Index: [{}]</>", e, count)
    # messy_addresses = pd.DataFrame(address_list)
    # messy_addresses['cleaned_addresses'] = messy_addresses.apply(lambda x: extract_clean_address(x[0]), axis=1)
    # print(messy_addresses['cleaned_addresses'])
