import requests as r
from bs4 import BeautifulSoup
import re
import time
import urllib.parse
import sys
import pinterestcreds

resp = r.get('https://weekinmemes.com/sitemap.xml')
bs = BeautifulSoup(resp.text, 'xml')
pages = bs.select('loc')
num_pages = len(pages)
memes = []
mc = 0 # meme counter
i = -1
while mc < int(sys.argv[1]):
    i += 1
    try:
        re.search('.*\/memes\/.+', pages[i].text).group()
        memes.append(pages[i].text)
        mc += 1
    except AttributeError:
        continue

def get_meme_soup(meme):
    meme_resp = r.get(meme)
    meme_bs = BeautifulSoup(meme_resp.text, 'lxml')
    return meme_bs

x = len('Origin\n\n')

def convert_to_hashtag(s):
    return '#' + s.replace(' ', '')

meme_hashtags = '#IndianMemes #Memes #DesiMemes #WeekInMemes'

def get_description(meme_bs):
    desc = meme_bs.find('meta', attrs = {'name': 'description'})
    desc_lst = [desc['content'][x:]]
    tags = meme_bs.find('span', attrs ={'class': 'tags'}).select('a')
    for tag in tags:
        desc_lst.append(convert_to_hashtag(tag.text))
    description = ' '.join(desc_lst)[:450]
    description.replace('\n', ' ')
    meme_hashtags = '#IndianMemes #Memes #DesiMemes #WeekInMemes'
    return urllib.parse.quote(f'{description} {meme_hashtags}')

def get_title(meme_bs):
    title = meme_bs.find('title').text
    return title

access_token = pinterestcreds.access_token

m = len('https://weekinmemes.com/memes/')

def post_meme(meme, img_url, description):
    pinterest_url = f'https://api.pinterest.com/v1/pins/?access_token={access_token}&board=weekinmemes/memes&note={description}&link={meme}&image_url={img_url}'
    post_meme = r.post(pinterest_url)
    if not post_meme.ok:
        print(post_meme.reason)

def make_pins(memes):
    count = 0
    for meme in memes:
        meme_bs = get_meme_soup(meme)
        description = get_description(meme_bs)
        meme_name = meme[m:-1]
        meme_img_urls = meme_bs.find_all('img', attrs={'src': re.compile(rf'.*/img/{meme_name}.*')})
        if len(meme_img_urls) > 0:
            for meme_img_url in meme_img_urls:
                post_meme(meme, meme_img_url['src'], description)
                count += 1
                if count % 9 == 0:
                    print(count)
                    time.sleep(3700)

        meme_template_urls = meme_bs.find_all('img', attrs={'src': re.compile(rf'.*/img/templates/{meme_name}.*')})
        if len(meme_template_urls) > 0:
            for meme_template_url in meme_template_urls:
                post_meme(meme, meme_template_url['src'], description)
                count += 1
                if count % 9 == 0:
                    print(count)
                    time.sleep(3700)
        print(f'{meme} posted completely!')

make_pins(memes)
