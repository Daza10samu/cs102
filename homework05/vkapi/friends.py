import dataclasses
import math
import time
import typing as tp

from vkapi import config, session, users
from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
        user_id: tp.Optional[int] = None, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    response = session.get(
        f'friends.get?user_id={user_id if user_id is not None else ""}&count={count}&offset={offset}' +
        f'&fields={",".join(fields) if fields is not None else ""}' +
        f'&access_token={config.VK_CONFIG["access_token"]}&v={config.VK_CONFIG["version"]}')
    json_data = response.json()
    if 'error' in json_data:
        raise APIError
    return FriendsResponse(count=json_data['response']['count'], items=json_data['response']['items'])


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
        source_uid: tp.Optional[int] = None,
        target_uid: tp.Optional[int] = None,
        target_uids: tp.Optional[tp.List[int]] = None,
        order: str = "",
        count: tp.Optional[int] = None,
        offset: int = 0,
        progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    #  В реальных условиях у меня не работает без source_id
    # if source_uid is None:
    #     source_uid = users.get_uid()
    if target_uids is not None:
        json_data = []
        if progress is None:
            progress = lambda x, *a, **kw: x
        for i in progress(range(0, len(target_uids), 100)):
            response = session.get(
                f'friends.getMutual?source_uid={source_uid if source_uid is not None else ""}' +
                f'&target_uids={",".join(map(str, target_uids))}' +
                f'&count={count if count is not None else ""}' +
                f'&offset={i}&order={order}&access_token={config.VK_CONFIG["access_token"]}&v={config.VK_CONFIG["version"]}')
            if 'response' in (curr_resp_json := response.json()):
                json_data.extend(curr_resp_json['response'])
            else:
                raise APIError
            if i % 3 == 2:
                time.sleep(1)
        result = []
        for friend_list in json_data:
            if 'common_friends' in friend_list:
                result.append(MutualFriends(id=friend_list['id'], common_friends=friend_list['common_friends'],
                                            common_count=friend_list['common_count']))
        return result
    response = session.get(
        f'friends.getMutual?source_uid={source_uid if source_uid is not None else ""}' +
        f'&target_uid={target_uid if target_uid is not None else ""}' +
        f'&count={count if count is not None else ""}' +
        f'&offset={offset}&order={order}&access_token={config.VK_CONFIG["access_token"]}&v={config.VK_CONFIG["version"]}')
    json_data_else = response.json()
    if 'error' in json_data_else:
        raise APIError
    return json_data_else['response']
