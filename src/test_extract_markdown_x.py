from markdownToTextnode import extract_markdown_images, extract_markdown_links
from main import extract_title
import unittest


class test_extract_markdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [google link](https://google.com/lang=eng)"
        )
        self.assertListEqual([("google link", "https://google.com/lang=eng")], matches)

    def test_extract_markdown_images_2(self):
        matches = extract_markdown_images(
            "This is text with an [google link](https://google.com/lang=eng)"
        )
        self.assertListEqual([], matches)

    def test_extract_title(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_whitespace(self):
        markdown = "   #    Mon Titre    "
        self.assertEqual(extract_title(markdown), "Mon Titre")

    def test_extract_title_exception(self):
        markdown = "## Ceci est un H2, pas un H1"
        with self.assertRaises(Exception):
            extract_title(markdown)
