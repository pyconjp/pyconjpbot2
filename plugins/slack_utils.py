from functools import cache

from slack_sdk import WebClient


@cache
def _get_users_dict(client: WebClient) -> dict[str, dict]:
    """Get user list from Slack

    - https://api.slack.com/methods/users.list

    :client: `slack_sdk.web.WebClient` instance with a valid token
    :return: dict of user info
    {"id1": user_info1, "id2": user_info2...}
    """
    results = client.users_list()
    users_dict = {member["id"]: member for member in results["members"]}
    return users_dict


def get_user_ids(client: WebClient, is_bot: bool = False) -> list[str]:
    """Get list of user ids

    :client: `slack_sdk.web.WebClient` instance with a valid token
    :param is_bot: True: only bot, False: without bot, None: all user
    :return: list of user ids
    """
    users_dict = _get_users_dict(client)
    if is_bot is None:
        user_ids = list(users_dict)
    else:
        user_ids = [u["id"] for u in users_dict.values() if u["is_bot"] == is_bot]
    return user_ids


def get_display_name(client: WebClient, user_id: str) -> str:
    """Returns the display name of user

    :client: `slack_sdk.web.WebClient` instance with a valid token
    :param Slack user_id:
    :return: display name
    """
    users_dict = _get_users_dict(client)
    user_info = users_dict[user_id]
    return user_info["profile"]["display_name"]


def is_admin_user(client: WebClient, user_id: str) -> bool:
    """Returns the user is admin or not

    :client: `slack_sdk.web.WebClient` instance with a valid token
    :param user_id: Slack user id
    :return: True: admin
    """
    users_dict = _get_users_dict(client)
    return users_dict[user_id]["is_admin"]
