from scraper.sitemap_crawler import get_end_urls_from_sitemap
from scraper.page_content import get_page_content as _scrape_page
from scraper.landing_crawl import get_l1_urls
from  utils.logger import logger
from  services.db.models import Website, ScrapedContent, E_WebsiteStatus
import  text_processing as tp
from  controllers.domain import get_page_content_by_url, save_scraped_content, update_website
import json
from urllib.error import HTTPError

MIN_WORDS_EXPECTED = 800
MAX_WORDS_EXPECTED = 20000

def get_page_content(website: Website, url: str) -> ScrapedContent:
    logger.info(f"[scraper] scraping {url}")
    if not url:
        raise "get_content(url) called with no url"
    saved_content = get_page_content_by_url(website_id=website.id, url=url)
    if saved_content:
        return saved_content
    content = _scrape_page(url=url)
    scraped_content = tp.process_text(content, website=website, url=url)
    # scraped_content = save_scraped_content()
    return scraped_content

def crawl_website_for_content(website: Website):
    content_corpus: list[str] = []
    try:
        _scraped_content = get_page_content(website=website, url=website.url)
        content_parsed = json.loads(_scraped_content.content)
        content_corpus.extend(content_parsed)
        if len(' '.join(content_corpus).split(' ')) < MIN_WORDS_EXPECTED:
            logger.info("trying l0-l1 crawling")
            urls = get_l1_urls(website.url)
            for url in urls:
                _scraped_content = get_page_content(website=website, url=url)
                content_corpus.extend(_scraped_content.content)
                if len(content_corpus.join(' ').split(' ')) >= MAX_WORDS_EXPECTED:
                    break
    except HTTPError as err:
        logger.error(err)
        logger.info("trying sitemap crawling")
        urls = get_end_urls_from_sitemap(robots=website.url + "/robots.txt")
        for url in urls:
            logger.info(f"[scraper] scraping {url}")
            _scraped_content = get_page_content(website=website, url=url)
            content_corpus.extend(_scraped_content.content)
            if len(content_corpus.join(' ').split(' ')) >= MAX_WORDS_EXPECTED:
                break
    except Exception as err:
        logger.error(err)
    update_website(website_id=website.id, status=E_WebsiteStatus.CRAWLED)
    return content_corpus