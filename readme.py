from mdslicer import MDSlicer
from jinja2 import Template

slicer = MDSlicer(extensions=['fenced_code'])
header, sections = slicer.slice_file("README.md")

template = Template(
"""
<h1>MDSlicer</h1>
<h2>Table of contents</h2>
<ul>
{% for section in sections[1:] %}
    <li><a href="#{{ section.id }}">{{ section.title }}</a></li>
{% endfor %}
</ul>
{% for section in sections %}
<section id="{{ section.id }}">
    <a href="#{{ section.id }}">
        <h2>{{ section.title }}</h2>
    </a>
    {{ section.content }}
</section>
{% endfor %}
"""
)
html = template.render(sections=sections)
print(html)