from enum import Enum


class HTMLParser(Enum):
    """
    Enum representing different HTML parsers.
    """

    LXML: str = "lxml"
    HTML5LIB: str = "html5lib"
    HTML: str = "html.parser"
