from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as bs
import os
from dotenv import load_dotenv

load_dotenv()
LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def open_firefox():
	driver = webdriver.Firefox()

def login_to_linkedin(driver):
	# Webpage to automate
	driver.get("https://www.linkedin.com/home")
	# get the page title
	title = driver.title

	# make the driver wait 5 seconds
	driver.implicitly_wait(5)

	# Create a text_box element
	user_name = driver.find_element(by=By.ID, value="session_key")
	password = driver.find_element(by=By.ID, value="session_password")

	# Create a submit_button element
	submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button.btn-md:nth-child(3)")

	# send username and password to the text boxes
	user_name.send_keys(LINKEDIN_USERNAME)
	time.sleep(1)
	password.send_keys(LINKEDIN_PASSWORD)
	time.sleep(2)

	# Submit the form submit button
	submit_button.click()

if __name__ == "__main__":

	# Which driver to use
	driver = webdriver.Firefox()

	# login function
	login_to_linkedin(driver)

	# NOW I NEED TO GET DATA FROM THE LINKED IN PAGE:
	# (I can use BeautifulSoup for this)
	soup = driver.to_soup()
	print(soup.parse_html())

	# Get the message after the click
	# text = text_box.text
	time.sleep(3)
	# Close the driver out
	driver.quit()