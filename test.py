import unittest
import re

from markdown_converter import convert_markdown_to_html_helper, replace_br_tags


class UnitTests(unittest.TestCase):
    def test_sanity(self):
        self.assertEqual("<code>x == 2</code>", convert_markdown_to_html_helper("`x == 2`", build_meta()))

    def test_code_is_inserted_in_paragraph(self):
        expected = "Here's some code: <code>x == 2</code>."
        actual = convert_markdown_to_html_helper("Here's some code: `x == 2`.", build_meta())

        self.assertEqual(expected, actual)

    def test_everything_is_not_wrapped_in_h1(self):
        expected = "<h1>Heading 1</h1>\nHere's some code: <code>x == 2</code>."
        actual = convert_markdown_to_html_helper("# Heading 1\nHere's some code: `x == 2`.", build_meta())

        self.assertEqual(expected, actual)

    def test_replace_br(self):
        expected = 'Two qualities a good writer must have:\n\n- {{c1::Confidence}},\n- {{c2::Ego}}'
        actual = replace_br_tags('Two qualities a good writer must have:<br><br>- {{c1::Confidence}},<br>- {{c2::Ego}}')

        self.assertEqual(expected, actual)

    def test_markdown_conversion_with_br(self):
        expected = 'Two qualities a good writer must have: <ul> <li>{{c1::Confidence}},</li> <li>{{c2::Ego}}</li> </ul>'
        actual = convert_markdown_to_html_helper('Two qualities a good writer must have:<br><br>- {{c1::Confidence}},<br>- {{c2::Ego}}', build_meta())

        self.assertEqual(normalize_whitespace(expected), normalize_whitespace(actual))

    def test_that_html_tags_are_ignored(self):
        expected = r'im a <b>card</b> with <div>im in a div!</div> some latex <anki-mathjax>3\log_{b}{x}</anki-mathjax>'
        actual = convert_markdown_to_html_helper(expected, build_meta())

        self.assertEqual(expected, actual)

    def test_that_escape_characters_are_not_removed(self):
        expected = r'\(3\log_{b}{x}\)'
        actual = convert_markdown_to_html_helper(expected, build_meta())

        self.assertEqual(expected, actual)

    def test_that_escape_characters_are_not_removed_mixed_with_other_text(self):
        expected = r'This is some mathjax - \(3\log_{b}{x}\). isnt it cool!'
        actual = convert_markdown_to_html_helper(expected, build_meta())

        self.assertEqual(expected, actual)

    def test_that_multiline_escape_characters_are_not_removed(self):
        expected = r'This is some inline mathjax - \(3\log_{b}{x}\). and this is some multiline mathjax - \[3\log_{b}{x}\]'
        actual = convert_markdown_to_html_helper(expected, build_meta())

        self.assertEqual(expected, actual)


    def test_that_multiline_escape_characters_with_markdown_are_not_removed(self):
        expected = r'This is some <em>inline</em> mathjax - \(3\log_{b}{x}\). and this is some <code>multiline</code> mathjax - \[3\log_{b}{x}\]'
        actual = convert_markdown_to_html_helper(r'This is some *inline* mathjax - \(3\log_{b}{x}\). and this is some `multiline` mathjax - \[3\log_{b}{x}\]', build_meta())

        self.assertEqual(expected, actual)


def normalize_whitespace(text):
    """Normalize whitespace by collapsing multiple spaces and newlines into single spaces."""
    return re.sub(r'\s+', ' ', text).strip()


def build_meta():
    return {"name": "Simple Markdown",
            "mod": 1720511633,
            "min_point_version": 230900,
            "max_point_version": 231201,
            "branch_index": 0,
            "disabled": False,
            "config": {
                "automatic": True,
                "extensions": {
                    "abbr": False,
                    "admonition": False,
                    "attr_list": False,
                    "codehilite": False,
                    "def_list": False,
                    "fenced_code": True,
                    "footnotes": False,
                    "legacy_attrs": False,
                    "legacy_em": False,
                    "md_in_html": False,
                    "meta": False,
                    "nl2br": False,
                    "sane_lists": False,
                    "smarty": False,
                    "tables": False,
                    "toc": False,
                    "wikilinks": False},
                "wrap_with_p_tags": False},
            "conflicts": [],
            "update_enabled": True}
