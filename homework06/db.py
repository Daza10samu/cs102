import sqlite3
import typing as tp

from News import News


class NoSuchTable(Exception):
    pass


def make_connection(file_name: str = "news.db") -> sqlite3.Connection:
    """
    Make connection to sqlite db

    Args:
        file_name: str with name of db file

    Returns:
        Connection: connection to sqlite db
    """
    return sqlite3.connect(file_name)


def get_cursor(conn: sqlite3.Connection) -> sqlite3.Cursor:
    """
    Returns cursor to given connection

    Args:
        conn: Connection

    Returns:
        Cursor: sqlite cursor
    """
    return conn.cursor()


def execute_sql_query(conn: sqlite3.Connection, sql_query: str) -> None:
    """
    Executes SQL cure in connection

    Args:
        conn: Connection
        sql_query: str with query. NORMALIZE ALL ARGS IN QUERY BEFORE EXECUTE
    """
    get_cursor(conn).execute(sql_query)
    conn.commit()


def create_table(conn: sqlite3.Connection) -> None:
    """
    Creates SQL Table for news if it does not exist

    Args:
        conn: Connection
    """
    execute_sql_query(
        conn,
        """CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT,
                  author TEXT, url TEXT, comments INTEGER, points INTEGER, label TEXT);""",
    )


def drop_table(conn: sqlite3.Connection) -> None:
    """
    Drops Table with news if it exists

    Args:
        conn: Connection
    """
    try:
        execute_sql_query(conn, """DROP TABLE news;""")
    except sqlite3.OperationalError:
        pass


def normalize_str_for_sql(s: str) -> str:
    """
    Normalizes str to avoid SQL Injections

    Args:
        s: str

    Returns:
        str: normalized string with replaced ' to +CHAR(39)+
    """
    return s.replace("'", "+CHAR(39)+")


def change_label(conn: sqlite3.Connection, id: str, label: str) -> None:
    """

    Args:
        conn: Connection
        id: id of the news. Str but it can be converted to int
        label: str
    """
    try:
        execute_sql_query(
            conn, f"""UPDATE news SET label='{normalize_str_for_sql(label)}' WHERE id={int(id)}"""
        )
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            raise NoSuchTable("no such table")


def get_news_from_db(conn: sqlite3.Connection) -> tp.List[News]:
    """
    Returns list of news in db

    Args:
        conn: Connection

    Returns:
        list[News]: List of news in db
    """
    return list(
        map(lambda it: News(*it), get_cursor(conn).execute("""SELECT * FROM news;""").fetchall())
    )


def add_news(conn: sqlite3.Connection, news: tp.List[tp.Dict[str, tp.Any]]) -> None:
    """

    Args:
        conn: Connection
        news: List of news in format dict[str, Any]
    """
    for element in news:
        found_news = (
            get_cursor(conn)
            .execute(
                f"""SELECT id FROM news WHERE title='{normalize_str_for_sql(element['title'])}';"""
            )
            .fetchall()
        )
        if found_news:
            execute_sql_query(
                conn,
                f"""UPDATE news SET comments={element['comments']}, points={element['points']} WHERE id={found_news[0][0]}""",
            )
        else:
            execute_sql_query(
                conn,
                f"""INSERT INTO news (title, author, url, comments, points) VALUES
            ('{normalize_str_for_sql(element['title'])}', '{normalize_str_for_sql(element['author'])}',
            '{element['url']}', {element['comments']}, {element['points']});""",
            )
