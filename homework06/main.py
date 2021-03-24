import typing as tp
from parser import get_news

from bottle import redirect, request, route, run, view

from classifier import NaiveBayesClassifier
from db import *
from News import News
from textutils import clean

classifier = NaiveBayesClassifier()
normalizer = {"good": 0, "maybe": 1, "never": 2}
colors = {0: "#21610B", 1: "#0B3B39", 2: "#610B0B"}
conn = make_connection()


def fit_classifier() -> None:
    """ fit classifier by data from DB """
    xy = list(filter(lambda x: not x.label is None, get_news_from_db(conn)))
    classifier.clear_fitted()
    classifier.fit(
        list(map(lambda x: clean(x.title).lower(), xy)),
        list(map(lambda x: normalizer[x.label], xy)),  # type: ignore
    )


def get_redirect_path(referer: str) -> str:
    """
    Returns sub-url to redirect

    Args:
        referer: sub-url from we came to current page

    Returns:
        str: sub-url to redirect
    """
    if "ranged" in referer:
        return "/ranged"
    elif "all" in referer:
        return "/all"
    else:
        return "/news"


@route("/news")  # type: ignore
@view("news")  # type: ignore
def news_list() -> tp.Dict[str, tp.List[News]]:
    """
    Responses not a ranged news

    Returns:
        dict[str, list[News]]: list to format template
    """
    rows = list(filter(lambda x: x.label is None, get_news_from_db(conn)))
    return {"rows": rows}


@route("/ranged")  # type: ignore
@view("ranged_news")  # type: ignore
def ranged_list() -> tp.Dict[str, tp.List[tp.Tuple[str, News]]]:
    """
    Responses ranged news

    Returns:
        dict[str, list[News]]: list to format template
    """
    data = list(filter(lambda x: x.label is None, get_news_from_db(conn)))
    predictions = classifier.predict(list(map(lambda it: it.title, data)))
    rows = []
    for i in range(len(data)):
        rows.append((colors[predictions[i]], data[i]))  # type: ignore
    return {"rows": rows}


@route("/all")  # type: ignore
@view("ranged_news")  # type: ignore
def all() -> tp.Dict[str, tp.List[tp.Tuple[str, News]]]:
    """
    Responses all news

    Returns:
        dict[str, list[News]]: list to format template
    """
    data = list(get_news_from_db(conn))
    rows = []
    for i in range(len(data)):
        if data[i].label is None:
            rows.append((colors[classifier.predict([data[i].title])[0]], data[i]))  # type: ignore
        else:
            data[i].title = "(✔) " + data[i].title
            rows.append((colors[normalizer[data[i].label]], data[i]))  # type: ignore
    return {"rows": rows}


@route("/update_news")  # type: ignore
def update_news() -> None:
    """
    Updates news in db
    """
    add_news(conn, get_news("https://news.ycombinator.com/", 100))
    fit_classifier()
    redirect(get_redirect_path(request.headers.environ.get("HTTP_REFERER", "")))


@route("/add_label/")  # type: ignore
def add_label() -> None:
    """
    Add label to news

    http://$HOSTNAME/add_label/?id=$ID&label=$LABEL
    """
    change_label(conn, request.query["id"], request.query["label"])
    fit_classifier()
    redirect(get_redirect_path(request.headers.environ.get("HTTP_REFERER", "")))


if __name__ == "__main__":
    make_connection()
    create_table(conn)
    fit_classifier()
    run()
