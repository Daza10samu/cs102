import typing
from parser import get_news

from bottle import redirect, request, route, run, view

from classifier import NaiveBayesClassifier, clean
from db import *

classifier = NaiveBayesClassifier()
normalizer = {"good": 0, "maybe": 1, "never": 2}
colors = {0: "#21610B", 1: "#0B3B39", 2: "#610B0B"}
conn = make_connection()


def fit_classifier() -> None:
    xy = list(filter(lambda x: not x[-1] is None, get_news_from_db(conn)))
    classifier.fit(
        list(map(lambda x: clean(x[1]).lower(), xy)),
        list(map(lambda x: normalizer[x[-1]], xy)),  # type: ignore
    )


def get_redirect_path(referer: str) -> str:
    if "ranged" in referer:
        return "/ranged"
    elif "all" in referer:
        return "/all"
    else:
        return "/news"


@route("/news")  # type: ignore
@view("news")  # type: ignore
def news_list() -> typing.Dict[str, typing.Tuple[int, str, str, str, int, int, None]]:
    rows = filter(lambda x: x[-1] is None, get_news_from_db(conn))
    return {"rows": rows}  # type: ignore


@route("/ranged")  # type: ignore
@view("ranged_news")  # type: ignore
def ranged_list() -> typing.Dict[str, typing.Tuple[int, str, str, str, int, int, str]]:
    data = list(filter(lambda x: x[-1] is None, get_news_from_db(conn)))
    predictions = classifier.predict(list(map(lambda it: it[1], data)))
    rows = []
    for i in range(len(data)):
        rows.append(
            (
                data[i][0],
                data[i][1],
                data[i][2],
                data[i][3],
                data[i][4],
                data[i][5],
                colors[predictions[i]],  # type: ignore
            )
        )
    return {"rows": rows}  # type: ignore


@route("/all")  # type: ignore
@view("ranged_news")  # type: ignore
def all() -> typing.Dict[str, typing.Tuple[int, str, str, str, int, int, typing.Optional[str]]]:
    data = list(get_news_from_db(conn))
    rows = []
    for i in range(len(data)):
        if data[i][6] is None:
            rows.append(
                (
                    data[i][0],
                    data[i][1],
                    data[i][2],
                    data[i][3],
                    data[i][4],
                    data[i][5],
                    colors[classifier.predict([data[i][1]])[0]],  # type: ignore
                )
            )
        else:
            rows.append(
                (
                    data[i][0],
                    "(✔) " + data[i][1],
                    data[i][2],
                    data[i][3],
                    data[i][4],
                    data[i][5],
                    colors[normalizer[data[i][6]]],  # type: ignore
                )
            )
    return {"rows": rows}  # type: ignore


@route("/update_news")  # type: ignore
def update_news() -> None:
    add_news(conn, get_news("https://news.ycombinator.com/", 100))
    redirect(get_redirect_path(request.headers.environ.get("HTTP_REFERER", "")))


@route("/add_label/")  # type: ignore
def add_label() -> None:
    change_label(conn, request.query["id"], request.query["label"])
    fit_classifier()
    redirect(get_redirect_path(request.headers.environ.get("HTTP_REFERER", "")))


if __name__ == "__main__":
    make_connection()
    create_table(conn)
    fit_classifier()
    run()
