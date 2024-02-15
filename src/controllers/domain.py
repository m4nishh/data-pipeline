from services.db.engine import engine

from services.db.models import Keyword, Website, ScrapedContent, ArticleContent, ArticleHeader, E_WebsiteStatus
from sqlalchemy.orm import Session
from sqlalchemy import select

def get_website(website_id: str):
    query = select(Website).where(Website.id == website_id)
    with Session(engine) as session:
        res = session.scalar(query)
        if not res:
            raise Exception(f"website with id {website_id} not found")
        return res

def update_website(website_id: str, status: E_WebsiteStatus | None):
    query = select(Website).where(Website.id == website_id)
    with Session(engine) as session:
        res = session.scalar(query)
        if not res:
            raise Exception(f"website with id {website_id} not found")
        if (status):
            res.status = status
        session.commit()
        return res
    
def save_scraped_content(scraped_content: ScrapedContent):
    # scraped_content = ScrapedContent(**kwargs)
    with Session(engine) as session:
        session.add(scraped_content)
        session.commit()
        return scraped_content

def get_page_content_by_url(website_id: str, url: str):
    query = select(ScrapedContent).where(ScrapedContent.website_id==website_id, ScrapedContent.url==url)
    with Session(engine) as session:
        res = session.scalar(query)
        return res

def get_keywords_by_website(website_id: str):
    query = select(Keyword).where(Keyword.website_id==website_id).order_by(Keyword.raw_rank.asc())
    with Session(engine) as session:
        res = session.scalars(query).all()
        return res

def save_keywords(keywords: list[Keyword], website: Website, scraped_content: ScrapedContent):
    query = select(Website).where(Website.id == website.id)
    with Session(engine) as session:
        website = session.scalar(query)
        website.keywords.extend(keywords)
        session.add(scraped_content)
        session.add_all(keywords)
        scraped_content.keywords.extend(keywords)
        website.scraped_contents.append(scraped_content)
        session.commit()
    return scraped_content
    
def save_article_header_content(content: ArticleContent, header: ArticleHeader, keywords: list[Keyword]):
    with Session(engine) as session:
        # session.add(content)
        header.article_content.append(content)
        header.keywords.extend(keywords)
        session.add(header)
        session.commit()