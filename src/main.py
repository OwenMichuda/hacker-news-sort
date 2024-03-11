from src.api_requests import send_get_request
from src.sort_comments import get_comment_ids, create_comment_dict

# Example usage:
if __name__ == "__main__":
    # Replace 'https://api.example.com' with the actual URL you want to send the GET request to
    item_no = 39670046
    kids = get_comment_ids(item_no)
    create_comment_dict(kids)
