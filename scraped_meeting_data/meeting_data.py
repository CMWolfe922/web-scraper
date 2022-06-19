import csv
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
# import itertools as it
from loguru import logger
import time
import humanize
# Move the CSV file and the logger
# this is where any files or directories/path variables go:
csv_filename = './meetings.csv'


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

        meeting_name = soup.find('div', class_='fui-card-body').find(class_='weight-300')
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
            return {'name': name, 'address': address, 'city': city, 'state': 'state'}
        except UnboundLocalError as ule:
            logger.error("[-] UnboundLocalError occured: {} ", ule)
        try:
            return {'name': name, 'address': address, 'city': 'city', 'state': state}
        except UnboundLocalError as ule:
            logger.error("[-] UnboundError occured {} ", ule)
        try:
            return {'name': name, 'address': 'address', 'city': city, 'state': state}
        except UnboundLocalError as ule:
            logger.error("[-] UnboundError occured {} ", ule)
        try:
            return {'name': 'name', 'address': address, 'city': city, 'state': state}
        except UnboundLocalError as ule:
            logger.error("[-] UnboundError occured {} ", ule)


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

def parse_dicts(item0, item1):
    """
    :param item0: This is the address data in a dictionary. Use the following keys to access
    the data -> Keys: 'name' - 'address' - 'city' - 'state' 
    :param item1: This is the meeting details data in a dictionary. Use the following keys to
    access the data -> Keys: 'day' - 'time' - 'info'
    
    create a final dictionary that will be used to store the information in the database as one row. 
    I will need to join the list items to create one string with a | seperating each item so I can 
    split the string when retrieving the data.
    """
    row = {'name': [], 'address': [], 'city': [], 'state': [], 'zip_code': [], 'day': [], 'time': [], 'info': []}
    try:

        try:
            row['name'].append(item0['name'])
            row['address'].append(item0['address'])
            row['city'].append(item0['city'])
            row['state'].append(item0['state'])
            row['zip_code'].append(item0['zip_code'])
        except Exception as e:
            logger.error("[-] Row Data Raised Exception: {}", e)
            print(e)
            row['name'].append('name')
            row['address'].append('address')
            row['city'].append('city')
            row['state'].append('state')
            row['zip_code'].append('zip_code')

        # now add item1 to the row data
        row['day'].append(' | '.join(item1['day']))
        row['time'].append(' | '.join(item1['time']))
        row['info'].append(' | '.join(item1['info']))

        logger.info("[+] Row Data Parsed")
        return row
    except Exception as e:
        logger.error("Exception Raised: {}", e)

new_csv_file = './meeting_details.csv'

#####################################################################################


# whole list of links
link_list = create_list_from_column_data(csv_filename, 'link')
edited_list = link_list[2000:]
####################################################################################
# chunk the links into bunches of 10,000
####################################################################################
link_list1 = link_list[:10000]
link_list2 = link_list[10000:20000]
link_list3 = link_list[20000:30000]
link_list4 = link_list[30000:]
# Test link list
link_list_test = link_list[:1000]
####################################################################################
# Soup List Scraper
####################################################################################


def soup_list_scraper(soup_data):
    """
    :param soup_data: This is the list of soup data that was returned by the scrape function. 

    :returns: a list of dictionaries that will get stored to the variable row since each dict 
    creates a row of data for the csv file. 
    """
    try:
        rows = {'name':[], 'address':[], 'city':[], 'state':[], 'zip_code':[], 'day':[], 'time':[], 'info':[]}
        for soup in soup_data:
            # Create two dicts with the following keys
            address_dict = get_address_data(soup)
            details_dict = get_table_data(soup)
            logger.info("[+] Address and table data parsed")
            d = [address_dict, details_dict]
            row_data = parse_dicts(d[0], d[1])
            rows['name'].append(row_data['name'])
            rows['address'].append(row_data['address'])
            rows['city'].append(row_data['city'])
            rows['state'].append(row_data['state'])
            rows['zip_code'].append(row_data['zip_code'])
            rows['day'].append(row_data['day'])
            rows['time'].append(row_data['time'])
            rows['info'].append(row_data['info'])

        logger.info("++++++++ SCRAPED SCRAPED BATCH OF LINKS +++++++++ ")
        return rows

    except IndexError as ie:
        logger.error("{}: List Exhausted. No more Soup Items", ie)

    except Exception as e:
        logger.error("{}: Exception raised", e)
        
####################################################################################
# Now create the same logic above in the if __name__ == '__main__':
####################################################################################
def scrape(link_list):
    """
    :param link_list: A list of links to scrape and get the soup data from the site, 
    parse the data and append the soup data to the soup_data list. 
    """
    # Two empty lists. One for soup_data and another to store row_data
    soup_data = []
    # The headers for the csv_file
    headers = ["name", 'address', 'city', 'state',
               'zip_code', 'day', 'time', 'info']
    try:
        count = 0
        for link in link_list:
            soup = fetch_soup_data(link)
            soup_data.append(soup)
            logger.info(
                "[+] {} scraped successfully: Link number {}", link, count)
            count += 1
            if count % 1000 == 0:
                time.sleep(5)
                # Every 1000 links, write the row data to the new CSV file
                rows = soup_list_scraper(soup_data)
                row_df = pd.DataFrame.from_dict(rows)
                row_df.to_csv(new_csv_file, mode='a', sep="|", index=False)
                soup_data.clear()
                logger.info("[+] Count is divisible by 1000:{} | Writing ROW_DATA to [csv_file] | soup_data and row_data cleared!", count)

                print(row_df)
        logger.info("<<<<<<<<<<<<<<< SUCCESS >>>>>>>>>>>>>>>>")
    except IndexError as e:
        logger.error("{}: List Exhausted. No more links to scrape.", e)

if __name__ == '__main__':
    start = time.time()
    new_csv_filename = './meeting_details.csv'

    # Build the log file:
    log_file_path = './data/meeting_scraper.log'
    rotation = "100 MB"
    logger.add(log_file_path, rotation=rotation, level="INFO",
               format="[<green>{time: MMM D YYYY HH:mm:ss:SSSS}</>] | <level>{message}</>", backtrace=True, diagnose=True)

    try:
        scrape(link_list)
        end = time.time()
        program_timer = humanize.naturaltime((end - start))
        logger.info(
            "<<<<<<<<<<<<<<< test_link_list: SUCCESS: PROGRAM STARTED {} >>>>>>>>>>>>>>>>", program_timer)
    except IndexError as e:
        logger.error("{}: List Exhausted. No more links to scrape.", e)
