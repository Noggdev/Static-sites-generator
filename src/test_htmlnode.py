import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p", "text dans le tag p", None, None)
        node2 = HTMLNode("p", "text dans le tag p", None, None)
        self.assertEqual(node1.__repr__(), node2.__repr__())

        node1 = HTMLNode(None, "raw text", None, None)
        node2 = HTMLNode(None, "raw text", None, None)
        self.assertEqual(node1.__repr__(), node2.__repr__())

        node1 = HTMLNode("h1", "SUPER TITRE", None, {"id": "primary-navigation"})
        node2 = HTMLNode("h1", "SUPER TITRE", None, {"id": "primary-navigation"})
        self.assertEqual(node1.__repr__(), node2.__repr__())

        children_node = HTMLNode(None, "raw text", None, None)
        node1 = HTMLNode(
            "h1", "SUPER TITRE", children_node, {"id": "primary-navigation"}
        )
        print(node1)
        node2 = HTMLNode(
            "h1", "SUPER TITRE", children_node, {"id": "primary-navigation"}
        )
        self.assertEqual(node1.__repr__(), node2.__repr__())

    def test_not_eq(self):
        node1 = HTMLNode("h1", "text dans le tag p", None, None)
        node2 = HTMLNode("p", "text dans le tag p", None, None)
        self.assertNotEqual(node1.__repr__(), node2.__repr__())

        node1 = HTMLNode(None, "raw text", None, None)
        node2 = HTMLNode(None, "raw text maybe", None, None)
        self.assertNotEqual(node1.__repr__(), node2.__repr__())

        node1 = HTMLNode("h1", "SUPER TITRE", None, {"id": "primary-navigation"})
        node2 = HTMLNode("h1", "SUPER TITRE", None, {"id": "second-navigation"})
        self.assertNotEqual(node1.__repr__(), node2.__repr__())

        children_node = HTMLNode(None, "raw text", None, None)
        node1 = HTMLNode(
            "p", "SUPER TITRE", children_node, {"id": "primary-navigation"}
        )
        node2 = HTMLNode("h1", "SUPER TITRE", None, {"id": "primary-navigation"})
        self.assertNotEqual(node1.__repr__(), node2.__repr__())

    def test_enum_not_eq(self):
        children_node = HTMLNode(None, "raw text", None, None)
        node1 = HTMLNode(
            "h1",
            "SUPER TITRE",
            children_node,
            {
                "id": "primary-navigation",
                "test_id": "8784",
                "secret_id": "nothing to see",
            },
        )
        print(node1.props_to_html())
        self.assertTrue(True)


class TestLeafNodeToHtml(unittest.TestCase):
    def test_plain_paragraph(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_with_props(self):
        node = LeafNode("p", "Hello, world!", props={"class": "lead", "id": "greeting"})
        self.assertEqual(
            node.to_html(), '<p class="lead" id="greeting">Hello, world!</p>'
        )

    def test_no_tag_returns_raw_value(self):
        node = LeafNode(None, "Hello")
        self.assertEqual(node.to_html(), "Hello")

    def test_raises_on_none_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_attribute_value_coercion(self):
        node = LeafNode("p", "count", props={"data-count": 3})
        self.assertEqual(node.to_html(), '<p data-count="3">count</p>')

    def test_props_insertion_order(self):
        node = LeafNode("div", "x", props={"a": "1", "b": "2", "c": "3"})
        self.assertEqual(node.to_html(), '<div a="1" b="2" c="3">x</div>')


class TestHTMLNodeToHTML(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children_mixed(self):
        parent = ParentNode(
            "div",
            [
                LeafNode(None, "A"),
                LeafNode("b", "B"),
                LeafNode(None, "C"),
            ],
        )
        self.assertEqual(parent.to_html(), "<div>A<b>B</b>C</div>")

    def test_to_html_parent_with_props(self):
        parent = ParentNode(
            "div",
            [LeafNode(None, "x")],
            props={"class": "c", "id": "i"},
        )
        self.assertEqual(parent.to_html(), '<div class="c" id="i">x</div>')

    def test_to_html_parent_and_child_props(self):
        parent = ParentNode(
            "div",
            [LeafNode("span", "child", props={"class": "chip"})],
            props={"id": "wrapper"},
        )
        self.assertEqual(
            parent.to_html(),
            '<div id="wrapper"><span class="chip">child</span></div>',
        )

    def test_to_html_text_only_children(self):
        parent = ParentNode(
            "p",
            [LeafNode(None, "Hello "), LeafNode(None, "World")],
        )
        self.assertEqual(parent.to_html(), "<p>Hello World</p>")

    def test_to_html_raises_when_tag_missing(self):
        with self.assertRaises(ValueError) as cm:
            ParentNode(None, [LeafNode("span", "x")]).to_html()
        self.assertEqual(str(cm.exception), "ParentNode must have a tag")

    def test_to_html_raises_when_children_is_none(self):
        with self.assertRaises(ValueError) as cm:
            ParentNode("div", None).to_html()
        self.assertEqual(str(cm.exception), "ParentNode must have children")

    def test_to_html_raises_when_children_empty_list(self):
        with self.assertRaises(ValueError) as cm:
            ParentNode("div", []).to_html()
        self.assertEqual(str(cm.exception), "ParentNode must have children")

    def test_to_html_deep_nesting(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "p",
                            [LeafNode("b", "x"), LeafNode(None, "y")],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><section><p><b>x</b>y</p></section></div>",
        )

    def test_to_html_list_with_item_props(self):
        node = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode(None, "1")], props={"class": "item"}),
                ParentNode("li", [LeafNode(None, "2")], props={"data-id": "2"}),
            ],
            props={"id": "list"},
        )
        self.assertEqual(
            node.to_html(),
            '<ul id="list"><li class="item">1</li><li data-id="2">2</li></ul>',
        )

    def test_children_order_is_preserved(self):
        children = [
            LeafNode(None, "first"),
            LeafNode("i", "second"),
            LeafNode(None, "third"),
        ]
        node = ParentNode("p", children)
        self.assertEqual(
            node.to_html(),
            "<p>first<i>second</i>third</p>",
        )


if __name__ == "__main__":
    unittest.main()
