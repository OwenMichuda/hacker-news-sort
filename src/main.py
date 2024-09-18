import requests
import html
import asyncio
import aiohttp

from bs4 import BeautifulSoup

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None


def get_comment_ids(who_is_hiring_id, base_url):
    url = f"{base_url}{who_is_hiring_id}.json"
    data = fetch_data(url)
    if data:
        return data.get('kids', [])
    return []


def get_comments(comment_ids, base_url):
    comments = []
    for comment_id in comment_ids:
        url = f"{base_url}{comment_id}.json"
        data = fetch_data(url)
        if data:
            text = data.get('text')
            if text is not None:
                comments.append(text)
    return comments


def filter_comments(comments, keywords, filter_words):
    keywords = [keyword.lower() for keyword in keywords]
    filter_words = [filter_word.lower() for filter_word in filter_words]

    filtered_comments = []
    for comment in comments:
        decoded_comment = html.unescape(comment).lower()
        if any(filter_word in decoded_comment for filter_word in filter_words):
            continue
        elif any(keyword in decoded_comment for keyword in keywords):
            filtered_comments.append(clean_html(comment))

    return filtered_comments


def clean_html(html_content):
    html_content = html.unescape(html_content)
    soup = BeautifulSoup(html_content, 'html.parser')

    cleaned_text = ""
    for element in soup.descendants:
        if isinstance(element, str):
            cleaned_text += element
        elif element.name == 'a':
            continue
        elif element.name == 'p':
            cleaned_text += "\n"

    return cleaned_text


if __name__ == '__main__':
    base_url = "https://hacker-news.firebaseio.com/v0/item/"
    who_is_hiring_id = "41425910"
    keywords = ["remote", "chicago"]
    filter_words = ["Europe", "Switzerland"]

    comment_ids = get_comment_ids(who_is_hiring_id, base_url)
    comments = get_comments(comment_ids, base_url)
    filtered_comments = filter_comments(comments, keywords, filter_words)

    for comment in filtered_comments:
        print(comment)
        print("-------------------------------------------------------------------------------------------------------")
