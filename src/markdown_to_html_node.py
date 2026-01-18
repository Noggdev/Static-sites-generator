from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType
from markdownToTextnode import text_to_textnodes, TextType
from htmlnode import LeafNode, ParentNode
import re
import textwrap


def markdown_to_html_node(markdown: str) -> ParentNode:
    markdown_blocks = markdown_to_blocks(markdown)

    htmlnodes_blocks = []

    for markdown_block in markdown_blocks:
        block_type = block_to_block_type(markdown_block)
        # On ne compacte que pour les paragraphes et les titres,
        # afin de ne pas casser les listes / citations.
        if block_type in (BlockType.PARAGRAPH, BlockType.HEADING):
            lines = [line.strip() for line in markdown_block.splitlines()]
            # On élimine les lignes vides et on compacte les espaces
            markdown_block = " ".join([ln for ln in lines if ln])

        htmlnode_block, markdown_block_fixed = markdown_block_to_htmlnode(
            markdown_block, block_type
        )
        if block_type == BlockType.CODE:
            code_node = LeafNode("code", value=markdown_block_fixed)
            htmlnode_block = ParentNode("pre", [code_node])

        elif htmlnode_block.tag in ("ul", "ol"):
            pass
        else:
            htmlnode_children = block_children_to_htmlnode(markdown_block_fixed)
            htmlnode_block.children = htmlnode_children

        htmlnodes_blocks.append(htmlnode_block)

    root = ParentNode(tag="div", children=htmlnodes_blocks, props=None)

    return root


def markdown_block_to_htmlnode(markdown_block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode(tag="p", children=[], props=None), markdown_block
        case BlockType.HEADING:
            head_number = markdown_block[:6].split()[0].count("#")
            return ParentNode(
                tag=f"h{head_number}", children=[], props=None
            ), markdown_block[head_number + 1 :]
        case BlockType.CODE:
            content = markdown_block.strip()
            content = content.removeprefix("```").removesuffix("```")

            # Beaucoup de tests fournissent un \n juste après la fence ouvrante
            if content.startswith("\n"):
                content = content[1:]

            # On supprime l'indentation commune (due à la triple-quoted string)
            content = textwrap.dedent(content)

            # Le test attend un \n final dans le contenu du <code>
            if not content.endswith("\n"):
                content += "\n"

            return ParentNode(tag="pre", children=[], props=None), content
        case BlockType.QUOTE:
            lines = [ligne.removeprefix("> ") for ligne in markdown_block.splitlines()]
            markdown_block = "\n".join(lines)
            return ParentNode(tag="blockquote", children=[], props=None), markdown_block
        case BlockType.UNORDERED_LIST:
            lines = [ligne[2:] for ligne in markdown_block.splitlines()]
            ul_children = []
            for line in lines:
                textnode_li_children = text_to_textnodes(line)
                htmlnode_li_children = block_children_to_htmlnode(textnode_li_children)
                ul_children.append(ParentNode("li", htmlnode_li_children))
            markdown_block = "\n".join(lines)
            return ParentNode(
                tag="ul", children=ul_children, props=None
            ), markdown_block
        case BlockType.ORDERED_LIST:
            lines = []
            for line in markdown_block.splitlines():
                m = re.match(r"^(\d+\.\s)(.*)", line.lstrip())
                lines.append(m.group(2) if m else line)
            ol_children = []
            for line in lines:
                textnode_li_children = text_to_textnodes(line)
                htmlnode_li_children = block_children_to_htmlnode(textnode_li_children)
                ol_children.append(ParentNode("li", htmlnode_li_children))
            markdown_block = "\n".join(lines)
            return ParentNode(
                tag="ol", children=ol_children, props=None
            ), markdown_block


def block_children_to_htmlnode(block):
    nodes = []
    if type(block) == str:
        text_nodes = text_to_textnodes(block)
    else:
        text_nodes = block

    for tn in text_nodes:
        match tn.text_type:
            case TextType.TEXT:
                nodes.append(LeafNode(None, tn.text))
            case TextType.BOLD:
                nodes.append(LeafNode("b", tn.text))
            case TextType.ITALIC:
                nodes.append(LeafNode("i", tn.text))
            case TextType.CODE:
                nodes.append(LeafNode("code", tn.text))
            case TextType.LINK:
                nodes.append(LeafNode("a", tn.text, {"href": tn.url}))
            case TextType.IMAGE:
                nodes.append(LeafNode("img", None, {"src": tn.url, "alt": tn.text}))
            case _:
                raise ValueError(f"Unknown text type: {tn.text_type}")
    return nodes
