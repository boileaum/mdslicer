"""Parse markdown content"""

import markdown
from markdown.extensions import toc
import bs4


md = markdown.Markdown(extensions=["toc"])


def md_slugify(value: str) -> str:
    """
    slugify string using markdown extension slugifier

    Args:
        value: string to slugify

    Returns:
        str: slugified string
    """
    return toc.slugify(value, "-")


def get_sections(md_content: str) -> tuple[list[dict], list[dict]]:
    """
    Parse markdown string to build a list of section dicts:
    
    >>> sections, toc = get_sections(md_content)
    >>> print(section[0])
    {
        'title': h2 title,
        'id': slugify(title),
        'content': section_content
    }
    

    Also return the table of content tokens

    Args:
        md_content: markdown content

    Returns:
        tuple: list of section dicts, list of toc tokens
    """

    # Important for performance:
    # see https://python-markdown.github.io/extensions/api/#registerextension
    md.reset()
    html = md.convert(md_content)
    # Build section dict
    soup = bs4.BeautifulSoup(html, "html.parser")
    section_dict = {}

    # If section does not start with a h2 tag
    no_h2_section = ""
    for tag in soup:
        if isinstance(tag, bs4.Tag) and tag.name == "h2":
            break
        else:
            no_h2_section += str(tag)

    if no_h2_section:
        section_dict[""] = no_h2_section

    # Parse the rest
    for h2 in soup.find_all("h2"):
        title = h2.text
        section_dict[title] = ""
        for tag in h2.next_siblings:
            if isinstance(tag, bs4.Tag) and tag.name == "h2":
                break
            section_dict[title] += str(tag)

    sections = []
    for title, content in section_dict.items():
        section = {"title": title, "id": md_slugify(title), "content": content}
        sections.append(section)

    return sections, md.toc_tokens
