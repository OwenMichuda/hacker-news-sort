from src.api_requests import send_get_request


def get_comment_ids(post_id):
    post_json = send_get_request(post_id).json()
    return post_json.get("kids")


def create_comment_dict(comment_ids):
    comment_dict = {}

    for comment_id in comment_ids:
        comment_json = send_get_request(comment_id).json()
        comment_text = comment_json.get("text")
        comment_time = comment_json.get("time")

        comment_dict[comment_time] = comment_text

    comment_dict = dict(sorted(comment_dict.items(), reverse=True))
    return comment_dict
