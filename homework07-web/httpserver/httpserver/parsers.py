from .request import HTTPRequest


class RequestParserError(Exception):
    pass


def request_parser(raw_data: bytes) -> HTTPRequest:
    try:
        rows = raw_data.split(b"\r\n")
        method = rows[0].split(b" ")[0]
        url = rows[0].split(b" ")[1]
        headers = {
            rows[i].split(b": ")[0]: rows[i].split(b": ")[1] for i in range(1, rows.index(b""))
        }
        body = b"\r\n".join(rows[rows.index(b"") + 1 :])
        return HTTPRequest(method, url, headers, body)
    except Exception:
        raise RequestParserError
