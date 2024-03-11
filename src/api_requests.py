import requests

API_URL = "https://hacker-news.firebaseio.com/v0/item/"
PARAMS = {"print": "pretty"}


def send_get_request(item_no):
    item_url = API_URL + str(item_no) + ".json"
    try:
        response = requests.get(item_url, PARAMS)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return response
        else:
            print(f"Error: Failed to fetch data from {item_url}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
