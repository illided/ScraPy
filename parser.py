from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Optional, Tuple, List, Union


@dataclass
class HTMLTag:
    name: str
    attrs: List[Tuple[str, Optional[str]]]
    children: List[Union['HTMLTag', str]]

    @property
    def children_tags(self):
        return list(filter(lambda x: isinstance(x, HTMLTag), self.children))

    @property
    def data_tags(self):
        return list(filter(lambda x: isinstance(x, str), self.children))

    @property
    def data(self):
        return ''.join(self.data_tags)


class HTMLTree(HTMLParser):
    def __init__(self, document):
        super().__init__()
        self._tag_stack: List[HTMLTag] = []
        self.root: Optional[HTMLTag] = None
        self._wrong_tags_buffer = []
        self.feed(document)

    def handle_starttag(self, tag, attrs):
        new_tag = HTMLTag(
            name=tag,
            attrs=attrs,
            children=[]
        )
        if tag == 'html':
            self.root = new_tag
        self._tag_stack.append(new_tag)

    def handle_endtag(self, tag: str):
        last_tag = self._tag_stack.pop()
        if tag != last_tag.name:
            raise ValueError('Closed and open tag names doesn\'t match')
        if len(self._tag_stack) != 0:
            self._tag_stack[-1].children.append(last_tag)

    def _resolve_tag_buffer(self):
        while True:
            tag = self._tag_stack[-1]
            if tag.name in self._wrong_tags_buffer:
                self._tag_stack.pop()
                self._tag_stack[-1].children.append(tag)
                self._wrong_tags_buffer.remove(tag.name)
            else:
                break

    def handle_data(self, data: str) -> None:
        if len(self._tag_stack) != 0:
            last_tag = self._tag_stack[-1]
            last_tag.children.append(data)
