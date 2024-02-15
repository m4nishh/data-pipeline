import csv
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer
from controllers.domain import Website, Keyword, save_keywords, update_website, E_WebsiteStatus, ScrapedContent
import json
from chatgpt import get_keywords_from_website_text

def process_text(input_keywords: list[str], website: Website, url:str):
    # num_clusters = 5
    # similarity_matrix = text_similarity(input_keywords)
    # clusters = cluster_keywords(similarity_matrix, num_clusters)
    # out = sort_keywords(clusters, input_keywords)
    out = get_keywords_from_website_text(text = ' '.join(input_keywords))
    keywords = [Keyword(word=kw, raw_rank=out[kw]) for kw in out ]
    scraped_content  = save_keywords(keywords=keywords, website=website, scraped_content=ScrapedContent(website_id=website.id, url=url, content=json.dumps(input_keywords)))
    update_website(website_id=website.id, status=E_WebsiteStatus.CRAWLED)
    return scraped_content

# Write clustered keywords to output file
def sort_keywords(clusters: list[str], keywords: list[str]) -> dict[str, int]:
    # with open("out.csv", "w", newline='') as f:
        # writer = csv.writer(f)
        # writer.writerow(["Keyword", "Cluster"])
        # for keyword, cluster in zip(keywords, clusters):
            # if cluster > 0:
                # writer.writerow([keyword, cluster])
    unique_keywords = {}
    for keyword, cluster in zip(keywords, clusters):
        if cluster > 1:
            unique_keywords[keyword.lower()] = cluster
    
    # with open("keywords.out", "w", newline='') as f:
    #     f.write(", ".join(list(unique_keywords)))
    return unique_keywords


# Calculate text similarity using TF-IDF
def text_similarity(keywords):
    vectorizer = TfidfVectorizer()
    keyword_matrix = vectorizer.fit_transform(keywords)
    return keyword_matrix


# Perform clustering
def cluster_keywords(similarity_matrix, num_clusters):
    clustering = AgglomerativeClustering(n_clusters=num_clusters)
    clusters = clustering.fit_predict(similarity_matrix.toarray())
    return clusters
