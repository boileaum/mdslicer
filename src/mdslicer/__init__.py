"""A library to slice a markdown file into HTML sections."""

__version__ = "0.2.0"

from .mdslicer import MDSlicer, split_header_and_content

__all__ = ["MDSlicer", "split_header_and_content"]
