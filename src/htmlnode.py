class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list = None,
        props: dict = None,
    ):
        self.tag: str = tag
        self.value: str = value
        self.children: list = children
        self.props: dict = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(f'{k}="{v}"' for k, v in self.props.items())

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            if self.tag == "img":
                return f"<{self.tag}{self.props_to_html()}>"
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value
        props_string = self.props_to_html()
        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list,
        props: dict = None,
    ):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")

        children_html = "".join(child.to_html() for child in self.children)
        props_string = self.props_to_html()
        return f"<{self.tag}{props_string}>{children_html}</{self.tag}>"
