# Static Site Generator

A lightweight static site generator built from scratch in Python. Converts Markdown files into a fully navigable HTML website.

## How it works

The generator parses Markdown into an intermediate tree of text nodes, converts them to HTML nodes, and injects the result into an HTML template. It handles inline formatting (bold, italic, code, links, images) and block-level structures (headings, lists, quotes, code blocks).

## Project structure

    content/          — Markdown source files
    src/              — Python source (parser, HTML node classes, converter)
    static/           — CSS, images, and other static assets
    docs/             — Generated output
    template.html     — HTML template with {{ Title }} and {{ Content }} placeholders
    main.sh           — Run the dev server locally
    build.sh          — Build for GitHub Pages
    test.sh           — Run tests

## Usage

```bash
# Local dev
./main.sh

# Build for deployment
./build.sh

# Run tests
./test.sh
```

## Built with

Python — no external dependencies, no frameworks.
