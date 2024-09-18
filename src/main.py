import asyncio
import aiohttp
import html
from bs4 import BeautifulSoup


async def fetch_data(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Request failed with status code: {response.status}")
            return None


async def get_comment_ids(who_is_hiring_id, base_url, session):
    url = f"{base_url}{who_is_hiring_id}.json"
    data = await fetch_data(session, url)
    if data:
        return data.get('kids', [])
    return []


async def get_comments(comment_ids, base_url, session):
    tasks = [fetch_data(session, f"{base_url}{comment_id}.json") for comment_id in comment_ids]
    responses = await asyncio.gather(*tasks)

    comments = []
    for data in responses:
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


async def main():
    base_url = "https://hacker-news.firebaseio.com/v0/item/"
    who_is_hiring_id = "41425910"
    keywords = ["remote", "chicago"]
    filter_words = ["Europe", "Switzerland"]

    async with aiohttp.ClientSession() as session:
        comment_ids = await get_comment_ids(who_is_hiring_id, base_url, session)
        comments = await get_comments(comment_ids, base_url, session)
        filtered_comments = filter_comments(comments, keywords, filter_words)

        for comment in filtered_comments:
            print(comment)
            print("---------------------------------------------------------------------------------------------------")


if __name__ == '__main__':
    asyncio.run(main())
