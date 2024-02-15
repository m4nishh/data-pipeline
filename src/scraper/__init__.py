import csv
from scraper.sitemap_crawler import get_end_urls_from_sitemap
from scraper.page_content import get_page_content
from scraper.landing_crawl import get_l1_urls
from  utils.logger import logger


# SITEMAP_INDEX_URL_WHITELIST = ['page', 'post']
# SITEMAP_INDEX_URL_BLACKLIST = []


# Read keywords from input file
def dummy_data(file_path):
    keywords = []
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                keywords.append(row[0])
    return keywords

