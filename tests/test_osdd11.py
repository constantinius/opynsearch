import textwrap
from lxml.etree import tostring, cleanup_namespaces

from opynsearch.osdd11 import parse_osdd11, encode_osdd11
from opynsearch.description import Description, Url, Image, Query, SyndicationRight


def test_parse_minimal():
    desc = parse_osdd11(
        b"""<?xml version="1.0" encoding="UTF-8"?>
        <OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
          <ShortName>Web Search</ShortName>
          <Description>Use Example.com to search the Web.</Description>
          <Tags>example web</Tags>
          <Contact>admin@example.com</Contact>
          <Url type="application/rss+xml"
               template="http://example.com/?q={searchTerms}&amp;pw={startPage?}&amp;format=rss"/>
        </OpenSearchDescription>""")

    assert desc == Description(
        "Web Search",
        "Use Example.com to search the Web.",
        tags=["example", "web"],
        contact="admin@example.com",
        urls=[
            Url(
                template="http://example.com/?q={searchTerms}&pw={startPage?}&format=rss",
                type="application/rss+xml",
            )
        ]
    )


def test_parse_detailed():
    desc = parse_osdd11(
        b"""<?xml version="1.0" encoding="UTF-8"?>
            <OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
              <ShortName>Web Search</ShortName>
              <Description>Use Example.com to search the Web.</Description>
              <Tags>example web</Tags>
              <Contact>admin@example.com</Contact>
              <Url type="application/atom+xml"
                   template="http://example.com/?q={searchTerms}&amp;pw={startPage?}&amp;format=atom"/>
              <Url type="application/rss+xml"
                   template="http://example.com/?q={searchTerms}&amp;pw={startPage?}&amp;format=rss"/>
              <Url type="text/html"
                   template="http://example.com/?q={searchTerms}&amp;pw={startPage?}"/>
              <LongName>Example.com Web Search</LongName>
              <Image height="64" width="64" type="image/png">http://example.com/websearch.png</Image>
              <Image height="16" width="16" type="image/vnd.microsoft.icon">http://example.com/websearch.ico</Image>
              <Query role="example" searchTerms="cat" />
              <Developer>Example.com Development Team</Developer>
              <Attribution>Search data Copyright 2005, Example.com, Inc., All Rights Reserved</Attribution>
              <SyndicationRight>open</SyndicationRight>
              <AdultContent>false</AdultContent>
              <Language>en-us</Language>
              <OutputEncoding>UTF-8</OutputEncoding>
              <InputEncoding>UTF-8</InputEncoding>
            </OpenSearchDescription>""")

    assert desc == Description(
        "Web Search",
        "Use Example.com to search the Web.",
        tags=["example", "web"],
        contact="admin@example.com",
        urls=[
            Url(
                template="http://example.com/?q={searchTerms}&pw={startPage?}&format=atom",
                type="application/atom+xml",
            ),
            Url(
                template="http://example.com/?q={searchTerms}&pw={startPage?}&format=rss",
                type="application/rss+xml",
            ),
            Url(
                template="http://example.com/?q={searchTerms}&pw={startPage?}",
                type="text/html",
            )
        ],
        long_name="Example.com Web Search",
        images=[
            Image("http://example.com/websearch.png", 64, 64, "image/png"),
            Image("http://example.com/websearch.ico", 16, 16, "image/vnd.microsoft.icon"),
        ],
        queries=[
            Query("example", search_terms="cat"),
        ],
        developer="Example.com Development Team",
        attribution="Search data Copyright 2005, Example.com, Inc., All Rights Reserved",
        syndication_right=SyndicationRight("open"),
        adult_content=False,
        languages=["en-us"],
        output_encodings=["UTF-8"],
        input_encodings=["UTF-8"],
    )



def test_encode_simple():
    encoded = encode_osdd11(Description(
        "Web Search",
        "Use Example.com to search the Web.",
        tags=["example", "web"],
        contact="admin@example.com",
        urls=[
            Url(
                template="http://example.com/?q={searchTerms}&pw={startPage?}&format=rss",
                type="application/rss+xml",
            )
        ]
    ))
    cleanup_namespaces(encoded)

    assert tostring(encoded, pretty_print=True).decode() == textwrap.dedent("""\
        <OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
          <ShortName>Web Search</ShortName>
          <Description>Use Example.com to search the Web.</Description>
          <Url template="http://example.com/?q={searchTerms}&amp;pw={startPage?}&amp;format=rss" type="application/rss+xml"/>
          <Tags>example web</Tags>
          <Contact>admin@example.com</Contact>
        </OpenSearchDescription>
    """)


def test_encode_complex():
    encoded = encode_osdd11(Description(
        "Web Search",
        "Use Example.com to search the Web.",
        tags=["example", "web"],
        contact="admin@example.com",
        urls=[
            Url(
                template="http://example.com/?q={searchTerms}&pw={startPage?}&format=atom",
                type="application/atom+xml",
            ),
            Url(
                template="http://example.com/?q={searchTerms}&pw={startPage?}&format=rss",
                type="application/rss+xml",
            ),
            Url(
                template="http://example.com/?q={searchTerms}&pw={startPage?}",
                type="text/html",
            )
        ],
        long_name="Example.com Web Search",
        images=[
            Image("http://example.com/websearch.png", 64, 64, "image/png"),
            Image("http://example.com/websearch.ico", 16, 16, "image/vnd.microsoft.icon"),
        ],
        queries=[
            Query("example", search_terms="cat"),
        ],
        developer="Example.com Development Team",
        attribution="Search data Copyright 2005, Example.com, Inc., All Rights Reserved",
        syndication_right=SyndicationRight("open"),
        adult_content=False,
        languages=["en-us"],
        output_encodings=["UTF-8"],
        input_encodings=["UTF-8"],
    ))
    cleanup_namespaces(encoded)

    assert tostring(encoded, pretty_print=True).decode() == textwrap.dedent("""\
        <OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
          <ShortName>Web Search</ShortName>
          <Description>Use Example.com to search the Web.</Description>
          <Url template="http://example.com/?q={searchTerms}&amp;pw={startPage?}&amp;format=atom" type="application/atom+xml"/>
          <Url template="http://example.com/?q={searchTerms}&amp;pw={startPage?}&amp;format=rss" type="application/rss+xml"/>
          <Url template="http://example.com/?q={searchTerms}&amp;pw={startPage?}" type="text/html"/>
          <Tags>example web</Tags>
          <Image width="64" height="64" type="image/png"/>
          <Image width="16" height="16" type="image/vnd.microsoft.icon"/>
          <LongName>Example.com Web Search</LongName>
          <Contact>admin@example.com</Contact>
          <Query role="example" searchTerms="cat"/>
          <Developer>Example.com Development Team</Developer>
          <Attribution>Search data Copyright 2005, Example.com, Inc., All Rights Reserved</Attribution>
          <Language>en-us</Language>
        </OpenSearchDescription>
    """)
