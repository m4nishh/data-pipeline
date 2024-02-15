import re
import urllib.request
from faker import Faker
# from lxml import etree
from xml.etree import ElementTree
from bs4 import BeautifulSoup
from scraper.page_content import get_page_content

fake = Faker()

URL_FILTER_WHITELIST = ["/about"]

def filter_url(url: str):
    for word in URL_FILTER_WHITELIST:
        # for url in urls:
        if word in url:
            return True
    return False

# def get_l1_urls(html):
    
    
#     return hrefs

def get_l1_urls(landing_page: str) -> list[str]:
    if not landing_page:
        raise "landing_page url not given in get_end_urls_from_sitemap(landing_page) call"
    Faker.seed(0)
    hdr = {'User-Agent': fake.user_agent()}
    req = urllib.request.Request(landing_page, headers=hdr)
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    hrefs = soup.findAll('a', href=True)
    l1_urls = set()
    for href in hrefs:
        if landing_page in href['href']:
            l1_urls.update([href['href']])
    
    return list(l1_urls)