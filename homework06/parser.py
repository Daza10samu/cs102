import typing

import requests
from lxml import etree


class RequestNotOkError(Exception):
    pass


def make_request(url: str) -> requests.Response:
    resp = requests.get(url)
    if not resp.ok:
        raise RequestNotOkError(str(resp.status_code) + "\n" + str(resp.content))
    return resp


def get_news(url: str, n: int = 3) -> typing.List[typing.Dict[str, typing.Any]]:
    news = []
    b_url = url
    for _ in range(n):
        resp = make_request(url)
        news.extend(extract_news(resp.text))
        new_sub_url = extract_next_page(resp.text)
        if new_sub_url == "":
            break
        url = b_url + new_sub_url
    return news


def extract_news(content: str) -> typing.List[typing.Dict[str, typing.Any]]:
    tree = etree.HTML(content)
    news = []
    for i in tree.xpath("//table[@class='itemlist']/tr"):
        if i.get("class") == "morespace":
            break
        elif i.get("class") == "athing":
            news.append(
                {"url": i.xpath("./td/a")[0].get("href"), "title": i.xpath("./td/a")[0].text}
            )
        elif i.get("class") == "spacer":
            continue
        else:
            news[-1].update(
                {
                    "points": int(i.xpath(".//span[@class='score']")[0].text.split()[0])
                    if i.xpath(".//span[@class='score']")
                    else 0,
                    "author": i.xpath(".//a[@class='hnuser']")[0].text
                    if i.xpath(".//a[@class='hnuser']")
                    else "",
                    "comments": int(i.xpath(".//a")[-1].text.split()[0])
                    if "comments" in i.xpath(".//a")[-1].text
                    else 0,
                }
            )
    return news


def extract_next_page(content: str) -> str:
    try:
        return str(etree.HTML(content).xpath("//a[@class='morelink']")[0].get("href"))
    except IndexError:
        return ""
