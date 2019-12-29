from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
import instagramcreds
import os
import time
import pandas as pd

cap = DesiredCapabilities().FIREFOX

with open('do_not_unfollow.txt') as f:
	do_not_unfollow = f.read().split('\n')

def open_browser(driver_path, cap):
    driver = webdriver.Firefox(capabilities=cap, executable_path=driver_path)
    driver.maximize_window()
    return driver


def login_to_instagram(driver, username, password):
    driver.get('https://www.instagram.com/accounts/login/')
    driver.implicitly_wait(1)
    
    username_field = driver.find_element_by_name('username')
    username_field.send_keys(username)
    driver.implicitly_wait(1)
    
    password_field = driver.find_element_by_name('password')
    password_field.send_keys(password)
    driver.implicitly_wait(1)
    
    submit_button = driver.find_element_by_css_selector('button[type="submit"]')
    submit_button.click()

def unfollow_user(driver, j):
    following_link = driver.find_elements_by_xpath("//button[contains(text(), 'Following')]")[j]
    driver.implicitly_wait(1)
    following_link.click()
    unfollow_button = driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]")
    unfollow_button.click()
    time.sleep(2)
    
    #return {'timestamp': f'{timestamp}', 'action': 'Unfollow', 'account': account} 

def unfollow_bulk(driver, max_num = 10):
	log = []
	driver.get('https://www.instagram.com/weekinmemes/following')
	following_link = driver.find_element_by_css_selector('a[href="/weekinmemes/following/"]')
	driver.implicitly_wait(1)
	following_link.click()
	count = 0
	j = 0
	accounts = driver.find_elements_by_class_name('notranslate')
	while count < max_num:
		try:
			account = accounts[count].text
			if account in do_not_unfollow:
				j += 1
				count += 1
				continue
			unfollow_user(driver, j)
			timestamp = time.strftime('%Y/%m/%d %H:%M:%S')
			print('Unfollow ' + account)
			log.append({'timestamp': f'{timestamp}', 'action': 'Unfollow', 'account': account})
		except NoSuchElementException:
			return log + unfollow_bulk(driver, max_num = max_num - count)
		count += 1
	return log


driver_path = os.path.join(os.getcwd(),'geckodriver-v0.26.0-win64', 'geckodriver.exe')

driver = open_browser(driver_path, cap)

username = instagramcreds.username
password = instagramcreds.password

login_to_instagram(driver, username, password)
time.sleep(2)
log = unfollow_bulk(driver)
log_df = pd.io.json.json_normalize(log)
driver.close()

time_now = time.strftime('%Y%m%d%H%M')
log_df.to_csv(f'log_{time_now}.csv', index = False)

master_log_df = pd.read_csv('master_log.csv')

master_log_df = pd.concat([master_log_df, log_df], ignore_index=True, sort = False)
master_log_df.to_csv('master_log.csv', index = False)