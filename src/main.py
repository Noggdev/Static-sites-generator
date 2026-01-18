from textnode import TextNode, TextType
from markdown_to_html_node import markdown_to_html_node
import os
import sys
import shutil


def extract_title(markdown: str) -> str:
    lines = markdown.splitlines()

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("# "):
            title = stripped[2:]
            return title.strip()

    raise Exception("No H1 title found in markdown")


def copy_static_to_docs() -> None:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src_dir = os.path.join(project_root, "static")
    dst_dir = os.path.join(project_root, "docs")

    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)

    os.makedirs(dst_dir)

    def copy_recursive(current_src, current_dst):
        for item in os.listdir(current_src):
            src_path = os.path.join(current_src, item)
            dst_path = os.path.join(current_dst, item)

            if os.path.isfile(src_path):
                shutil.copy(src_path, dst_path)
            else:
                os.makedirs(dst_path, exist_ok=True)
                copy_recursive(src_path, dst_path)

    copy_recursive(src_dir, dst_dir)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    root_node = markdown_to_html_node(markdown_content)
    html_text = root_node.to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_text)
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template_content)


def generate_pages_recursive(base_path, dir_path_content, template_path, dest_dir_path):
    def generate_html_text(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()
        root_node = markdown_to_html_node(markdown_content)
        html_text = root_node.to_html()
        title = extract_title(markdown_content)
        page_content = template_content.replace("{{ Title }}", title)
        page_content = page_content.replace("{{ Content }}", html_text)
        page_content = page_content.replace('href="/', f'href="{base_path}')
        page_content = page_content.replace('src="/', f'src="{base_path}')
        return page_content

    def gen_recursive(current_src, current_dst):
        for item in os.listdir(current_src):
            src_path = os.path.join(current_src, item)
            dst_path = os.path.join(current_dst, item)

            if os.path.isfile(src_path):
                if src_path.endswith(".md"):
                    html_text = generate_html_text(src_path)
                    base, ext = os.path.splitext(dst_path)
                    dest_path_file = base + ".html"
                    with open(dest_path_file, "w", encoding="utf-8") as f:
                        f.write(html_text)
            else:
                os.makedirs(dst_path, exist_ok=True)
                gen_recursive(src_path, dst_path)

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
    os.makedirs(dest_dir_path, exist_ok=True)
    gen_recursive(dir_path_content, dest_dir_path)


def main():
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"
    copy_static_to_docs()
    generate_pages_recursive(base_path, "content/", "template.html", "docs/")


if __name__ == "__main__":
    main()
