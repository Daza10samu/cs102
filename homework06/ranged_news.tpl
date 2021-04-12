<!-- ranged_news.tpl -->
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body style="background-color:#151515;">
        <div class="ui container" style="padding-top: 10px;">
        <table class="ui celled table">
            <thead>
                <th>Title</th>
                <th>Author</th>
                <th>#Likes</th>
                <th>#Comments</th>
                <th colspan="3">Label</th>
            </thead>
            <tbody>
                %for row in rows:
                <tr style="background-color:{{ row[0] }}">
                    <td><a href="{{ row[1].url }}">{{ row[1].title }}</a></td>
                    <td>{{ row[1].author }}</td>
                    <td>{{ row[1].points }}</td>
                    <td>{{ row[1].comments }}</td>
                    <td class="positive"><a href="/add_label/?label=good&id={{ row[1].id }}">Интересно</a></td>
                    <td class="active"><a href="/add_label/?label=maybe&id={{ row[1].id }}">Возможно</a></td>
                    <td class="negative"><a href="/add_label/?label=never&id={{ row[1].id }}">Не интересно</a></td>
                </tr>
                %end
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/update_news" class="ui right floated small primary button">I Wanna more Hacker News!</a>
                    </th>
                </tr>
            </tfoot>
        </table>
        </div>
    </body>
</html>