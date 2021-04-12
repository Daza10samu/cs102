import sqlite3

from db import (
    add_news,
    change_label,
    create_table,
    drop_table,
    get_cursor,
    get_news_from_db,
    make_connection,
    normalize_str_for_sql,
)
from News import News


def test_make_connection() -> None:
    conn = make_connection("/tmp/tmp.db")
    try:
        with open("/tmp/tmp.db", "r") as f:
            pass
    except FileNotFoundError:
        assert False


def test_create_table() -> None:
    conn = make_connection("/tmp/tmp.db")
    create_table(conn)
    try:
        get_news_from_db(conn)
    except sqlite3.OperationalError:
        assert False


def test_get_cursor() -> None:
    conn = make_connection("/tmp/tmp.db")
    make_connection("/tmp/tmp.db")
    assert type(get_cursor(conn)) == sqlite3.Cursor


def test_normalize_str_for_sql() -> None:
    assert normalize_str_for_sql("'") == "+CHAR(39)+"


def test_add_news() -> None:
    conn = make_connection("/tmp/tmp.db")
    create_table(conn)
    add_news(conn, [{"title": "None", "comments": 0, "points": 0, "author": "None", "url": "None"}])
    assert get_news_from_db(conn) == [News(1, "None", "None", "None", 0, 0, None)]
    drop_table(conn)


def test_drop_table() -> None:
    conn = make_connection("/tmp/tmp.db")
    create_table(conn)
    drop_table(conn)
    try:
        get_news_from_db(conn)
    except sqlite3.OperationalError:
        return
    assert False


def test_change_label() -> None:
    conn = make_connection("/tmp/tmp.db")
    create_table(conn)
    add_news(conn, [{"title": "None", "comments": 0, "points": 0, "author": "None", "url": "None"}])
    change_label(conn, "1", "Nope")
    assert get_news_from_db(conn) == [News(1, "None", "None", "None", 0, 0, "Nope")]
    drop_table(conn)


def test_change_label_injetion_id() -> None:
    conn = make_connection("/tmp/tmp.db")
    create_table(conn)
    add_news(conn, [{"title": "None", "comments": 0, "points": 0, "author": "None", "url": "None"}])
    try:
        change_label(conn, "1; DROP TABLE news", "Nope")
    except ValueError:
        drop_table(conn)
    else:
        assert False


def test_change_label_injetion_label_name() -> None:
    conn = make_connection("/tmp/tmp.db")
    create_table(conn)
    add_news(conn, [{"title": "None", "comments": 0, "points": 0, "author": "None", "url": "None"}])
    change_label(conn, "1", "Nope'; DROP TABLE news")
    assert get_news_from_db(conn) == [
        News(1, "None", "None", "None", 0, 0, "Nope+CHAR(39)+; DROP TABLE news")
    ]
    drop_table(conn)
