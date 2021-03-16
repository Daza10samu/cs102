from parser import get_news

from bottle import redirect, request, route, run, view

from classifier import NaiveBayesClassifier, clean
from db import *

classifier = NaiveBayesClassifier()
normalizer = {"good": 0, "maybe": 1, "never": 2}
colors = {0: "#21610B", 1: "#0B3B39", 2: "#610B0B"}
conn = make_connection()


def fit_classifier():
    xy = list(filter(lambda x: not x[-1] is None, get_news_from_db(conn)))
    classifier.fit(
        list(map(lambda x: clean(x[1]).lower(), xy)),  # type: ignore
        list(map(lambda x: normalizer[x[-1]], xy)),
    )  # type: ignore


def get_redirect_path(referer: str) -> str:
    if "ranged" in referer:
        return "/ranged"
    elif "all" in referer:
        return "/all"
    else:
        return "/news"


@route("/news")
@view("news")
def news_list():
    rows = filter(lambda x: x[-1] is None, get_news_from_db(conn))
    return {"rows": rows}


@route("/ranged")
@view("ranged_news")
def ranged_list():
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
                colors[predictions[i]],
            )
        )
    return {"rows": rows}


@route("/all")
@view("ranged_news")
def all():
    data = list(get_news_from_db())
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
                    colors[classifier.predict([data[i][1]])[0]],
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
                    colors[normalizer[data[i][6]]],
                )
            )
    return {"rows": rows}


@route("/update_news")
def update_news():
    add_news(conn, get_news("https://news.ycombinator.com/", 100))
    redirect(get_redirect_path(request.headers.environ.get("HTTP_REFERER", "")))


@route("/add_label/")
def add_label():
    change_label(conn, request.query["id"], request.query["label"])
    fit_classifier()
    redirect(get_redirect_path(request.headers.environ.get("HTTP_REFERER", "")))


if __name__ == "__main__":
    make_connection()
    create_table(conn)
    fit_classifier()
    run()
