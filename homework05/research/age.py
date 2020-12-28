import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    friends: tp.List[tp.Dict[str, tp.Any]] = get_friends(user_id, fields=['bdate']).items # type:ignore
    ages = []
    user: tp.Dict[str, tp.Any]
    for user in friends:
        date: tp.List[int]
        if 'bdate' in user and len(date := list(map(int, user['bdate'].split('.')))) == 3:
            today = dt.date.today()
            age = today.year - date[2] - 1
            if today.month > date[1] or (today.month == date[1] and today.day > date[0]):
                age += 1
            ages.append(age)
    if ages:
        return statistics.median(ages)
    else:
        return None
