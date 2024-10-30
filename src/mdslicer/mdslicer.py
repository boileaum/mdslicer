"""
Parse markdown file into header, sections and table of content tokens

>>> from mdslicer import MdSlicer
>>> slicer = MdSlicer()
>>> header, sections = slicer.slice_file("tests/data/sample.md")
>>> header["title"]
'Example'
>>> sections[0]["title"]
''
>>> sections[1]["title"]
'Help today forget tell positive could yeah'
>>> toc_tokens[0]["name"]
'Help today forget tell positive could yeah'
>>> toc_tokens[1]["name"]
'Democrat ago stock if end place'

"""

from __future__ import annotations
from pathlib import Path
import sys
from typing import Callable


import bs4
import frontmatter
import markdown  # type: ignore
from markdown.extensions.toc import slugify
import yaml


class MDSlicer:
    """
    Parse markdown content into sections and table of content tokens
    """

    def __init__(
        self,
        extensions: list[str] | None = None,
        additional_parser: Callable | None = None,
    ):
        """
        Create a markdown parser with the given extensions.

        Args:
            extensions: List of markdown extensions
            additional_parser: Additional parser to apply on the markdown content
        """
        if extensions is None:
            extensions = []
        self.md = markdown.Markdown(extensions=extensions)
        self.md.reset()
        self.additional_parser = additional_parser

    def slice_content(self, md_content: str) -> list[dict]:
        """
        Convert markdown content to HTML.
        Return the list of HTML sections and the table of content tokens

        >>> md_content = '''
        ... ## Section 1
        ... 
        ... Content 1
        ... 
        ... ## Section 2
        ... 
        ... Content 2'''
        >>> e_content(md_content)
        [{'title': 'Section 1', 'id': 'section-1', 'content': '<p>Content 1</p>'},
         {'title': 'Section 2', 'id': 'section-2', 'content': '<p>Content 2</p>'}]

        Args:
            md_content: Markdown content

        Returns:
            List of sections
        """
        if self.additional_parser:
            md_content = self.additional_parser(md_content)
        self.md.reset()
        html = self.md.convert(md_content)
        sections = self.get_sections(html)

        return sections

    def get_sections(self, html: str) -> list[dict]:
        """
        Get sections from the HTML content by splitting it with h2 tags

        >>> html = "<h2>Section 1</h2><p>Content 1</p><h2>Section 2</h2><p>Content 2</p>"
        >>> get_sections(html)
        [{'title': 'Section 1', 'id': 'section-1', 'content': '<p>Content 1</p>'},
         {'title': 'Section 2', 'id': 'section-2', 'content': '<p>Content 2</p>'}]

        Args:
            html: HTML content

        Returns:
            List of sections with an id, a title and an html content
        """

        # Important for performance:
        # see https://python-markdown.github.io/extensions/api/#registerextension

        # Build section dict
        soup = bs4.BeautifulSoup(html, "html.parser")
        sections = []

        # If section does not start with a h2 tag
        no_h2_section = ""
        for tag in soup:
            if tag.name == "h2":  # type: ignore
                break
            else:
                no_h2_section += str(tag)

        if no_h2_section:
            sections.append({"title": "", "id": "", "content": no_h2_section})

        # Parse the rest
        for h2 in soup.find_all("h2"):
            title = h2.text
            content = ""
            for tag in h2.next_siblings:
                if tag.name == "h2":  # type: ignore
                    break
                content += str(tag)
            section = {"title": title, "id": slugify(title, "-"), "content": content}
            sections.append(section)

        return sections

    def slice_file(
        self, mdfile_path: str | Path
    ) -> tuple[dict, list[dict]]:
        """
        Parse a markdown file into a YAML header and a content

        >>> header, sections = slice_file("tests/data/sample.md")
        >>> header["title"]
        'Example'
        >>> sections[0]["title"]
        ''
        >>> sections[1]["title"]
        'Help today forget tell positive could yeah'

        Args:
            mdfile_path: Path to the markdown file

        Returns:
            header of the markdown file,
            content sections of the markdown file,
        """
        mdfile_path = Path(mdfile_path)
        file_content = mdfile_path.read_text()
        try:
            header, md_content = frontmatter.parse(file_content)

        except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
            sys.exit(f"Cannot parse {mdfile_path}:\n{file_content}\nReason: {e}")

        sections = self.slice_content(md_content)
        return header, sections
