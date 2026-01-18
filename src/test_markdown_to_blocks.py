from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType
import unittest


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestMarkdownToBlocksType(unittest.TestCase):
    def test_markdown_to_blocks_type_unordered_list(self):
        s = """
- This is a list -
- with items
"""
        self.assertIs(block_to_block_type(s), BlockType.UNORDERED_LIST)

    def test_markdown_to_blocks_type_ordered_list(self):
        s = """
5. This is a list
50. with items .
"""
        self.assertIs(block_to_block_type(s), BlockType.ORDERED_LIST)

    def test_markdown_to_blocks_type_quote(self):
        s = """
> This is a list >
> with items <
"""
        self.assertIs(block_to_block_type(s), BlockType.QUOTE)

    def test_markdown_to_blocks_type_code(self):
        s = """
``` import helloword
for t in hello:
print(t) ```
# yes we can
> with items
```
"""
        self.assertIs(block_to_block_type(s), BlockType.CODE)

    def test_markdown_to_blocks_type_heading(self):
        s = """
#import helloword
for t in hello:
print(t)
# yes we can
> with items
```
"""
        self.assertIs(block_to_block_type(s), BlockType.PARAGRAPH)

    def test_markdown_to_blocks_type_heading_good(self):
        s = """
###### import helloword
zlzllz
"""
        self.assertIs(block_to_block_type(s), BlockType.HEADING)

    def test_markdown_to_blocks_type_paragraph(self):
        s = """
import helloword
for t in hello:
print(t)
# yes we can
> with items
```
"""
        self.assertIs(block_to_block_type(s), BlockType.PARAGRAPH)
