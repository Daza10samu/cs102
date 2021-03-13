from parser import extract_news, extract_next_page, get_news

import responses

try:
    with open("tests/eaxmple_page.html", "r") as f:
        EXAMPLE_PAGE = f.read()
except FileNotFoundError:
    EXAMPLE_PAGE = """
<html lang="en" op="news">
<table border="0" cellpadding="0" cellspacing="0" class="itemlist">
    <tr class='athing' id='26384403'>
        <td align="right" valign="top" class="title"><span class="rank">1.</span></td>
        <td valign="top" class="votelinks">
            <center><a id='up_26384403' href='vote?id=26384403&amp;how=up&amp;goto=news'>
                <div class='votearrow' title='upvote'></div>
            </a></center>
        </td>
        <td class="title"><a
                href="http://avinayak.github.io/algorithms/programming/2021/02/19/finding-mona-lisa-in-the-game-of-life.html"
                class="storylink">Finding Mona Lisa in the Game of Life</a><span class="sitebit comhead"> (<a
                href="from?site=avinayak.github.io"><span class="sitestr">avinayak.github.io</span></a>)</span></td>
    </tr>
    <tr>
        <td colspan="2"></td>
        <td class="subtext">
            <span class="score" id="score_26384403">88 points</span> by <a href="user?id=mseri"
                                                                           class="hnuser">mseri</a> <span
                class="age"><a href="item?id=26384403">1 hour ago</a></span> <span id="unv_26384403"></span> | <a
                href="hide?id=26384403&amp;goto=news">hide</a> | <a href="item?id=26384403">10&nbsp;comments</a>
        </td>
    </tr>
    <tr class="spacer" style="height:5px"></tr>
    <tr class='athing' id='26383419'>
        <td align="right" valign="top" class="title"><span class="rank">2.</span></td>
        <td valign="top" class="votelinks">
            <center><a id='up_26383419' href='vote?id=26383419&amp;how=up&amp;goto=news'>
                <div class='votearrow' title='upvote'></div>
            </a></center>
        </td>
        <td class="title"><a
                href="https://www.bloomberg.com/news/articles/2021-03-01/inflation-2021-malnutrition-and-hunger-fears-rise-as-food-prices-soar-globally"
                class="storylink">Food Prices Soar Globally</a><span class="sitebit comhead"> (<a
                href="from?site=bloomberg.com"><span class="sitestr">bloomberg.com</span></a>)</span></td>
    </tr>
    <tr>
        <td colspan="2"></td>
        <td class="subtext">
            <span class="score" id="score_26383419">178 points</span> by <a href="user?id=prostoalex"
                                                                            class="hnuser">prostoalex</a> <span
                class="age"><a href="item?id=26383419">4 hours ago</a></span> <span id="unv_26383419"></span> | <a
                href="hide?id=26383419&amp;goto=news">hide</a> | <a href="item?id=26383419">143&nbsp;comments</a>
        </td>
    </tr>
    <tr class="spacer" style="height:5px"></tr>
    <tr class='athing' id='26380822'>
        <td align="right" valign="top" class="title"><span class="rank">3.</span></td>
        <td valign="top" class="votelinks">
            <center><a id='up_26380822' href='vote?id=26380822&amp;how=up&amp;goto=news'>
                <div class='votearrow' title='upvote'></div>
            </a></center>
        </td>
        <td class="title"><a href="https://text.npr.org/974534021" class="storylink">Remembering Allan McDonald, who
            refused to approve the Challenger launch</a><span class="sitebit comhead"> (<a
                href="from?site=npr.org"><span
                class="sitestr">npr.org</span></a>)</span></td>
    </tr>
    <tr>
        <td colspan="2"></td>
        <td class="subtext">
            <span class="score" id="score_26380822">952 points</span> by <a href="user?id=everybodyknows"
                                                                            class="hnuser">everybodyknows</a> <span
                class="age"><a href="item?id=26380822">13 hours ago</a></span> <span id="unv_26380822"></span> | <a
                href="hide?id=26380822&amp;goto=news">hide</a> | <a href="item?id=26380822">188&nbsp;comments</a>
        </td>
    </tr>
    <tr class="spacer" style="height:5px"></tr>
    <tr class='athing' id='26384133'>
        <td align="right" valign="top" class="title"><span class="rank">4.</span></td>
        <td valign="top" class="votelinks">
            <center><a id='up_26384133' href='vote?id=26384133&amp;how=up&amp;goto=news'>
                <div class='votearrow' title='upvote'></div>
            </a></center>
        </td>
        <td class="title"><a href="https://chrisvoncsefalvay.com/2021/03/07/julia-a-post-mortem/" class="storylink">Julia:
            A Post-Mortem</a><span class="sitebit comhead"> (<a href="from?site=chrisvoncsefalvay.com"><span
                class="sitestr">chrisvoncsefalvay.com</span></a>)</span></td>
    </tr>
    <tr>
        <td colspan="2"></td>
        <td class="subtext">
            <span class="score" id="score_26384133">70 points</span> by <a href="user?id=LittlePeter"
                                                                           class="hnuser">LittlePeter</a> <span
                class="age"><a href="item?id=26384133">2 hours ago</a></span> <span id="unv_26384133"></span> | <a
                href="hide?id=26384133&amp;goto=news">hide</a> | <a href="item?id=26384133">71&nbsp;comments</a>
        </td>
    </tr>
    <tr class="spacer" style="height:5px"></tr>
    <tr class='athing' id='26380110'>
        <td align="right" valign="top" class="title"><span class="rank">5.</span></td>
        <td valign="top" class="votelinks">
            <center><a id='up_26380110' href='vote?id=26380110&amp;how=up&amp;goto=news'>
                <div class='votearrow' title='upvote'></div>
            </a></center>
        </td>
        <td class="title"><a href="https://vole.wtf/kilobytes-gambit/" class="storylink">The Kilobyte’s
            Gambit</a><span class="sitebit comhead"> (<a href="from?site=vole.wtf"><span
                class="sitestr">vole.wtf</span></a>)</span></td>
    </tr>
    <tr>
        <td colspan="2"></td>
        <td class="subtext">
            <span class="score" id="score_26380110">416 points</span> by <a href="user?id=msszczep2" class="hnuser">msszczep2</a>
            <span class="age"><a href="item?id=26380110">15 hours ago</a></span> <span id="unv_26380110"></span> |
            <a href="hide?id=26380110&amp;goto=news">hide</a> | <a href="item?id=26380110">130&nbsp;comments</a>
        </td>
    </tr>
    <tr class="spacer" style="height:5px"></tr>
    <tr class="morespace" style="height:10px"></tr>
    <tr>
        <td colspan="2"></td>
        <td class="title"><a href="news?p=2" class="morelink" rel="next">More</a></td>
    </tr>
</table>
</html>"""


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
