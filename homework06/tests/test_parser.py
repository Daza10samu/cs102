from parser import extract_news, extract_next_page, get_news

import responses

with open("tests/eaxmple_page.html", "r") as f:
    EXAMPLE_PAGE = f.read()


def test_extract_news():
    news = extract_news(EXAMPLE_PAGE)
    assert news == [
        {
            "url": "http://avinayak.github.io/algorithms/programming/2021/02/19/finding-mona-lisa-in-the-game-of-life.html",
            "title": "Finding Mona Lisa in the Game of Life",
            "points": 88,
            "author": "mseri",
            "comments": 10,
        },
        {
            "url": "https://www.bloomberg.com/news/articles/2021-03-01/inflation-2021-malnutrition-and-hunger-fears-rise-as-food-prices-soar-globally",
            "title": "Food Prices Soar Globally",
            "points": 178,
            "author": "prostoalex",
            "comments": 143,
        },
        {
            "url": "https://text.npr.org/974534021",
            "title": "Remembering Allan McDonald, who\n            refused to approve the Challenger launch",
            "points": 952,
            "author": "everybodyknows",
            "comments": 188,
        },
        {
            "url": "https://chrisvoncsefalvay.com/2021/03/07/julia-a-post-mortem/",
            "title": "Julia:\n            A Post-Mortem",
            "points": 70,
            "author": "LittlePeter",
            "comments": 71,
        },
        {
            "url": "https://vole.wtf/kilobytes-gambit/",
            "title": "The Kilobyte’s\n            Gambit",
            "points": 416,
            "author": "msszczep2",
            "comments": 130,
        },
    ]


def test_extract_next_page():
    next_page = extract_next_page(EXAMPLE_PAGE)
    assert next_page == "news?p=2"


@responses.activate
def test_get_news():
    responses.add(responses.GET, "https://news.ycombinator.com/", body=EXAMPLE_PAGE, status=200)
    assert get_news("https://news.ycombinator.com/", 1) == extract_news(EXAMPLE_PAGE)
