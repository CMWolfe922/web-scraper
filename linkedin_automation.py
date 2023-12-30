from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
from bs4 import BeautifulSoup as bs
import os
from loguru import logger
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
    # setting up logging
	PATH = "./tmp/"
	FILE = __file__.split('/')[-1] + ".log"
	LOG_FILE = os.path.join(PATH, FILE)

	logger.add(LOG_FILE, format="{time:MM/DD/YYYY at HH:mm:ss} | {level} | {name} | {message}", diagnose=True, backtrace=True)

	# Check if the system is running on Windows or Linux
	try:
		# Extract data from the feed page and do something with it
		title = "//h1[@class='main-heading text-color-text-accent-2 babybear:pb-[24px]']"
		impressions = "//span[normalize-space()='410']"
		reposts = "button[id='ember1208'] span[aria-hidden='true']"
		post_title = "body > div:nth-child(65) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > main:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1)"
		followers = "body > div:nth-child(65) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > main:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > span:nth-child(2) > span:nth-child(1)"
		main_image = "/html[1]/body[1]/div[5]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/a[1]/span[1]/div[1]/div[1]/img[1]"
		post_image = "/html[1]/body[1]/div[5]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/div[1]/a[1]/div[1]/div[1]/img[1]"
		submissions = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/div[4]/div/div[1]/div[2]/div/div/div/div/div/div/article/div/div[2]/div/a/div/div/div/div/span"
		post_comments = "/html[1]/body[1]/div[5]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[7]/div[1]/div[1]/div[1]/ul[1]/li[2]/button[1]/span[1]"
		
		if os.name == 'nt':
			logger.info("Running on Windows")

			# Set up headless Firefox
			driver = webdriver.Firefox()

			# login function
			url = login_to_linkedin(driver)

			data = {
			'title': driver.find_element(By.XPATH, title),
			'impressions': driver.find_element(By.XPATH, impressions),
			'reposts': driver.find_element(By.CSS_SELECTOR, reposts),
			'post_title': driver.find_element(By.CSS_SELECTOR, post_title),
			'followers': driver.find_element(By.CSS_SELECTOR, followers),
			'main_image': driver.find_element(By.XPATH, main_image),
			'post_image': driver.find_element(By.XPATH, post_image),
			'submissions': driver.find_element(By.XPATH, submissions),
			'post_comments': driver.find_element(By.XPATH, post_comments),
			}

			# NOW I NEED TO GET DATA FROM THE LINKED IN PAGE:
			# (I can use BeautifulSoup for this)
			title = bs.get(data['title'])
			print(title.text)

			# Get the message after the click
			# text = text_box.text
			time.sleep(3)
			# Close the driver out
			driver.quit()

		elif os.name == 'posix':

			logger.info("Running ona POSIX-compatiblesystem (Like Ubuntu)")
			# Set up headless Firefox
			executable_firefox = "/usr/bin/firefox"
			service = Service(executable_path=executable_firefox)
			options = FirefoxOptions()
			options.add_argument("--headless")
			driver = webdriver.Firefox(service=service, options=options)
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

	except Exception as e:
		logger.error(e.with_traceback())
