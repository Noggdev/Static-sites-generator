from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]


def block_to_block_type(block: str) -> BlockType:
    block = block.strip()

    lines = [line.strip() for line in block.splitlines() if line.strip()]

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all(l.startswith(">") for l in lines):
        return BlockType.QUOTE
    if all(line.startswith(("- ", "* ", "+ ")) for line in lines):
        return BlockType.UNORDERED_LIST
    if all(re.match(r"^\d+\.\s", line.lstrip()) for line in lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
