from vkapi import config, session


def get_uid() -> int:
    """
    Get id of current user

    Returns: [int] id of user
    """
    return \
        session.get(
            f'users.get?access_token={config.VK_CONFIG["access_token"]}&v={config.VK_CONFIG["version"]}').json()['response'][0]['id']