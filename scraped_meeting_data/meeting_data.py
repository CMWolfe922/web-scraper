import sqlite3 as sql
import csv
import json
import re
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import lxml


def csv_parser(csv_reader, header: str):
    _header = next(csv_reader)
    headerIndex = _header.index(header)

    # now create an empty list to append the addresses to
    data_list = []

    # loop through CSV file and append to address_list
    for line in csv_reader:
        all_data = line[headerIndex]
        data_list.append(all_data)
    return data_list


csv_filename = 'scraped_meeting_data/meetings.csv'
states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}
address_ending_strings = ['Ave', 'Blvd', 'Street', 'Dr',
                          'Ln', 'Rd', 'Road', 'Highway', 'Hwy', 'Pkwy', 'St']


def meeting_data_scraper(link):
    data = {'name': [], 'address': [], 'city': [], 'state': [], 'zip_code': [
    ], 'details': {'schedule': {'day': [], 'time': [], 'info': []}}}
    # get the requests object from the link
    page = requests.get(link)
    soup = bs(page.text, "lxml")

    def get_address_data(soup, data):
        address_tag = soup.address
        data['address'].append(address_tag.contents[1])
        meeting_name = soup.find(
            'div', class_='fui-card-body').find(class_='weight-300')
        data['name'].append(meeting_name.contents[1])
        city_tag = meeting_name.find_next('a')
        data['city'].append(city_tag.contents[0])
        state_tag = city_tag.find_next('a')
        data['state'].append(state_tag.contents[0])
        return data

    get_address_data(soup, data)

    def get_table_data(soup, data):
        info_table = soup.find('table', class_='table fui-table')
        # obtain all the columns from <th>
        headers = []
        for i in info_table.find_all('th'):
            title = i.text
            headers.append(title.lower())

            # now create a dataframe:
        table_data = pd.DataFrame(columns=headers)

        # Now create the foor loop to fill dataframe
        # a row is under the <tr> tags and data under the <td> tags
        for j in info_table.find_all('tr')[1:]:
            row_data = j.find_all('td')
            row = [i.text for i in row_data]
            length = len(table_data)
            table_data.loc[length] = row

        print(table_data)

    get_table_data(soup, data)


csv_filename = 'scraped_meeting_data/meetings.csv'
states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}
address_ending_strings = ['Ave', 'Blvd', 'Street', 'Dr',
                          'Ln', 'Rd', 'Road', 'Highway', 'Hwy', 'Pkwy', 'St']

with open(csv_filename, 'r') as f:
    csv_reader = csv.reader(f)
    link_list = csv_parser(csv_reader, 'link')

meeting_data_scraper(link_list[4])
