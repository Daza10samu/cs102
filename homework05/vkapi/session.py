import typing as tp
from time import sleep

import requests
from requests.adapters import HTTPAdapter
from requests import Session as RequestsSession


# from requests.packages.urllib3.util.retry import Retry


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param min_delay: Минимальное время, которое будет между запросами.
    :param max_delay: Максимальное время, которое будет между запросами.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.__session = RequestsSession()
        self.__base_url = base_url
        self.__timeout = timeout
        self.__max_retries = max_retries
        self.__backoff_factor = backoff_factor

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        response: tp.Optional[requests.Response]
        try:
            if "timeout" not in kwargs:
                response = self.__session.get(
                    self.__base_url + "/" + url, *args, timeout=self.__timeout, **kwargs
                )
            else:
                response = self.__session.get(self.__base_url + "/" + url, *args, **kwargs)
        except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout):
            response = None
        if response is None or not response.ok:
            curr_delay = self.__backoff_factor
            for i in range(self.__max_retries):
                try:
                    if "timeout" not in kwargs:
                        response = self.__session.get(
                            self.__base_url + "/" + url, *args, timeout=self.__timeout, **kwargs
                        )
                    else:
                        response = self.__session.get(self.__base_url + "/" + url, *args, **kwargs)
                except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout):
                    pass
                if response is not None and response.ok:
                    break
                if i != self.__max_retries - 1:
                    curr_delay = curr_delay * 2
                    sleep(curr_delay)
        if response is None:
            raise requests.exceptions.ReadTimeout
        elif not response.ok:
            raise requests.exceptions.RetryError
        else:
            return response

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        response: tp.Optional[requests.Response]
        try:
            if "timeout" not in kwargs:
                response = self.__session.post(
                    self.__base_url + "/" + url, *args, timeout=self.__timeout, **kwargs
                )
            else:
                response = self.__session.post(self.__base_url + "/" + url, *args, **kwargs)
        except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout):
            response = None
        if response is None or not response.ok:
            curr_delay = self.__backoff_factor * 2
            sleep(curr_delay)
            for i in range(self.__max_retries):
                try:
                    if "timeout" not in kwargs:
                        response = self.__session.post(
                            self.__base_url + "/" + url, *args, timeout=self.__timeout, **kwargs
                        )
                    else:
                        response = self.__session.post(self.__base_url + "/" + url, *args, **kwargs)
                except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout):
                    pass
                if response is not None and response.ok:
                    break
                if i != self.__max_retries - 1:
                    curr_delay = curr_delay * 2
                    sleep(curr_delay)
        if response is None:
            raise requests.exceptions.ReadTimeout
        elif not response.ok:
            raise requests.exceptions.RetryError
        else:
            return response
