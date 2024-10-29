from faker import Faker

from mdslicer import mdslicer


fake = Faker()
Faker.seed(4321)


address = fake.address()

formatted_address = "".join(f"> {line}\n" for line in address.split("\n"))

md_sections = f"""\
{fake.text()}

It's address is:

{formatted_address}

## {fake.sentence(nb_words=6)[:-1]}

You may want to see [StrasMap](https://strasmap.eu/Home).

## {fake.sentence(nb_words=5)[:-1]}

### {fake.sentence(nb_words=3)[:-1]}

- {fake.sentence(nb_words=6)[:-1]},
- {fake.sentence(nb_words=2)[:-1]},
- {fake.sentence(nb_words=6)}
"""


expected_parsed_sections = [
    {
        "title": "",
        "id": "",
        "content": """\
<p>See possible world personal decision. Itself detail out create doctor social. Hope attention friend peace create each.
House laugh health price its. Federal lot next senior.</p>
<p>It's address is:</p>
<blockquote>
<p>25102 Tom Loop Apt. 667
South Adam, ND 20695</p>
</blockquote>
""",
    },
    {
        "title": "Help today forget tell positive could yeah",
        "id": "help-today-forget-tell-positive-could-yeah",
        "content": """
<p>You may want to see <a href="https://strasmap.eu/Home">StrasMap</a>.</p>
""",
    },
    {
        "title": "Democrat ago stock if end place",
        "id": "democrat-ago-stock-if-end-place",
        "content": """
<h3 id="set-design">Set design</h3>
<ul>
<li>For book material I accept,</li>
<li>Cause,</li>
<li>Pattern both ball bit base fall rule.</li>
</ul>""",
    },
]


def test_get_sections():
    sections, toc = mdslicer.get_sections(md_sections)
    assert sections == expected_parsed_sections

    toc_1 = toc[0]
    assert toc_1["children"] == []
    assert toc_1["id"] == "help-today-forget-tell-positive-could-yeah"
    assert toc_1["level"] == 2
    assert toc_1["name"] == "Help today forget tell positive could yeah"

    toc_2 = toc[1]
    toc2_child = toc_2["children"][0]
    assert toc2_child["children"] == []
    assert toc2_child["id"] == "set-design"
    assert toc2_child["level"] == 3
    assert toc2_child["name"] == "Set design"

    assert toc_2["id"] == "democrat-ago-stock-if-end-place"
    assert toc_2["level"] == 2
    assert toc_2["name"] == "Democrat ago stock if end place"
