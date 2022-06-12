"""
This is the main meeting scraper module file. This is where the logic will be implemented
using the least amount of nested functions. My goal is to be able to get this script to
execute one link in .2 seconds.

> This means:
1) Scrape the page, create soup_data and return it.
2) Parse the soup_data and create two dictionaries. (now I know how to merge two dicts)
3) Use the row_parser function (or logic) and parse the two dictionaries to create
one dictionary (each having one string value)
4) append that row to the row_data list (or use list comprehension to do 2-4)
5) Use the csv_writer function to write each row (aka dictionary in the row_data list)
to a csv file.
"""

import csv
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import itertools as it
from loguru import logger
import time

# this is where any files or directories/path variables go:

meetings_csv = './meetings.csv'

# ==================================================================================================================== #
# SETUP LOGURU'S LOGGER METHOD. USE .add() .bind() etc.
# ==================================================================================================================== #
log_file_path = './data/meeting_scraper.log'
rotation = "100 MB"
logger_format = "[<green>{time: MMM D YYYY HH:mm:ss:SSSS}</>] | <level>{message}</>"
logger.add(log_file_path, rotation=rotation, level="INFO", format=logger_format, backtrace=True, diagnose=True)


# ==================================================================================================================== #
# SETUP SCRAPER FUNCTIONS: only the funcs that can be used again somewhere else.
# ==================================================================================================================== #
# Func to retrieve csv data from a specific column
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
        column_index = _column.index(column)
        # loop through CSV file and append to address_list
        for line in csv_reader:
            all_data = line[column_index]
            data_list.append(all_data)
    return data_list


# func to retrieve soup data from a specific link:
def fetch_soup_data(link):
    """
    :param link:-> Link of site that you want to scrape and parse the site data using BeautifulSoup.
    For this module, this link is from the create_list_from_column_data function.

    :return link_list:
    """
    # STEP 1: Get the webpage response obj from requests
    page = requests.get(link)
    # STEP 2: Get Soup object for html parsing
    soup = bs(page.text, "lxml")
    logger.info("Retrieved soup_data for link: {}", link)
    return soup


# ==================================================================================================================== #
# CREATE A BUNCH OF LINK LISTS CONTAINING 10,000 LINKS EACH
# ==================================================================================================================== #
# get a list of the links from meetings_csv
link_list = create_list_from_column_data(meetings_csv, 'link')

# link_list1 = link_list[:10000]
# link_list2 = link_list[10000:20000]
# link_list3 = link_list[20000:30000]
# link_list4 = link_list[30000:]

# Create shortened lists to test with:
# first 100
links_100 = link_list[:100]
# first 500
links_500 = link_list[:500]
# first 1000
links_1000 = link_list[:1000]


# ==================================================================================================================== #
# THIS IS WHERE THE MODULE LOGIC GOES if __name__ == '__main__':
# ==================================================================================================================== #
if __name__ == '__main__':
    try:
        soup_data = map(fetch_soup_data, links_100)
        if len(soup_data) == 100:
            logger.info("[+] map function worked on fetch_soup_data!")

    except Exception as e:
        logger.error("[-] Base Exception Raised on map function: {}", e)
        try:
            soup_data = [fetch_soup_data(link) for link in links_100]
            if len(soup_data) == 100:
                logger.info("[+] List Comprehension worked on fetch_soup_data!")
        except Exception as e:
            logger.error("[-] Base Exception Raised on list comprehension: {}", e)

    finally:
        if len(soup_data) > 10:
            print(soup_data)
            logger.info("+++++++++++ Soup Data Retrieved: +++++++++++")
        else:
            logger.info("<<<<<<<<<< Neither Attempt Worked >>>>>>>>>>>")
