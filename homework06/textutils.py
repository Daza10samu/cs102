def clean(s: str) -> str:
    """
    Clean str from some of punctuation

    Args:
        s: str

    Returns:
        str: cleaned str
    """
    for x in ",.!?;#$%^*-=":
        s = s.replace(x, "")
    for x in '/()"+':
        s = s.replace(x, " ")
    return s
