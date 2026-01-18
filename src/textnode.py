from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"

    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str = None, text_type: TextType = None, url: str = None):
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text},{self.text_type.value},{self.url})"

    def to_html(self):
        if self.text_type == TextType.TEXT:
            return LeafNode(value=self.text)

        if self.text_type == TextType.BOLD:
            return LeafNode(tag="b", value=self.text)

        if self.text_type == TextType.ITALIC:
            return LeafNode(tag="i", value=self.text)

        if self.text_type == TextType.CODE:
            return LeafNode(tag="code", value=self.text)

        if self.text_type == TextType.LINK:
            return LeafNode(tag="a", props={"href": self.url}, value=self.text)

        if self.text_type == TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": self.url, "alt": self.text}
            )
