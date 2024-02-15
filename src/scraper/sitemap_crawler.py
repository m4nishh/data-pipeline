import re
import urllib.request
from faker import Faker
# from lxml import etree
from xml.etree import ElementTree

fake = Faker()

URL_FILTER_WHITELIST = ["/about"]

def filter_url(url: str):
    for word in URL_FILTER_WHITELIST:
        # for url in urls:
        if word in url:
            return True
    return False

def get_end_urls_from_sitemap(robots:str):
    if not robots:
        raise "robots url not given in get_end_urls_from_sitemap(robots) call"
    Faker.seed(0)
    hdr = {'User-Agent': fake.user_agent()}
    req = urllib.request.Request(robots, headers=hdr)
    content = urllib.request.urlopen(req).read().decode('utf-8')
    sitemap_indices = []
    for line in content.split('\n'):
        if line.startswith('Sitemap:'):
            split = line.split(':', maxsplit=1)
            sitemap_indices.append(split[1].strip())
    print("sitemap_indices", sitemap_indices)

    sitemaps = []
    for sitemap_root in sitemap_indices:
        hdr = {'User-Agent': fake.user_agent()}
        req = urllib.request.Request(sitemap_root, headers=hdr)
        content = urllib.request.urlopen(req).read().decode('utf-8')
        content = re.sub(r"[\n\t]*", "", content)
        content = re.sub(' xmlns="[^"]+"', '', content, count=1)

        try: 
            
            tree = ElementTree.fromstring(content)
            sm = [loc.text for loc in tree.findall('./sitemap/loc')]
            if len(sm) > 0:
                sitemaps.extend(sm)
            else:
                print(f"no sitemap urls found in {sitemap_root}")
            
        except Exception as err:
            print(err) 

    print("sitemaps", sitemaps)
    urls = set()
    for sitemap in sitemaps:
        hdr = {'User-Agent': fake.user_agent()}
        req = urllib.request.Request(sitemap, headers=hdr)
        content = urllib.request.urlopen(req).read().decode('utf-8')
        content = re.sub(r"[\n\t]*", "", content)
        content = re.sub(' xmlns="[^"]+"', '', content, count=1)

        try:
            tree = ElementTree.fromstring(content)
            sm = [loc.text for loc in tree.findall('./url/loc')]
            if len(sm) > 0:
                sm = list(filter(filter_url, sm))
                urls.update(sm)
            else:
                print(f"no sitemap urls found in {sitemap_root}")
            
        except Exception as err:
            print(err) 
    
    return list(urls)