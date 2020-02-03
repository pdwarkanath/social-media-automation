from selenium import webdriver
import pyautogui
import os
import time
import twittercreds
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import sys

cap = DesiredCapabilities().FIREFOX

#driver_path = os.path.join(os.getcwd(),'chromedriver_win32', 'chromedriver.exe')

driver_path = os.path.join(os.getcwd(),'geckodriver-v0.26.0-win64', 'geckodriver.exe')

username = twittercreds.username
password = twittercreds.password

meme_path = os.path.join('C:\\Hugo\\weekinmemes\\static\\img')
tweets = pd.read_csv(sys.argv[1])

# Login

driver = webdriver.Firefox(capabilities=cap, executable_path=driver_path)
driver.maximize_window()

driver.get('https://twitter.com/login')
time.sleep(3)
username_field = driver.find_element_by_name("session[username_or_email]")
password_field = driver.find_element_by_name("session[password]")

username_field.send_keys(username)
driver.implicitly_wait(1)

password_field.send_keys(password)
driver.implicitly_wait(1)

driver.find_element_by_xpath("//div[@data-testid='LoginForm_Login_Button']").click()
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

