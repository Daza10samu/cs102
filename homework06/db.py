import sqlite3
import typing


def make_connection(file_name="news.db"):
    return sqlite3.connect(file_name)


def get_cursor(conn: sqlite3.Connection) -> sqlite3.Cursor:
    return conn.cursor()


def execute_sql_query(conn: sqlite3.Connection, sql_query: str):
    get_cursor(conn).execute(sql_query)
    conn.commit()


def create_table(conn: sqlite3.Connection):
    execute_sql_query(
        conn,
        """CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT,
                  author TEXT, url TEXT, comments INTEGER, points INTEGER, label TEXT);""",
    )


def drop_table(conn: sqlite3.Connection):
    try:
        execute_sql_query(conn, """DROP TABLE news;""")
    except sqlite3.OperationalError:
        pass


def normalize_str_for_sql(s: str) -> str:
    return s.replace("'", "+CHAR(39)+")


def change_label(conn: sqlite3.Connection, id: str, label: str):
    execute_sql_query(
        conn, f"""UPDATE news SET label='{normalize_str_for_sql(label)}' WHERE id={int(id)}"""
    )


def get_news_from_db(conn: sqlite3.Connection) -> typing.List[typing.Tuple[typing.Any]]:
    return get_cursor(conn).execute("""SELECT * FROM news;""").fetchall()


def add_news(conn: sqlite3.Connection, elements: typing.List[typing.Dict[str, typing.Any]]):
    for element in elements:
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
