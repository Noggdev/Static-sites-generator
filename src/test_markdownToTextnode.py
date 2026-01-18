import unittest
from textnode import TextNode, TextType
from markdownToTextnode import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestMarkdownToTextnode(unittest.TestCase):
    def test_base_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        node1 = TextNode("This is text with a ", TextType.TEXT)
        node2 = TextNode("code block", TextType.CODE)
        node3 = TextNode(" word", TextType.TEXT)
        test_result = [node1, node2, node3]
        self.assertEqual(test_result, new_nodes)

    def test_base_invalide_markdown(self):
        node = TextNode("This is text with a `code block` wo`rd", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    def test_base_invalide_markdown_2(self):
        node = TextNode("Thi__s is text with a _code block_ wo_r_d___", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_base_delimiter_empty(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter([node], "", TextType.CODE)

    def test_base_bold(self):
        node = TextNode("This **is** text with a **bold text** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        node1 = TextNode("This ", TextType.TEXT)
        node2 = TextNode("is", TextType.BOLD)
        node3 = TextNode(" text with a ", TextType.TEXT)
        node4 = TextNode("bold text", TextType.BOLD)
        node5 = TextNode(" word", TextType.TEXT)
        test_result = [node1, node2, node3, node4, node5]
        self.assertEqual(test_result, new_nodes)

    def test_base_bold_2(self):
        node = TextNode("This ** is** text with a **bold text ** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        node1 = TextNode("This ", TextType.TEXT)
        node2 = TextNode(" is", TextType.BOLD)
        node3 = TextNode(" text with a ", TextType.TEXT)
        node4 = TextNode("bold text ", TextType.BOLD)
        node5 = TextNode(" word", TextType.TEXT)
        test_result = [node1, node2, node3, node4, node5]
        self.assertEqual(test_result, new_nodes)

    def test_base_bold_3(self):
        node = TextNode(
            "This ** is** text with a __**bold text **__ word", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        node1 = TextNode("This ", TextType.TEXT)
        node2 = TextNode(" is", TextType.BOLD)
        node3 = TextNode(" text with a __", TextType.TEXT)
        node4 = TextNode("bold text ", TextType.BOLD)
        node5 = TextNode("__ word", TextType.TEXT)
        test_result = [node1, node2, node3, node4, node5]
        self.assertEqual(test_result, new_nodes)

    def test_base_bold_4(self):
        node = TextNode(
            "This ** is** text* with a __**bold* text **__ word", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        node1 = TextNode("This ", TextType.TEXT)
        node2 = TextNode(" is", TextType.BOLD)
        node3 = TextNode(" text* with a __", TextType.TEXT)
        node4 = TextNode("bold* text ", TextType.BOLD)
        node5 = TextNode("__ word", TextType.TEXT)
        test_result = [node1, node2, node3, node4, node5]
        self.assertEqual(test_result, new_nodes)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with an [allez sur google!](https://google.com/lang=fr) and another [allez sur bing](https://www.bing.com/lang=eng)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "allez sur google!", TextType.LINK, "https://google.com/lang=fr"
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "allez sur bing", TextType.LINK, "https://www.bing.com/lang=eng"
                ),
            ],
            new_nodes,
        )

    def test_split_images_empty(self):
        node = TextNode(
            "This is text with an image and another image ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])

    #########################################################################

    def test_text_to_textnode_1(self):
        string = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(string)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            result,
        )

    def test_plain_text_only(self):
        s = "Just a plain string."
        result = text_to_textnodes(s)
        self.assertListEqual(
            [TextNode("Just a plain string.", TextType.TEXT)],
            result,
        )

    def test_image_and_link_multiple(self):
        s = "Start ![img1](https://ex.com/1) mid [L](https://ex.com/2) end ![img2](https://ex.com/3)"
        result = text_to_textnodes(s)
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "https://ex.com/1"),
                TextNode(" mid ", TextType.TEXT),
                TextNode("L", TextType.LINK, "https://ex.com/2"),
                TextNode(" end ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://ex.com/3"),
            ],
            result,
        )

    def test_code_bold_italic_simple_order(self):
        s = "`x` then **y** then _z_."
        result = text_to_textnodes(s)
        self.assertListEqual(
            [
                TextNode("x", TextType.CODE),
                TextNode(" then ", TextType.TEXT),
                TextNode("y", TextType.BOLD),
                TextNode(" then ", TextType.TEXT),
                TextNode("z", TextType.ITALIC),
                TextNode(".", TextType.TEXT),
            ],
            result,
        )

    def test_unclosed_bold_raises(self):
        with self.assertRaises(Exception):
            text_to_textnodes("Open **bold only")

    def test_unclosed_code_raises(self):
        with self.assertRaises(Exception):
            text_to_textnodes("A `code without end")

    def test_consecutive_bold_delimiters_empty_content_filtered(self):
        # pas de noeud BOLD vide
        s = "before **** after"
        result = text_to_textnodes(s)
        self.assertListEqual(
            [TextNode("before ", TextType.TEXT), TextNode(" after", TextType.TEXT)],
            result,
        )

    def test_two_code_spans(self):
        s = "A `x` and `y`."
        result = text_to_textnodes(s)
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT),
                TextNode("x", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("y", TextType.CODE),
                TextNode(".", TextType.TEXT),
            ],
            result,
        )

    def test_image_at_start_and_link_at_end_with_punct(self):
        s = "![alt](https://ex.com/i) and text and a [link](https://ex.com/u)."
        result = text_to_textnodes(s)
        self.assertListEqual(
            [
                TextNode("alt", TextType.IMAGE, "https://ex.com/i"),
                TextNode(" and text and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://ex.com/u"),
                TextNode(".", TextType.TEXT),
            ],
            result,
        )

    def test_empty_alt_image(self):
        s = "Text ![](https://ex.com/i) done"
        result = text_to_textnodes(s)
        self.assertListEqual(
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://ex.com/i"),
                TextNode(" done", TextType.TEXT),
            ],
            result,
        )

    def test_back_to_back_images(self):
        s = "![a](https://ex.com/1)![b](https://ex.com/2)"
        result = text_to_textnodes(s)
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "https://ex.com/1"),
                TextNode("b", TextType.IMAGE, "https://ex.com/2"),
            ],
            result,
        )

    def test_image_link_image_sequence_regression(self):
        #  multiples découpes successives
        s = "pre ![img](https://ex.com/i) mid [lnk](https://ex.com/l) post ![img2](https://ex.com/j)"
        result = text_to_textnodes(s)
        self.assertListEqual(
            [
                TextNode("pre ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://ex.com/i"),
                TextNode(" mid ", TextType.TEXT),
                TextNode("lnk", TextType.LINK, "https://ex.com/l"),
                TextNode(" post ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://ex.com/j"),
            ],
            result,
        )

    def test_bold_only(self):
        s = "**bold**"
        result = text_to_textnodes(s)
        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            result,
        )

    def test_code_then_image_then_link(self):
        s = "`code` ![pic](https://ex.com/p) and [ref](https://ex.com/r)"
        result = text_to_textnodes(s)
        self.assertListEqual(
            [
                TextNode("code", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "https://ex.com/p"),
                TextNode(" and ", TextType.TEXT),
                TextNode("ref", TextType.LINK, "https://ex.com/r"),
            ],
            result,
        )

    #########################################################################

    def test_split_images_image_at_start(self):
        node = TextNode("![a](u) and text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "u"),
                TextNode(" and text", TextType.TEXT, None),
            ],
            new_nodes,
        )

    def test_split_images_image_at_end(self):
        node = TextNode("text then ![a](u)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("text then ", TextType.TEXT, None),
                TextNode("a", TextType.IMAGE, "u"),
            ],
            new_nodes,
        )

    def test_split_images_consecutive(self):
        node = TextNode("X ![a](u)![b](v) Y", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("X ", TextType.TEXT, None),
                TextNode("a", TextType.IMAGE, "u"),
                TextNode("b", TextType.IMAGE, "v"),
                TextNode(" Y", TextType.TEXT, None),
            ],
            new_nodes,
        )

    def test_split_images_only_image(self):
        node = TextNode("![only](https://x)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("only", TextType.IMAGE, "https://x"),
            ],
            new_nodes,
        )

    def test_split_images_non_text_node_passthrough(self):
        node_img = TextNode("alt", TextType.IMAGE, "https://x")
        new_nodes = split_nodes_image([node_img])
        self.assertListEqual([node_img], new_nodes)

    def test_split_images_parentheses_in_url_no_split(self):
        node = TextNode("T ![a](https://x.com/img_(1).png) Z", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_title_in_parentheses_captured_in_url_current_behavior(self):
        node = TextNode('T ![a](https://x "title") Z', TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("T ", TextType.TEXT, None),
                TextNode("a", TextType.IMAGE, 'https://x "title"'),
                TextNode(" Z", TextType.TEXT, None),
            ],
            new_nodes,
        )

    def test_split_images_empty_alt(self):
        node = TextNode("A ![](u) B", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT, None),
                TextNode("", TextType.IMAGE, "u"),
                TextNode(" B", TextType.TEXT, None),
            ],
            new_nodes,
        )

    def test_split_links_link_at_start(self):
        node = TextNode("[start](u) then text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.LINK, "u"),
                TextNode(" then text", TextType.TEXT, None),
            ],
            new_nodes,
        )

    def test_split_links_link_at_end(self):
        node = TextNode("text then [end](u)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("text then ", TextType.TEXT, None),
                TextNode("end", TextType.LINK, "u"),
            ],
            new_nodes,
        )

    def test_split_links_consecutive(self):
        node = TextNode("A [one](u)[two](v) Z", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT, None),
                TextNode("one", TextType.LINK, "u"),
                TextNode("two", TextType.LINK, "v"),
                TextNode(" Z", TextType.TEXT, None),
            ],
            new_nodes,
        )

    def test_split_links_ignores_images(self):
        node = TextNode("X ![img](u) and [lnk](v) Y", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("X ![img](u) and ", TextType.TEXT, None),
                TextNode("lnk", TextType.LINK, "v"),
                TextNode(" Y", TextType.TEXT, None),
            ],
            new_nodes,
        )

    def test_split_links_parentheses_in_url_no_split(self):
        node = TextNode("Go [here](https://x.com/a(b)c)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_empty_text(self):
        node = TextNode("A [](u) B", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT, None),
                TextNode("", TextType.LINK, "u"),
                TextNode(" B", TextType.TEXT, None),
            ],
            new_nodes,
        )

    def test_split_mix_pipeline_images_then_links(self):
        node = TextNode("Start ![img](u) and [link](v) end", TextType.TEXT)
        nodes = split_nodes_image([node])
        nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT, None),
                TextNode("img", TextType.IMAGE, "u"),
                TextNode(" and ", TextType.TEXT, None),
                TextNode("link", TextType.LINK, "v"),
                TextNode(" end", TextType.TEXT, None),
            ],
            nodes,
        )

    def test_split_multiple_input_nodes_and_passthrough(self):
        n1 = TextNode("A [x](u) B", TextType.TEXT)
        n2 = TextNode("img", TextType.IMAGE, "u")
        n3 = TextNode("C no links", TextType.TEXT)

        out = split_nodes_link([n1, n2, n3])
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT, None),
                TextNode("x", TextType.LINK, "u"),
                TextNode(" B", TextType.TEXT, None),
                n2,
                n3,
            ],
            out,
        )

    def test_split_images_empty_string_textnode(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_no_match_returns_original_node(self):
        node = TextNode("plain text only", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
