import requests as r
from numpy import random
from bs4 import BeautifulSoup
from selenium import webdriver
import instagramcreds
import os
import json
import emoji
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd
import sys

cap = DesiredCapabilities().FIREFOX

with open('do_not_unfollow.txt') as f:
    do_not_unfollow = f.read().split('\n')

def get_hashtag_posts_urls(hashtag, max_posts = 10, top_posts = False):
    search_results = r.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
    soup = BeautifulSoup(search_results.text, 'html.parser')
    script = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
    page_json = script.text.split(' = ', 1)[1].rstrip(';')
    data = json.loads(page_json)
    
    urls = []
    if top_posts:
        posts = data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges'][:max_posts]
    else:
        posts = data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges'][:max_posts]
    for p in posts:
        shortcode = p['node']['shortcode']
        urls.append(f'https://instagram.com/p/{shortcode}')
    return urls

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

def like_post(driver, url):
    try:
        like_button = driver.find_element_by_css_selector('span[aria-label="Like"]')
    except NoSuchElementException as e:
        return
    like_button.click()
    timestamp = time.strftime('%Y/%m/%d %H:%M:%S')
    account = driver.find_element_by_class_name('notranslate').text
    return {'timestamp': f'{timestamp}', 'action': 'Like', 'account': account, 'url': url} 

def get_comment(comments, ask_to_follow = False):
    comment = emoji.emojize(random.choice(comments), use_aliases=True)
    if ask_to_follow:
        comment +=  ' Follow us for a weekly roundup of the best memes'
    return comment


def comment_on_post(driver, url, comment):
    account = driver.find_element_by_class_name('notranslate').text
    
    try:
        comment_field = driver.find_element_by_css_selector('textarea[aria-label="Add a comment…"]')
        comment_field.send_keys(f'{comment}')
    except ElementNotInteractableException as e:
        return comment_on_post(driver, url, comment)
    
    
    ActionChains(driver).move_to_element(comment_field).perform()
    time.sleep(2)
    
    submit_button = driver.find_element_by_css_selector('button[type="submit"]')
    submit_button.click()
    timestamp = time.strftime('%Y/%m/%d %H:%M:%S')
    
    return {'timestamp': f'{timestamp}', 'action': 'Comment', 'account': account, 'url': url, 'comment': comment} 

def follow_user(driver, url):
    account = driver.find_element_by_class_name('notranslate').text
    try:
        follow_button = driver.find_element_by_xpath("//button[contains(text(), 'Follow')]")
    except NoSuchElementException as e:
        return
    follow_button.click()
    timestamp = time.strftime('%Y/%m/%d %H:%M:%S')
    return {'timestamp': f'{timestamp}', 'action': 'Follow', 'account': account, 'url': url}

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

def automate_interactions(driver, urls):
    log = []
    for url in urls:
        driver.get(url)
        # Like
        to_like = random.choice([0,1])

        if to_like:
            action = like_post(driver, url)
            print(action['action'] + ' ' + action['url'] + ' by ' + action['account'])
            log.append(action)

        # Comment
        to_comment = random.choice([0,1])

        if to_comment:
            comment = get_comment(comments)
            action = comment_on_post(driver, url, comment)
            print(action['action'] + ' "' + action['comment'] + '" on ' + action['url'] + ' by ' + action['account'])
            log.append(action)

        # Follow
        to_follow = random.choice([0,1])

        if to_follow:
            action = follow_user(driver, url)
            print(action['action'] + ' ' + action['account'])
            log.append(action)

        time.sleep(2)
    log_df = pd.io.json.json_normalize(log)
    return log_df

hashtag = 'indianmemes'

driver_path = os.path.join(os.getcwd(),'geckodriver-v0.26.0-win64', 'geckodriver.exe')

driver = open_browser(driver_path, cap)

username = instagramcreds.username
password = instagramcreds.password

login_to_instagram(driver, username, password)

comments = ['ek number :ok_hand:',
       'LOL :laughing:',
       'HAHAHA :joy: :joy:',
       'Best one so far! :smile:',
       'Chha gaye guru :pray:',
       'Perfect! :clap:',
       ]


top_posts = random.choice([0,1], p = [0.8, 0.2])
print(top_posts)
urls = get_hashtag_posts_urls(hashtag, max_posts= 10, top_posts=top_posts)

to_do = sys.argv[1]
time_now = time.strftime('%Y%m%d%H%M')

if to_do == 'interact':
	log_df = automate_interactions(driver, urls)
elif to_do == 'unfollow':
	log = unfollow_bulk(driver)
	log_df = pd.io.json.json_normalize(log)

driver.close()

log_df.to_csv(f'log_{time_now}.csv', index = False)
master_log_df = pd.read_csv('master_log.csv')
master_log_df = pd.concat([master_log_df, log_df], ignore_index=True)
master_log_df.to_csv('master_log.csv', index = False)


