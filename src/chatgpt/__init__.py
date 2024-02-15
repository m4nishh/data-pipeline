from  config import APP_CONFIG
import openai
from  utils.logger import logger
import re

openai.api_key = APP_CONFIG.open_api_key


def create_content(keywords: list[str]):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant who generates articles with a heading that has to be published in websites for SEO based on keywors that the user mentions"
            },
            {
                "role": "system",
                "content": "you shouldnt use more than 600 to 700 words"
            },
            {
                "role": "system",
                "content": "infer the industry space from the user input"
            },
            {
                "role": "user",
                "content": ", ".join(keywords)
            }
        ],
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    logger.info(response.usage)
    content = response.choices[0].message.content
    return content

def get_keywords_from_website_text(text: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant who generates keywords based on text that is scraped from a webpage. ignore keywords that are navigatory in nature. like home, about us"
            },
            {
                "role": "system",
                "content": "the user is gonna feed text scraped from a webpage"
            },
            {
                "role": "system",
                "content": "get me a set of comma separated keywords that'll help me generate articles"
            },
            # {
            #     "role": "system",
            #     "content": "infer the industry space from the user input"
            # },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    logger.info(response.usage)
    _content: str = response.choices[0].message.content
    # // remove "keywords: " from the text
    # content = _content.split(':', 1)[1]
    _keywords = re.split(',|\n', _content)
    # _keywords = content.split(',')
    keywords = _keywords[1:]
    out = {}
    i=1
    for k in keywords:
        out[k] = i
        i+=1
    return out
