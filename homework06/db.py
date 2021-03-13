import sqlite3
import typing

conn: sqlite3.Connection


def make_connection(file_name="news.db"):
    global conn
    conn = sqlite3.connect(file_name)


def get_cursor() -> sqlite3.Cursor:
    return conn.cursor()


def execute_sql_query(sql_query: str):
    get_cursor().execute(sql_query)
    conn.commit()


def create_table():
    execute_sql_query(
        """CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT,
    author TEXT, url TEXT, comments INTEGER, points INTEGER, label TEXT); """
    )


def drop_table():
    try:
        execute_sql_query("""DROP TABLE news;""")
    except sqlite3.OperationalError:
        pass


def normalize_str_for_sql(s: str) -> str:
    return s.replace("'", "+CHAR(39)+")


def change_label(id: int, label: str):
    execute_sql_query(f"""UPDATE news SET label='{label}' WHERE id={id}""")


def get_news_from_db() -> typing.List[typing.Tuple[typing.Any]]:
    return get_cursor().execute("""SELECT * FROM news;""").fetchall()


def add_elements(elements: typing.List[typing.Dict[str, typing.Any]]):
    for element in elements:
        found_elems = (
            get_cursor()
                .execute(
                f"""SELECT id FROM news WHERE title='{normalize_str_for_sql(element['title'])}';"""
            )
                .fetchall()
        )
        if found_elems:
            execute_sql_query(
                f"""UPDATE news SET comments={element['comments']} WHERE id={found_elems[0][0]}"""
            )
            execute_sql_query(
                f"""UPDATE news SET points={element['points']} WHERE id={found_elems[0][0]}"""
            )
        else:
            execute_sql_query(
                f"""INSERT INTO news (title, author, url, comments, points) VALUES
            ('{normalize_str_for_sql(element['title'])}', '{normalize_str_for_sql(element['author'])}',
            '{element['url']}', {element['comments']}, {element['points']});"""
            )
