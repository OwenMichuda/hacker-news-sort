import requests


def send_get_request(url):
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the response content (usually JSON data)
            print("Response:")
            print(response.text)
        else:
            print(f"Error: Failed to fetch data from {url}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


# Example usage:
if __name__ == "__main__":
    # Replace 'https://api.example.com' with the actual URL you want to send the GET request to
    url = 'https://hacker-news.firebaseio.com/v0/item/39562986.json?print=pretty'
    send_get_request(url)
