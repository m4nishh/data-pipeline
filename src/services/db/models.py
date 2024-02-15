from typing import List, Set
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Date, Integer, UUID, text
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import enum
from sqlalchemy import Enum, Table, Column
from services.db.engine import engine
import uuid
from sqlalchemy.schema import FetchedValue
class Base(DeclarativeBase):
    def query(*args):
        session = Session(engine)
        return session.query(*args)

class E_WebsiteStatus(enum.Enum):
    ADDED = "ADDED"
    CRAWLED = "CRAWLED"
    KEYWORDS_GENERATED = "KEYWORDS_GENERATED"
    KEYWORDS_RATED = "KEYWORDS_RATED"
    KEYWORDS_CLUSTERED = "KEYWORDS_CLUSTERED"
    ARTICLES_GENERATED = "ARTICLES_GENERATED"
    # ARTICLE_REGENERATE_REQUEST = "ARTICLE_REGENERATE_REQUEST"
    # ARTICLE_REGENERATE_DONE = "ARTICLE_REGENERATE_DONE"

class E_KeywrodType(enum.Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"

class Website(Base):
    __tablename__ = "websites"
    id: Mapped[str] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(30))
    language: Mapped[str] = mapped_column(String(30))
    updated_at: Mapped[str] = mapped_column(Date)
    status: Mapped[E_WebsiteStatus] = mapped_column(Enum(E_WebsiteStatus))
    keywords: Mapped[List["Keyword"]] = relationship(back_populates="website")
    scraped_contents: Mapped[List["ScrapedContent"]] = relationship(back_populates="website")
    article_headers: Mapped[List["ArticleHeader"]] = relationship(back_populates="website")
    def __repr__(self) -> str:
        return f"Website(id={self.id!r}, url={self.url!r}, status={self.status!r}, keywords={self.keywords!r}, scraped_contents={self.scraped_contents!r}, article_headers={self.article_headers!r})"

class ScrapedContent(Base):
    __tablename__ = "scraped_content"
    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=text("uuid()"))
    website_id: Mapped[str] = mapped_column(ForeignKey("websites.id"))
    website: Mapped[Website] = relationship(back_populates="scraped_contents")
    content: Mapped[str] = mapped_column(String)
    # keywords: Mapped[str] = mapped_column(String)
    keywords: Mapped[List["Keyword"]] = relationship(back_populates="scraped_content")
    url: Mapped[str] = mapped_column(String)
    updated_at: Mapped[str] = mapped_column(Date, default=text("CURRENT_TIMESTAMP"))
    created_at: Mapped[str] = mapped_column(Date, default=text("CURRENT_TIMESTAMP"))

article_header_keyword_assoc = Table(
    "article_keyword_map",
    Base.metadata,
    Column("keyword_id", ForeignKey("keywords.id")),
    Column("article_id", ForeignKey("article_headers.id")),
    Column("id", primary_key=True, default=text("uuid()")),
    Column("updated_at", default=text("CURRENT_TIMESTAMP")),
    Column("created_at", default=text("CURRENT_TIMESTAMP"))
)

class Keyword(Base):
    __tablename__ = "keywords"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=text("uuid()")) # TODO: fix UUID
    website_id: Mapped[str] = mapped_column(ForeignKey("websites.id"))
    website: Mapped[Website] = relationship(back_populates="keywords")
    word: Mapped[str] = mapped_column(String)
    # raw_rank: Mapped[int] = mapped_column(int)
    # level: Mapped[E_KeywrodType] = mapped_column(Enum(E_KeywrodType))
    raw_rank: Mapped[int] = mapped_column(Integer)
    scraped_content_id: Mapped["str"] = mapped_column(ForeignKey("scraped_content.id"))
    scraped_content: Mapped[ScrapedContent] = relationship(back_populates="keywords")
    article_headers: Mapped[List["ArticleHeader"]] = relationship(
        secondary=article_header_keyword_assoc, back_populates="keywords"
    )

    def is_primary(self):
        return self.level == E_KeywrodType.PRIMARY
    def is_secondary(self):
        return self.level == E_KeywrodType.SECONDARY
    
    def __repr__(self) -> str:
        return f"Keyword(id={self.id!r}, word={self.word!r}, website_id={self.website_id!r})"
    


class ArticleHeader(Base):
    __tablename__ = "article_headers"
    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=text("uuid()"))
    website_id: Mapped[str] = mapped_column(ForeignKey("websites.id"))
    website: Mapped[Website] = relationship(back_populates="article_headers")
    article_content: Mapped[List["ArticleContent"]] = relationship(back_populates="article_header")
    title: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    meta_json: Mapped[str] = mapped_column(String)
    # category_id: Mapped[str] = mapped_column(String)
    updated_at: Mapped[str] = mapped_column(Date, default=text("CURRENT_TIMESTAMP"))
    created_at: Mapped[str] = mapped_column(Date, default=text("CURRENT_TIMESTAMP"))
    keywords: Mapped[List["Keyword"]] = relationship(
        secondary=article_header_keyword_assoc, back_populates="article_headers"
    )

class ArticleContent(Base):
    __tablename__ = "article_content"
    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=text("uuid()"))
    platform: Mapped[str] = mapped_column(String, default='BLOG')
    content: Mapped[str] = mapped_column(String)
    article_id: Mapped[str] = mapped_column(ForeignKey("article_headers.id"))
    article_header: Mapped[ArticleHeader] = relationship(back_populates="article_content")
    status: Mapped[str] = mapped_column(String)
    updated_at: Mapped[str] = mapped_column(Date, default=text("CURRENT_TIMESTAMP"))
    created_at: Mapped[str] = mapped_column(Date, default=text("CURRENT_TIMESTAMP"))
