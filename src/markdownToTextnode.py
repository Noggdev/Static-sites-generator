from textnode import TextNode, TextType
import re


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if getattr(node, "text_type", None) != TextType.TEXT:
            new_nodes.append(node)
            continue

        extracted_value = extract_markdown_images(node.text)
        if extracted_value:
            node_text = node.text
            for find in extracted_value:
                splitted = node_text.split(f"![{find[0]}]({find[1]})", 1)
                if splitted[0]:
                    text_node = TextNode(
                        text=splitted[0], text_type=TextType.TEXT, url=None
                    )
                    new_nodes.append(text_node)
                image_node = TextNode(
                    text=find[0], text_type=TextType.IMAGE, url=find[1]
                )
                new_nodes.append(image_node)
                node_text = splitted[1]

            if node_text:
                text_node = TextNode(text=node_text, text_type=TextType.TEXT, url=None)
                new_nodes.append(text_node)
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if getattr(node, "text_type", None) != TextType.TEXT:
            new_nodes.append(node)
            continue

        extracted_value = extract_markdown_links(node.text)
        if extracted_value:
            node_text = node.text
            for find in extracted_value:
                splitted = node_text.split(f"[{find[0]}]({find[1]})", 1)
                if splitted[0]:
                    text_node = TextNode(
                        text=splitted[0], text_type=TextType.TEXT, url=None
                    )
                    new_nodes.append(text_node)
                link_node = TextNode(text=find[0], text_type=TextType.LINK, url=find[1])
                new_nodes.append(link_node)
                node_text = splitted[1]

            if node_text:
                text_node = TextNode(text=node_text, text_type=TextType.TEXT, url=None)
                new_nodes.append(text_node)
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not delimiter:
        raise ValueError("delimiter ne peut pas être une chaîne vide.")

    new_nodes = []
    len_delimiter = len(delimiter)

    for old_node in old_nodes:
        if getattr(old_node, "text_type", None) != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        inside_delimiter = False
        start = 0
        end = 0
        i = 0

        while i < len(text):
            if text[i : i + len_delimiter] == delimiter:
                if not inside_delimiter:
                    # PUSH le préfixe que s'il est non vide
                    if i > end:
                        new_nodes.append(
                            TextNode(
                                text=text[end:i], text_type=TextType.TEXT, url=None
                            )
                        )
                    start = i + len_delimiter
                    inside_delimiter = True
                    i += len_delimiter
                else:
                    #  PUSH le contenu stylé que s'il est non vide
                    if i > start:
                        new_nodes.append(
                            TextNode(text=text[start:i], text_type=text_type, url=None)
                        )
                    # après fermeture, le "reste" commence après le délimiteur fermant
                    end = i + len_delimiter
                    inside_delimiter = False
                    i += len_delimiter
            else:
                i += 1

        if inside_delimiter:
            raise Exception(
                f"Invalide markdown syntax : closing delimiter for '{text_type.value}' was not found"
            )

        # PUSH le suffixe que s'il reste quelque chose
        if end < len(text):
            new_nodes.append(
                TextNode(text=text[end:], text_type=TextType.TEXT, url=None)
            )

    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text=text, text_type=TextType.TEXT)
    node = split_nodes_delimiter([node], "`", TextType.CODE)
    node = split_nodes_delimiter(node, "**", TextType.BOLD)
    node = split_nodes_delimiter(node, "_", TextType.ITALIC)
    node = split_nodes_link(node)
    node = split_nodes_image(node)
    return node
