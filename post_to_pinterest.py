import requests as r
from bs4 import BeautifulSoup
import re
import time
import urllib.parse
import sys
import pinterestcreds


def get_memes(sitemap_url):
    resp = r.get(sitemap_url)
    bs = BeautifulSoup(resp.text, 'xml')
    memes = re.findall('.*\/memes\/.+', bs.text)
    return memes

def get_meme_soup(meme):
    meme_resp = r.get(meme)
    meme_bs = BeautifulSoup(meme_resp.text, 'lxml')
    return meme_bs

def get_title(meme_bs):
    title = meme_bs.find('title').text
    return title

def convert_to_hashtag(s):
    return '#' + s.replace(' ', '')

def get_hashtags(meme_bs):
    hashtags = ''
    tags = meme_bs.find('span', attrs ={'class': 'tags'}).select('a')
    for tag in tags:
        hashtags += f' {convert_to_hashtag(tag.text)}'
    base_hashtags = '#MemeTemplate #Template #IndianMemes #Memes #DesiMemes #WeekInMemes'
    return f'{hashtags} {base_hashtags}'

def get_template_name(img_url):
    x = img_url.index('/templates/') + len('/templates/')
    template_name = img_url[x:-4]
    tn = template_name.split('-')
    for i, w in enumerate(tn):
        if w.isupper():
            continue
        else:
            tn[i] = w.title()
    template_name = ' '.join(tn)
    return template_name

access_token = pinterestcreds.access_token

def post_meme(meme, img_url, description):
    pinterest_url = f'https://api.pinterest.com/v1/pins/?access_token={access_token}&board=dk_weekinmemes/memes&note={description}&link={meme}&image_url={img_url}'
    
    post_meme = r.post(pinterest_url)
    if not post_meme.ok:
        print(post_meme.reason)


def make_pins(memes):
    count = 0
    for meme in memes:
        meme_bs = get_meme_soup(meme)
        hashtags = get_hashtags(meme_bs)
        
        meme_name = meme[m:-1]
        meme_templates = meme_bs.find_all('img', attrs={'src': re.compile(rf'.*/img/templates/{meme_name}.*')})
        
        if len(meme_templates) > 0:
            for template in meme_templates:
                img_url = template['src']
                template_name = get_template_name(img_url)
                description = urllib.parse.quote(f'{template_name} {hashtags}')
                
                post_meme(meme, img_url, description)
                
                count += 1
                if count % 5 == 0:
                    print(count)
                    time.sleep(3700)
                    
                print(f'{template_name} posted!')

sitemap_url = 'https://weekinmemes.com/sitemap.xml'

memes = get_memes(sitemap_url)

m = len('https://weekinmemes.com/memes/')

start, end = int(sys.argv[1]), int(sys.argv[2]) 

print(start)
print(end)
make_pins(memes[start:end])

