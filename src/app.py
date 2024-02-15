import config
from  chatgpt import create_content
from  utils import logger
import scraper as scraper
from  services.sqs import consumer, producer
from  utils.logger import logger
import  controllers.domain as DB
import  controllers.scraping_controller as scraper_control
from  services.db.models import ArticleContent, ArticleHeader
import json
from slugify import slugify
from collections import OrderedDict
import enum

class E_JobTypes(enum.Enum):
    SCRAPE_AND_GATHER_KEYWORDS = "SCRAPE_AND_GATHER_KEYWORDS"
    WEBSITE_SCRAPED = "WEBSITE_SCRAPED"
    KEYWORDS_GENERATED = "KEYWORDS_GENERATED"
    KEYWORDS_CLUSTERED = "KEYWORDS_CLUSTERED"
    GENERATE_ARTICLES = "GENERATE_ARTICLES"
    ARTICLES_GENERATED = "ARTICLES_GENERATED"

def main():
    # config.ensure_envvars()
    consumer(process_message_fn=process_request)

    # process_request(json.dumps({
    #     "websiteId": "59b891c6-9db3-11ee-bb08-0a8dc119fcf6",
    #     "name": E_JobTypes.SCRAPE_AND_GATHER_KEYWORDS.value
    # }))
    

def process_new_website(website: DB.Website):
    # DB.save_keywords(keywords=[DB.Keyword(word="test")], website=website)
    content_corpus = scraper_control.crawl_website_for_content(website=website)
    # keywords = tp.process_text(content_corpus, website=website)
    logger.info(f"done processing {website.id}")
    producer(message={"name": E_JobTypes.KEYWORDS_GENERATED.value, "websiteId": website.id})

def generate_articles(website: DB.Website):
    keywords = DB.get_keywords_by_website(website_id=website.id,)
    # primaries = list(filter(lambda x: x.is_primary(), keywords))
    # secondaries = list(filter(lambda x: x.is_secondary(), keywords))
    
    MAX_ARTICLES = 2

    clusters: OrderedDict[str, list[str]] = OrderedDict()
    # NUMBER_OF_SECONDARIES_IN_CLUSTER = 2
    # for primary in primaries:
    #     for i in range(0,len(secondaries),1):
    #         sec = secondaries[i, NUMBER_OF_SECONDARIES_IN_CLUSTER]
    #         cluster_slug = slugify(f"{primary}-{sec.join('-')}")
    #         clusters[cluster_slug] = [primary, *sec]
    

    # clusters = keywords # for now, one cluster will be just one primary
    clusters = {cluster: [cluster.word] for cluster in keywords[:MAX_ARTICLES]}
    
    for cluster in clusters:
        article = create_content(keywords=clusters[cluster])
        [article_title, article_content] = article.split('\n\n', 1)
        header = ArticleHeader(website_id = website.id, title=article_title, status="DRAFT")
        content = ArticleContent(article_id=header.id, content=article_content, status="GENERATED")
        DB.save_article_header_content(content=content, header=header, keywords=[cluster])

    logger.info(f"done generating articles for {website.id}")
    producer(message={"name": E_JobTypes.ARTICLES_GENERATED.value, "websiteId": website.id})

def process_request(event_body: str):
    logger.info(event_body)
    event = json.loads(event_body)
    website = DB.get_website(website_id=event["websiteId"])
    logger.info(f"got event: {json.dumps(event)}")
    match event["name"]:
        case E_JobTypes.SCRAPE_AND_GATHER_KEYWORDS.value:
            process_new_website(website=website)
        case E_JobTypes.GENERATE_ARTICLES.value:
            generate_articles(website=website)
        # case _:
        case E_JobTypes.KEYWORDS_GENERATED.value | E_JobTypes.KEYWORDS_CLUSTERED.value | E_JobTypes.WEBSITE_SCRAPED.value | E_JobTypes.ARTICLES_GENERATED.value:
            pass
        case _:
            raise Exception(f"unhandled event type {event['name']}")

    # input = scraper.dummy_data(file_path="keywordsinput.csv")
    # keywords = tp.process_text(input)
    # logger.info(keywords)
    # content = create_content(keywords=keywords)

# # Test processing
# def test():
#     input = scraper.dummy_data(file_path="keywordsinput.csv")
#     keywords = tp.process_text(input)
#     logger.info(keywords)
#     # content = create_content(keywords=keywords)


if __name__ == "__main__":
    main()