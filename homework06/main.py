from parser import get_news
from db import *
from bottle import route, run, view, redirect, request


# create_table()
# add_elements(get_news('https://news.ycombinator.com/', 100))

@route('/news')
@view('hello_template')
def news_list():
    rows = filter(lambda x: x[-1] is None, get_news_from_db())
    return {"rows": rows}


@route('/update_news')
def update_news():
    add_elements(get_news('https://news.ycombinator.com/', 100))
    redirect("/news")


@route('/add_label/')
def add_label():
    change_label(request.query['id'], request.query['label'])
    redirect("/news")


if __name__ == '__main__':
    run()
