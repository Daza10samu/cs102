from parser import get_news

from bottle import redirect, request, route, run, view

from classifier import NaiveBayesClassifier
from db import *

classifier = NaiveBayesClassifier()
normalizer = {"good": 0, "maybe": 1, "never": 2}
colors = {0: "#21610B", 1: "#0B3B39", 2: "#610B0B"}


@route("/news")
@view("news")
def news_list():
    rows = filter(lambda x: x[-1] is None, get_news_from_db())
    return {"rows": rows}


@route("/ranged")
@view("ranged_news")
def ranged_list():
    (*data,) = filter(lambda x: x[-1] is None, get_news_from_db())
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
    (*data,) = get_news_from_db()
    predictions = classifier.predict(list(map(lambda it: it[1], data)))
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
    add_elements(get_news("https://news.ycombinator.com/", 100))
    if "ranged" in request.headers.environ["HTTP_REFERER"]:
        redirect("/ranged")
    elif "all" in request.headers.environ["HTTP_REFERER"]:
        redirect("/all")
    else:
        redirect("/news")


@route("/add_label/")
def add_label():
    change_label(request.query["id"], request.query["label"])
    (*xy,) = filter(lambda x: not x[-1] is None, get_news_from_db())
    classifier.fit(list(map(lambda x: x[1], xy)), list(map(lambda x: normalizer[x[-1]], xy)))
    if "ranged" in request.headers.environ["HTTP_REFERER"]:
        redirect("/ranged")
    elif "all" in request.headers.environ["HTTP_REFERER"]:
        redirect("/all")
    else:
        redirect("/news")


if __name__ == "__main__":
    make_connection()
    create_table()
    (*xy,) = filter(lambda x: not x[-1] is None, get_news_from_db())
    classifier.fit(list(map(lambda x: x[1], xy)), list(map(lambda x: normalizer[x[-1]], xy)))  # type: ignore
    run()
