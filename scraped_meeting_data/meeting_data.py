import sqlite3 as sql
import csv
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import Pool

# TODO: CREATE FUNCTION THAT EXTRACTS LINKS FROM CSV AND RETURNS LIST:


def get_links(csv_filename):
    with open(csv_filename, 'r') as f:
        csv_reader = csv.reader(f)
        link_list = csv_parser(csv_reader, 'link')
    return link_list

# TODO: CREATE FUNCTION THAT WILL GET THE PAGE CONTENTS AND CREATE SOUP OBJ:


def fetch_soup_data(link):
    page = requests.get(link)
    soup = bs(page.text, 'lxml')
    return soup

# TODO: CREATE FUNCTION THAT WILL RETRIEVE THE ADDRESS DATA AND RETURN DICT:


def get_address_data(soup):

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
        return {'name': name, 'address': address, 'city': city, 'state': state}

    except IndexError as ie:
        print(f"Index Error: {ie}")
        try:
            return {'name': name, 'address': address, 'city': city, 'state': 'state'}
        except UnboundLocalError as ule:
            print(f"UnboundLocalError: {ule}")
        try:
            return {'name': name, 'address': address, 'city': 'city', 'state': state}
        except UnboundLocalError as ule:
            print(f"UnboundLocalError: {ule}")
        try:
            return {'name': name, 'address': 'address', 'city': city, 'state': state}
        except UnboundLocalError as ule:
            print(f"UnboundLocalError: {ule}")
        try:
            return {'name': 'name', 'address': address, 'city': city, 'state': state}
        except UnboundLocalError as ule:
            print(f"UnboundLocalError: {ule}")

# TODO: CREATE FUNCTION THAT WILL RETRIEVE THE DETAILS DATA FROM AN HTML TABLE:


def get_table_data(soup):
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

        # now return data
        return {'day': day, 'time': time, 'info': info}

    except AttributeError as ae:
        print(f"info_table.find_all('tr')[1:] raised error: {ae}")
        return {'day': 'day', 'time': 'time', 'info': 'info'}

# TODO: PASS THOSE TWO DICTS TO A FUNCTION THAT WILL PARSE AND COMBINE THEM:


def meeting_row_parser(item0, item1):
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
    except Exception as e:
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

# TODO: CREATE A FUNCTION THAT WILL WRITE EACH ITEM IN THE ROW_DATA LIST TO A CSV FILE
# SAVING THE ROW VALUES IN THEIR KEY'S COLUMN:


def convert_row_data_to_csv(row_data):
    with open('meeting_details.csv', 'w') as csvfile:
        for d in row_data:
            csvwriter = csv.DictWriter(
                csvfile, delimiter=',', field_names=list(d.keys()))
            csvwriter.writerow(d)


# TODO: CREATE A MULTIPROCESSING POOL OBJECT WITH 60 WORKERS:
pool = Pool(60)

# -------------------------------------------------------------------------------- #
# OLD CODE:
# -------------------------------------------------------------------------------- #

if __name__ == "__main__":
    # program start:
    start = time.time()

    # STEP: Use the get_links function to retrieve link_list from csv
    csv_filename = './meetings.csv'
    link_list = get_links(csv_filename)

    # STEP: Use the pool.map method to fetch soup data from each link in link_list
    soup_data = pool.map(fetch_soup_data, link_list)

    # STEP: Cread a ThreadPoolExecutor with context and execute the functions used
    # to extract data from the soup_data
    with ThreadPoolExecutor(max_workers=2) as executor:
        address_data = executor.submit(pool.map(get_address_data, soup_data))
        detail_data = executor.submit(pool.map(get_table_data, soup_data))

    # Open CSV file to append data to:
    # with open('meetings.csv', 'w') as f:
    #     csv_writer = csv.DictWriter(f, field_names=list(d.keys()))

    # end of program timer
    end = time.time()
    t = end - start
    print(f"Program took: {t} seconds")
