import aiohttp
import asyncio
import async_timeout
from bs4 import BeautifulSoup as bs 
from collections import Counter 
import re 
from urllib.parse import urlparse
import time 
import pandas as pd 
import csv, requests
from loguru import logger
import humanize
import os.path

# ================================================================ #
# Put all the files or directories/path variables below:
# ================================================================ #
CSV_FILE = './meetings.csv'
LOG_FILE = './data/meetings.log'
NEW_CSV_FILE = './meeting_details.csv'


# ================================================================ #
# Setup the logger and get it ready:
# ================================================================ #

rotation = "5 MB"
logger.add(LOG_FILE, rotation=rotation, level="INFO",
               format="[<green>{time: MMM D YYYY HH:mm:ss:SSSS}</>] | <level>{message}</>", backtrace=True, diagnose=True)

# ================================================================ #
# Create Function to access the links in meetings csv file:
# ================================================================ #

def get_csv_column_data(csv_file, column):
    df = pd.read_csv(csv_file)
    return df[column][1:]

def chunk_list(data_list:list, size:int=250):
    """
    :: break the link list up into chunks of 250 links each ::
    """
    chunked_list = [data_list[i:i + size] for i in range(0, len(data_list), size)]
    chunked_list_size = len(chunked_list)
    logger.info("[+] List was broken up into {} smaller lists.", chunked_list_size)
    return chunked_list

# ================================================================ #
# Create async web scraping functions:
# ================================================================ #

async def fetch_link(session, link):
	async with async_timeout.timeout(10):
		async with session.get(link) as response:
			return await response.text()


# ================================================================ #
# Create async soup data fetcher:
# ================================================================ #

async def fetch_soup(html, display_result=False):
	soup = bs(html, 'lxml')
	if display_result:
		print(soup.prettify())
	return soup

# ================================================================ #
# Create the async function that extracts the text data needed:
# ================================================================ #

async def extract_address_data(html):
	"""
	:description: Extracts the address data from a soup object that gets past to it in a
	for loop.

	:param soup: This is a BeautifulSoup object that has been pulled from a soup_data list that was
	created using the fetch_soup_data function and stored into a soup_data list.

	:returns: A dictionary containing the address data components: {address, name, city, state}

	::: I need to figure out how to add zip_code to this :::
	"""
	try:
		soup = await fetch_soup(html)
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

async def extract_table_data(html):
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
		soup = await fetch_soup(html)
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
			# print("No info table found")
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

async def row_parser(item0, item1):
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

# ================================================================ #
# This is the main scrape function that scrapes data from a link:
# ================================================================ #

async def scrape(link):
	async with aiohttp.ClientSession() as session:
		parsed_url = urlparse(link)
		root_domain = parsed_url.netloc
		domain = parsed_url.geturl()
		html = await fetch_link(session, link)
		try:
			address_dict = await extract_address_data(html)
			details_dict = await extract_table_data(html)
			data = [address_dict, details_dict]
			row = await row_parser(data[0], data[1])
			logger.info("[+] Parsed Address and Table Data | Row [{}] Created", row)
			return row
		except IndexError as ie:
			logger.error("{}: List Exhausted. No more Soup Items", ie)

		except Exception as e:
			logger.error("{}: Exception raised", e)

# ================================================================ #
# This is the main function that contains the programs main logic:
# ================================================================ #

async def main(links:list):
	start_time = time.time()
	row_data = []
	headers = ["name", 'address', 'city', 'state', 'zip_code', 'day', 'time', 'info']
	try:
		count = 0
		for link in links:
			row = await scrape(link)
			row_data.append(row)
			logger.info("[+] {} scraped successfully: Link number {}", link, count)
			count += 1
			if count % 250 == 0:
				asyncio.sleep(2)
				if len(row_data) == 250:
					try:
						if not os.path.exists(NEW_CSV_FILE):
							df = pd.DataFrame(row_data, columns=headers)
							df.to_csv(NEW_CSV_FILE, sep='|', mode='a', index=False)
							row_data.clear()
							logger.info("[+] Count is divisible by 500:{} | Writing ROW_DATA to [{}] | row_data cleared!", count, NEW_CSV_FILE)
						else:
							df = pd.DataFrame(row_data, columns=headers)
							df.to_csv(NEW_CSV_FILE, sep='|', mode='a', index=False)
							row_data.clear()
							logger.info("[+] Count is divisible by 500:{} | Writing ROW_DATA to [{}] | row_data cleared!", count, NEW_CSV_FILE)
					except TypeError as te:
						logger.error("TypeError Raised: {}", te)
		end_time = time.time()
		finish = (end_time - start_time)
		program_run_time = humanize.naturaltime(finish)
		logger.success("<<<<<<<<<< Program Executed Successfully. Program Run Time: {} >>>>>>>>>> ", program_run_time)
	except IndexError as e:
		logger.error("{}: List Exhausted, no more links..", e)

def split(data_list, chunk_size):
	for i in range(0, len(data_list), chunk_size):
		yield data_list[i:i + chunk_size]


if __name__ == '__main__':
	links = get_csv_column_data(CSV_FILE, 'link')
	link_chunks = chunk_list(links)
	chunked = list(split(links, chunk_size=250))
	for link_list in chunked:
		soup_data = map(fetch_soup, link_list)
	for i in soup_data:
		print(i)
	# loop = asyncio.get_event_loop()
	# loop.run_until_complete(main(links[6750:]))

