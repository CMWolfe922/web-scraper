
import csv
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import itertools as it
from loguru import logger
import time
import humanize
import os.path

#####################################################################################
# GLOBAL VARIABLES:
#####################################################################################
# Move the CSV file and the logger
# this is where any files or directories/path variables go:
CSV_FILE = './meetings.csv'
NEW_CSV_FILE = './meeting_details.csv'
HEADERS = ["name", 'address', 'city', 'state',
           'zip_code', 'day', 'time', 'info']

#####################################################################################
# Data extraction functions:
#####################################################################################

def get_csv_column_data(csv_name, column):
    df = pd.read_csv(csv_name)
    return df[column][1:]


def fetch_soup_data(link):
    """
    Basic function that takes a link from link_list and accepts it as an argument,
    then uses the requests.get method to return an html page. Then uses BeautifulSoup
    to parse the pages' text using lxml
    """
    # STEP 1: Get the webpage response obj from requests
    page = requests.get(link)
    # STEP 2: Get Soup object for html parsing
    soup = bs(page.text, "lxml")
    logger.info("got soup data for link: {}", link)
    return soup


def chunk_list(data_list:list, size:int=250):
    """
    :: break the link list up into chunks of 250 links each ::
    """
    chunked_list = [data_list[i:i + size] for i in range(0, len(data_list), size)]
    chunked_list_size = len(chunked_list)
    logger.info("[+] List was broken up into {} smaller lists.", chunked_list_size)
    return chunked_list

#####################################################################################
# The data cleaner functions. They grab the needed data from the soup data:
#####################################################################################

# CREATE A FUNCTION THAT WILL EXTRACT ADDRESS DATA FROM EACH LINK IN
# LINK LIST:
def get_address_data(soup):
    """
    :description: Extracts the address data from a soup object that gets past to it in a
    for loop.

    :param soup: This is a BeautifulSoup object that has been pulled from a soup_data list that was
    created using the fetch_soup_data function and stored into a soup_data list.

    :returns: A dictionary containing the address data components: {address, name, city, state}

    ::: I need to figure out how to add zip_code to this :::
    """
    try:
        address_tag = soup.address
        address = address_tag.contents[1]

        meeting_name = soup.find(
            'div', class_='fui-card-body').find(class_='weight-300')
        name = meeting_name.contents[1]

        city_tag = meeting_name.find_next('a')
        city = city_tag.contents[0]

        state_tag = city_tag.find_next('a')
        state = state_tag.contents[0]

        zip_tag = state_tag.find_next('a')
        zip_code = zip_tag.contents[0]

        logger.info("[+] Address data retrieved")
        return {'name': name, 'address': address, 'city': city, 'state': state, 'zip_code': zip_code}

    except IndexError as ie:
        logger.error("[-] UnboundError occured {} ", ie)
        try:
            return {'name': name, 'address': address, 'city': city, 'state': state, 'zip_code': '00000'}
        except UnboundLocalError as ule:
            logger.error("[-] UnboundLocalError occured: (zip_code not found) {} ", ule)
        try:
            return {'name': name, 'address': address, 'city': city, 'state': 'state', 'zip_code': zip_code}
        except UnboundLocalError as ule:
            logger.error("[-] UnboundLocalError occured: (state not found) {} ", ule)
        try:
            return {'name': name, 'address': address, 'city': 'city', 'state': state, 'zip_code': zip_code}
        except UnboundLocalError as ule:
            logger.error("[-] UnboundError occured: (city not found) {} ", ule)
        try:
            return {'name': name, 'address': 'address', 'city': city, 'state': state, 'zip_code': zip_code}
        except UnboundLocalError as ule:
            logger.error("[-] UnboundError occured: (address not found) {} ", ule)
        try:
            return {'name': 'name', 'address': address, 'city': city, 'state': state, 'zip_code': zip_code}
        except UnboundLocalError as ule:
            logger.error("[-] UnboundError occured: (name not found) {} ", ule)


# CREATE A FUNCTION THAT WILL EXTRACT ALL THE TABLE DATA FROM EACH LINK
# IN THE LINK LIST. THE TABLE DATA WILL THEN NEED TO BE PARSED AND
# CLEANED IF THERE ARE MULTIPLE ITEMS:
def get_table_data(soup):
    """
    :description: Extracts the meeting details data from a soup object that gets past to it in a
    for loop. The data is extracted from an html table. Each row that returns a list is joined together to make
    one string so it can be saved to a csv file.

    :param soup: This is a BeautifulSoup object that has been pulled from a soup_data list that was
    created using the fetch_soup_data function and stored into a soup_data list.

    :returns: a dictionary with the days the meeting runs, the time, and info about the meeting:
    {day, time, info}
    """
    try:
        info_table = soup.find('table', class_='table fui-table')
        # obtain all the columns from <th>
        headers = []
        for i in info_table.find_all('th'):
            title = i.text
            headers.append(title.lower())

            # now create a dataframe:
        df = pd.DataFrame(columns=headers)

        # Now create the foor loop to fill dataframe
        # a row is under the <tr> tags and data under the <td> tags
        for j in info_table.find_all('tr')[1:]:
            # if info_table.find_all('tr')[1:] == AttributeError.NoneType:
            #     print("No info table found")
            row_data = j.find_all('td')
            row = [i.text for i in row_data]
            length = len(df)
            df.loc[length] = row

        # data['day'].append(df['day'].to_list())
        # data['time'].append(df['time'].to_list())
        # data['info'].append(df['info'].to_list())
        day = df['day'].to_list()
        time = df['time'].to_list()
        info = df['info'].to_list()

        logger.info("[+] Meeting Details Retrieved")
        # now return data
        return {'day': day, 'time': time, 'info': info}

    except AttributeError as ae:
        logger.error("info_table.find_all('tr') failed: {}", ae)
        return {'day': 'day', 'time': 'time', 'info': 'info'}


def row_parser(item0, item1):
    """
    :param item0: This is the address data in a dictionary. Use the following keys to access
    the data -> Keys: 'name' - 'address' - 'city' - 'state'
    :param item1: This is the meeting details data in a dictionary. Use the following keys to
    access the data -> Keys: 'day' - 'time' - 'info'

    create a final dictionary that will be used to store the information in the database as one row.
    I will need to join the list items to create one string with a | seperating each item so I can
    split the string when retrieving the data.
    """
    row = []
    try:
        row.append(item0['name'])
        row.append(item0['address'])
        row.append(item0['city'])
        row.append(item0['state'])
        row.append(item0['zip_code'])
        logger.info("[+] Row Data Parsed")
    except Exception as e:
        logger.error("[-] Row Data Raised Exception: {}", e)
        print(e)
        row['name'] = 'name'
        row['address'] = 'address'
        row['city'] = 'city'
        row['state'] = 'state'

    try:
        row.append('|'.join(item1['day']))
        row.append('|'.join(item1['time']))
        row.append('|'.join(item1['info']))
    except Exception as e:
        logger.error("[-] Row Data Raised Exception: {}", e)

    # now return the row data dictionary

    return row


def csv_writer(row_data, csv_file, headers=None):
    with open(csv_file, 'a') as f:
        if headers is not None:
            writer = csv.writer(f, delimiter='|')
            for row in row_data:
                writer.writerow(row)
        else:
            writer = csv.writer(f, delimiter='|')
            for row in row_data:
                writer.writerow(row)

#####################################################################################


# whole list of links
links = get_csv_column_data(CSV_FILE, 'link')

if __name__ == "__main__":
    chunks = chunk_list(links)
    for chunk in chunks:
        for link in chunk:
            print(link)