
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
from faker import Faker

from  utils.logger import logger

fake = Faker()


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def strip_junk(el):
    el = el.strip()
    if el == '\n':
        return False
    if el == '':
        return False
    return True

bad_tags = ['script', 'style', 'footer', 'header', 'nav', 'svg']

def text_from_html(body: str):
    soup = BeautifulSoup(body, 'html.parser')
    for a in soup(bad_tags):
        a.decompose()
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts) 
    stripped_visible_text =  filter(strip_junk, visible_texts)
    content = [t.strip() for t in stripped_visible_text]
    return content

def get_page_content(url) -> list[str]:
    if not url:
        raise "get_content(url) called with no url"
    Faker.seed(0)
    hdr = {'User-Agent': fake.user_agent()}
    req = urllib.request.Request(url, headers=hdr)
    html  = urllib.request.urlopen(req).read()
    return text_from_html(html)


# //*[matches(@*, '.*footer.*')]