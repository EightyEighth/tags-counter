from collections import Counter as counter
from html.parser import HTMLParser
from typing import Any, List, Counter


class CountTagsHtmlParser(HTMLParser):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(CountTagsHtmlParser, self).__init__(*args, **kwargs)
        self._start_tags: List[str] = []
        self._end_tags: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[tuple]) -> None:
        self._start_tags.append(tag)

    def handle_endtag(self, tag: str) -> None:
        self._end_tags.append(tag)

    def tags(self) -> Counter:
        return counter(self._start_tags)
