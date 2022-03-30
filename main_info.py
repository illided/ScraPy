from dataclasses import dataclass

from parser import HTMLTree, HTMLTag
from typing import Tuple, List


@dataclass
class MeaningTag:
    tag_proxy: HTMLTag
    children: List['MeaningTag']
    n_meaningful_char: int
    n_useless_char: int

    @property
    def meaning_coef(self):
        return self.n_meaningful_char / (self.n_meaningful_char + self.n_useless_char)

    @property
    def children_tags(self):
        return list(filter(lambda x: isinstance(x, MeaningTag), self.children))


class MeaningTree:
    MEANINGLESS_TAGS = ['script', 'style']

    def __init__(self, doc: HTMLTree):
        if doc.root is None:
            raise ValueError
        self.root = self._meaningful_tag_from_html_tag(doc.root)

    def _pre_order(self, tag: MeaningTag = None) -> List[MeaningTag]:
        if tag is None:
            tag = self.root
        result = [tag]
        for child in tag.children_tags:
            result.extend(self._pre_order(child))
        return result

    def sorted_tags(self) -> List[MeaningTag]:
        lst = self._pre_order(self.root)
        lst.sort(reverse=True, key=lambda x: x.meaning_coef)
        return lst

    def best_tag(self):
        return self.sorted_tags()[0]

    def main_info(self, threshold=0, min_len=0) -> List[str]:
        meaningful_tags = [n for n in self._pre_order() if n.meaning_coef > threshold]
        data = [x.tag_proxy.data.strip() for x in meaningful_tags]
        data_filtered = [x for x in data if len(x) > min_len]
        return data_filtered

    def doc_info_percentage(self) -> float:
        return self.root.meaning_coef

    def _get_data_stat(self, tag) -> Tuple[int, int]:
        data_len = 0
        spaces_len = 0
        for child in tag.children:
            if isinstance(child, str):
                data_filtered = child.strip()
                data_len += len(data_filtered)
                spaces_len += len(child) - len(data_filtered)
        return data_len, spaces_len

    def _get_attr_len(self, tag) -> int:
        attr_len = 0
        for attr in tag.attrs:
            attr_len += len(attr[0])
            if attr[1] is not None:
                attr_len += len(attr[1])
        return attr_len

    def _meaningful_tag_from_html_tag(self, tag: HTMLTag) -> MeaningTag:
        data_len, space_len = self._get_data_stat(tag)
        useless = len(tag.name) * 2 + self._get_attr_len(tag) + space_len
        meaningful = data_len
        new_children = []
        for child in tag.children_tags:
            new_child = self._meaningful_tag_from_html_tag(child)
            meaningful += new_child.n_meaningful_char
            useless += new_child.n_useless_char
            new_children.append(new_child)
        if tag.name in self.MEANINGLESS_TAGS:
            useless += meaningful
            meaningful = 0
        return MeaningTag(
            tag_proxy=tag,
            children=new_children,
            n_meaningful_char=meaningful,
            n_useless_char=useless
        )
