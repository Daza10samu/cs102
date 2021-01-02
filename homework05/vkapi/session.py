import typing as tp
from time import sleep

import requests
from requests.adapters import HTTPAdapter
from requests import Session as RequestsSession

from requests.packages.urllib3.util.retry import Retry


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = kwargs["timeout"]
        del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


class Session(RequestsSession):
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
        super().__init__()
        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["GET", "POST"],
            backoff_factor=backoff_factor,
        )
        adapter = TimeoutHTTPAdapter(timeout=timeout, max_retries=retry_strategy)
        self.__base_url = base_url
        self.mount("https://", adapter)
        self.mount("http://", adapter)

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:  # type:ignore
        return super().get("/".join((self.__base_url, url)), *args, **kwargs)

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:  # type:ignore
        return super().post("/".join((self.__base_url, url)), *args, **kwargs)
