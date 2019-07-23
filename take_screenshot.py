from selenium import webdriver
import pyautogui
import os
import time
import twittercreds
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import sys

driver_path = os.path.join(os.getcwd(),'chromedriver_win32', 'chromedriver.exe')

username = twittercreds.username
password = twittercreds.password

meme_path = os.path.join('C:\\Hugo\\weekinmemes\\static\\img')
tweets = pd.read_csv(sys.argv[1])

# Login

driver = webdriver.Chrome(driver_path)
driver.maximize_window()

driver.get('https://twitter.com/login')
username_field = driver.find_element_by_class_name("js-username-field")
password_field = driver.find_element_by_class_name("js-password-field")

username_field.send_keys(username)
driver.implicitly_wait(1)

password_field.send_keys(password)
driver.implicitly_wait(1)

driver.find_element_by_class_name("EdgeButtom--medium").click()
driver.implicitly_wait(2)

def take_screenshot(tweet, meme, count, isreply = 'no'):
	driver.get(tweet)
	time.sleep(3)
	img_path = f'{meme_path}/{meme}/{meme}-{i:03d}.png'
	screenshot_region = (320, 150, 590, 575)

	if isreply == 'yes':
		ActionChains(driver).move_to_element(driver.find_elements_by_tag_name('article')[1]).perform()
	else:
		ActionChains(driver).move_to_element(driver.find_element_by_tag_name('article')).perform()

	pyautogui.press('up')
	
	time.sleep(2)
	try:
		pyautogui.screenshot(imageFilename=img_path, region=screenshot_region)
	except FileNotFoundError:
		os.mkdir(os.path.join(meme_path, meme))
		pyautogui.screenshot(imageFilename=img_path, region=screenshot_region)


num_tweets = tweets.shape[0]

for i in range(num_tweets):
	meme = tweets.meme[i]
	tweet = tweets.tweet[i]
	isreply = tweets.isreply[i]
	take_screenshot(tweet, meme, i, isreply)

driver.close()

