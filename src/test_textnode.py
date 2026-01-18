import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node = TextNode("", None, "no url")
        node2 = TextNode("", None, "no url")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a url node", TextType.LINK, "www.google.com")
        node2 = TextNode("This is a url node", TextType.TEXT, "www.google.com")
        self.assertNotEqual(node, node2)
        node = TextNode(None, TextType.TEXT, "www.google.com")
        node2 = TextNode("This is a url node", TextType.TEXT, "www.google.com")
        self.assertNotEqual(node, node2)

    def test_enum_not_eq(self):
        node = TextNode(None, TextType.BOLD, None)
        node2 = TextNode(None, TextType.LINK, None)
        self.assertNotEqual(node, node2)

    def test_text_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.to_html()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_link(self):
        node = TextNode("This is a link to google.com", TextType.LINK, "www.google.com")
        html_node = node.to_html()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link to google.com")
        self.assertDictEqual({"href": "www.google.com"}, html_node.props)

    def test_text_img(self):
        node = TextNode(
            "image of an happy golden retriever",
            TextType.IMAGE,
            "dog.com/golden_retriever.png",
        )
        html_node = node.to_html()
        self.assertEqual(html_node.tag, "img")
        self.assertDictEqual(
            {
                "src": "dog.com/golden_retriever.png",
                "alt": "image of an happy golden retriever",
            },
            html_node.props,
        )

    def test_text_code(self):
        node = TextNode("print('hello world')", TextType.CODE)
        html_node = node.to_html()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello world')")


if __name__ == "__main__":
    unittest.main()
