from __future__ import absolute_import, division, unicode_literals

from six import PY2, text_type

import io

from . import support  # noqa

from html5lib.constants import namespaces
from html5lib import parse, parseFragment, HTMLParser


# tests that aren't autogenerated from text files
def test_assertDoctypeCloneable():
    doc = parse('<!DOCTYPE HTML>', treebuilder="dom")
    assert doc.cloneNode(True) is not None


def test_line_counter():
    # http://groups.google.com/group/html5lib-discuss/browse_frm/thread/f4f00e4a2f26d5c0
    assert parse("<pre>\nx\n&gt;\n</pre>") is not None


def test_namespace_html_elements_0_dom():
    doc = parse("<html></html>",
                treebuilder="dom",
                namespaceHTMLElements=True)
    assert doc.childNodes[0].namespaceURI == namespaces["html"]


def test_namespace_html_elements_1_dom():
    doc = parse("<html></html>",
                treebuilder="dom",
                namespaceHTMLElements=False)
    assert doc.childNodes[0].namespaceURI is None


def test_namespace_html_elements_0_etree():
    doc = parse("<html></html>",
                treebuilder="etree",
                namespaceHTMLElements=True)
    assert doc.tag == "{%s}html" % (namespaces["html"],)


def test_namespace_html_elements_1_etree():
    doc = parse("<html></html>",
                treebuilder="etree",
                namespaceHTMLElements=False)
    assert doc.tag == "html"


def test_unicode_file():
    assert parse(io.StringIO("a")) is not None


def test_duplicate_attribute():
    # This is here because we impl it in parser and not tokenizer
    doc = parse('<p class=a class=b>')
    el = doc[1][0]
    assert el.get("class") == "a"


def test_debug_log():
    parser = HTMLParser(debug=True)
    parser.parse("<!doctype html><title>a</title><p>b<script>c</script>d</p>e")

    expected = [('dataState', 'InitialPhase', 'InitialPhase', 'processDoctype', {'type': 'Doctype'}),
                ('dataState', 'BeforeHtmlPhase', 'BeforeHtmlPhase', 'processStartTag', {'name': 'title', 'type': 'StartTag'}),
                ('dataState', 'BeforeHeadPhase', 'BeforeHeadPhase', 'processStartTag', {'name': 'title', 'type': 'StartTag'}),
                ('dataState', 'InHeadPhase', 'InHeadPhase', 'processStartTag', {'name': 'title', 'type': 'StartTag'}),
                ('rcdataState', 'TextPhase', 'TextPhase', 'processCharacters', {'type': 'Characters'}),
                ('dataState', 'TextPhase', 'TextPhase', 'processEndTag', {'name': 'title', 'type': 'EndTag'}),
                ('dataState', 'InHeadPhase', 'InHeadPhase', 'processStartTag', {'name': 'p', 'type': 'StartTag'}),
                ('dataState', 'AfterHeadPhase', 'AfterHeadPhase', 'processStartTag', {'name': 'p', 'type': 'StartTag'}),
                ('dataState', 'InBodyPhase', 'InBodyPhase', 'processStartTag', {'name': 'p', 'type': 'StartTag'}),
                ('dataState', 'InBodyPhase', 'InBodyPhase', 'processCharacters', {'type': 'Characters'}),
                ('dataState', 'InBodyPhase', 'InBodyPhase', 'processStartTag', {'name': 'script', 'type': 'StartTag'}),
                ('scriptDataState', 'TextPhase', 'TextPhase', 'processCharacters', {'type': 'Characters'}),
                ('dataState', 'TextPhase', 'TextPhase', 'processEndTag', {'name': 'script', 'type': 'EndTag'}),
                ('dataState', 'InBodyPhase', 'InBodyPhase', 'processCharacters', {'type': 'Characters'}),
                ('dataState', 'InBodyPhase', 'InBodyPhase', 'processEndTag', {'name': 'p', 'type': 'EndTag'}),
                ('dataState', 'InBodyPhase', 'InBodyPhase', 'processCharacters', {'type': 'Characters'})]

    if PY2:
        for i, log in enumerate(expected):
            log = [x.encode("ascii") if isinstance(x, text_type) else x for x in log]
            expected[i] = tuple(log)

    assert parser.log == expected


def test_no_duplicate_clone():
    frag = parseFragment("<b><em><foo><foob><fooc><aside></b></em>")
    assert len(frag) == 2


def test_self_closing_col():
    parser = HTMLParser()
    parser.parseFragment('<table><colgroup><col /></colgroup></table>')
    assert not parser.errors
