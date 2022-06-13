import csv
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import itertools as it
from loguru import logger
import time

# Move the CSV file and the logger
# this is where any files or directories/path variables go:
csv_filename = './meetings.csv'


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

        meeting_name = soup.find(
            'div', class_='fui-card-body').find(class_='weight-300')
        name = meeting_name.contents[1]

        city_tag = meeting_name.find_next('a')
        city = city_tag.contents[0]

        state_tag = city_tag.find_next('a')
        state = state_tag.contents[0]
        logger.info("[+] Address data retrieved")
        return {'name': name, 'address': address, 'city': city, 'state': state}

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
    row = {}
    try:
        row['name'] = item0['name']
        row['address'] = item0['address']
        row['city'] = item0['city']
        row['state'] = item0['state']
        row['zip_code'] = ''
        logger.info("[+] Row Data Parsed")
    except Exception as e:
        logger.error("[-] Row Data Raised Exception: {}", e)
        print(e)
        row['name'] = 'name'
        row['address'] = 'address'
        row['city'] = 'city'
        row['state'] = 'state'

    # now add item1 to the row data
    row['day'] = ' | '.join(item1['day'])
    row['time'] = ' | '.join(item1['time'])
    row['info'] = ' | '.join(item1['info'])

    # now return the row data dictionary

    return row


new_csv_file = './meeting_details.csv'
headers = ["name", 'address', 'city', 'state',
           'zip_code', 'day', 'time', 'info']


def csv_writer(row_data, csv_filename, headers=None):
    with open(csv_filename, 'a') as f:
        if headers is not None:
            writer = csv.DictWriter(f, fieldnames=headers, delimiter='|')
            # writer.writeheader(headers)
            for row in row_data:
                writer.writerow(row)
        else:
            # fieldnames = [k for k in row_data.keys()]
            # writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='|')
            # writer.writeheader(fieldnames)
            writer = csv.DictWriter(f, fieldnames=headers, delimiter='|')
            for row in row_data:
                writer.writerow(row)

#####################################################################################


# whole list of links
link_list = create_list_from_column_data(csv_filename, 'link')

####################################################################################
# chunk the links into bunches of 10,000
####################################################################################
link_list1 = link_list[:10000]
link_list2 = link_list[10000:20000]
link_list3 = link_list[20000:30000]
link_list4 = link_list[30000:]
####################################################################################
# Single Soup Scraper for
####################################################################################


def single_soup_scraper(soup):
    """
    :param soup_data: This is the list of soup data that was returned by the scrape function.

    :returns: a list of dictionaries that will get stored to the variable row since each dict
    creates a row of data for the csv file.
    """
    try:
        # Create two dicts with the following keys
        address_dict = get_address_data(soup)
        details_dict = get_table_data(soup)
        d = [address_dict, details_dict]
        row = row_parser(d[0], d[1])
        logger.info(
            "[+] Parsed Address and Table Data | Row [{}] Created", row)
        return row

    except IndexError as ie:
        logger.error("{}: List Exhausted. No more Soup Items", ie)

    except Exception as e:
        logger.error("{}: Exception raised", e)

####################################################################################
# Now create the same logic above in the if __name__ == '__main__':
####################################################################################


if __name__ == '__main__':
    new_csv_filename = './meeting_details.csv'

    # Build the log file:
    log_file_path = './data/meeting_scraper.log'
    rotation = "100 MB"
    logger.add(log_file_path, rotation=rotation, level="INFO",
               format="[<green>{time: MMM D YYYY HH:mm:ss:SSSS}</>] | <level>{message}</>", backtrace=True, diagnose=True)

    ##############################################################################
    # Two empty lists. One for soup_data and another to store row_data
    row_data = []
    soup_data = []
    # The headers for the csv_file
    headers = ["name", 'address', 'city', 'state',
               'zip_code', 'day', 'time', 'info']
    try:
        count = 0
        # Scrape Link List # 2:
        for link in link_list2:
            soup = fetch_soup_data(link)
            soup_data.append(soup)
            logger.info(
                "[+] {} scraped successfully: Link number {}", link, count)
            count += 1
            if count % 500 == 0:
                time.sleep(5)
                # Every 500 links, write the row data to the new CSV file
                for soup in soup_data:
                    row = single_soup_scraper(soup)
                    row_data.append(row)
                # check that row_data has 500 items:
                    if len(row_data) == 500:
                        # after each soup item is parsed and the results appended to row_data, append row data to csv
                        csv_writer(row_data, new_csv_filename, headers)
                        # Then clear both soup and row data lists
                        soup_data.clear()
                        row_data.clear()
                        # log the success of the script
                        logger.info(
                            "[+] Count is divisible by 500:{} | Writing ROW_DATA to [{}] | soup_data and row_data cleared!", count, new_csv_filename)
        logger.info("<<<<<<<<<<<<<<< LINK_LIST2 SUCCESS >>>>>>>>>>>>>>>>")
    except IndexError as e:
        logger.error("{}: List Exhausted. No more links to scrape.", e)
