import sqlite3

from db import (
    add_elements,
    change_label,
    create_table,
    drop_table,
    get_cursor,
    get_news_from_db,
    make_connection,
    normalize_str_for_sql,
)


def test_make_connection():
    make_connection("/tmp/tmp.db")
    try:
        with open("/tmp/tmp.db", "r") as f:
            pass
    except FileNotFoundError:
        assert False


def test_create_table():
    make_connection("/tmp/tmp.db")
    create_table()
    try:
        get_news_from_db()
    except sqlite3.OperationalError:
        assert False


def test_get_cursor():
    make_connection("/tmp/tmp.db")
    assert type(get_cursor()) == sqlite3.Cursor


def test_normalize_str_for_sql():
    assert normalize_str_for_sql("'") == "+CHAR(39)+"


def test_add_elements():
    make_connection("/tmp/tmp.db")
    create_table()
    add_elements([{"title": "None", "comments": 0, "points": 0, "author": "None", "url": "None"}])
    assert get_news_from_db() == [(1, "None", "None", "None", 0, 0, None)]
    drop_table()


def test_drop_table():
    make_connection("/tmp/tmp.db")
    create_table()
    drop_table()
    try:
        get_news_from_db()
    except sqlite3.OperationalError:
        return
    assert False


def test_change_label():
    make_connection("/tmp/tmp.db")
    create_table()
    add_elements([{"title": "None", "comments": 0, "points": 0, "author": "None", "url": "None"}])
    change_label(1, "Nope")
    assert get_news_from_db() == [(1, "None", "None", "None", 0, 0, "Nope")]
    drop_table()
