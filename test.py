import unittest
import re

from markdown_core import convert_markdown_to_html_helper, replace_br_tags


class UnitTests(unittest.TestCase):
    def test_sanity(self):
        self.assertEqual("<code>x == 2</code>", convert_markdown_to_html_helper("`x == 2`", build_config()))

    def test_nbsp_are_converted(self):
        expected = 'My List:\n<ul>\n<li>Item 1</li>\n<li>Item 2</li>\n</ul>'
        actual = convert_markdown_to_html_helper('My List:<br><br>-&nbsp;Item 1\n-&nbsp;Item 2', build_config(replace_non_breaking_spaces=True))

        self.assertEqual(expected, actual)

    def test_empty_divs_are_removed(self):
        expected = 'customers can demand a refund if an {{c1::SLA}} is not met'
        actual = convert_markdown_to_html_helper('<div> <div> <div> <div>customers can demand a refund if an {{c1::SLA}} is not met</div></div></div></div>', build_config(remove_empty_divs=True))

        self.assertEqual(expected, actual)

    def test_non_empty_divs_are_not_removed(self):
        expected = '<div class="dont delete me">customers can demand a refund if an {{c1::SLA}} is not met</div>'
        actual = convert_markdown_to_html_helper('<div class="dont delete me">customers can demand a refund if an {{c1::SLA}} is not met</div>', build_config(remove_empty_divs=True))

        self.assertEqual(expected, actual)

    def test_code_is_inserted_in_paragraph(self):
        expected = "Here's some code: <code>x == 2</code>."
        actual = convert_markdown_to_html_helper("Here's some code: `x == 2`.", build_config())

        self.assertEqual(expected, actual)

    def test_everything_is_not_wrapped_in_h1(self):
        expected = "<h1>Heading 1</h1>\nHere's some code: <code>x == 2</code>."
        actual = convert_markdown_to_html_helper("# Heading 1\nHere's some code: `x == 2`.", build_config())

        self.assertEqual(expected, actual)

    def test_replace_br(self):
        expected = 'Two qualities a good writer must have:\n\n- {{c1::Confidence}},\n- {{c2::Ego}}'
        actual = replace_br_tags('Two qualities a good writer must have:<br><br>- {{c1::Confidence}},<br>- {{c2::Ego}}')

        self.assertEqual(expected, actual)

    def test_markdown_conversion_with_br(self):
        expected = 'Two qualities a good writer must have: <ul> <li>{{c1::Confidence}},</li> <li>{{c2::Ego}}</li> </ul>'
        actual = convert_markdown_to_html_helper('Two qualities a good writer must have:<br><br>- {{c1::Confidence}},'
                                                 '<br>- {{c2::Ego}}', build_config())

        self.assertEqual(normalize_whitespace(expected), normalize_whitespace(actual))

    def test_that_html_tags_are_ignored(self):
        expected = r'im a <b>card</b> with <div>im in a div!</div> some latex <anki-mathjax>3\log_{b}{x}</anki-mathjax>'
        actual = convert_markdown_to_html_helper(expected, build_config())

        self.assertEqual(expected, actual)

    def test_that_escape_characters_are_not_removed(self):
        expected = r'\(3\log_{b}{x}\)'
        actual = convert_markdown_to_html_helper(expected, build_config())

        self.assertEqual(expected, actual)

    def test_blockquotes(self):
        expected = 'Here is a\n<blockquote>\nblockquote\n</blockquote>'
        actual = convert_markdown_to_html_helper(r'Here is a<br>> blockquote', build_config())

        self.assertEqual(expected, actual)

    def test_html_entity(self):
        expected = 'Here is a\n<blockquote>\nblockquote\n</blockquote>'
        actual = convert_markdown_to_html_helper(r'Here is a<br>&gt; blockquote', build_config())

        self.assertEqual(expected, actual)

    def test_that_escape_characters_are_not_removed_mixed_with_other_text(self):
        expected = r'This is some mathjax - \(3\log_{b}{x}\). isnt it cool!'
        actual = convert_markdown_to_html_helper(expected, build_config())

        self.assertEqual(expected, actual)

    def test_that_multiline_escape_characters_are_not_removed(self):
        expected = (r'This is some inline mathjax - \(3\log_{b}{x}\). and this is some multiline mathjax - \[3\log_{'
                    r'b}{x}\]')
        actual = convert_markdown_to_html_helper(expected, build_config())

        self.assertEqual(expected, actual)

    def test_that_multiline_escape_characters_with_markdown_are_not_removed(self):
        expected = (r'This is some <em>inline</em> mathjax - \(3\log_{b}{x}\). and this is some <code>multiline</code> '
                    r'mathjax - \[3\log_{b}{x}\]')
        actual = convert_markdown_to_html_helper(r'This is some *inline* mathjax - \(3\log_{b}{x}\). and this is some '
                                                 r'`multiline` mathjax - \[3\log_{b}{x}\]', build_config())

        self.assertEqual(expected, actual)

    def test_definition_lists(self):
        test_str = ("Apple\n:   Pomaceous fruit of plants of the genus Malus in the family Rosaceae.\n\nOrange\n:   "
                    "The fruit of an evergreen tree of the genus Citrus.")
        expected = ('<dl>\n<dt>Apple</dt>\n<dd>Pomaceous fruit of plants of the genus Malus in the family '
                    'Rosaceae.</dd>\n<dt>Orange</dt>\n<dd>The fruit of an evergreen tree of the genus '
                    'Citrus.</dd>\n</dl>')
        actual = convert_markdown_to_html_helper(test_str, build_config())

        self.assertEqual(expected, actual)

    def test_definition_lists_with_one_space(self):
        test_str = ("Apple\n: Pomaceous fruit of plants of the genus Malus in the family Rosaceae.\n\nOrange\n: The "
                    "fruit of an evergreen tree of the genus Citrus.")
        expected = ('<dl>\n<dt>Apple</dt>\n<dd>Pomaceous fruit of plants of the genus Malus in the family '
                    'Rosaceae.</dd>\n<dt>Orange</dt>\n<dd>The fruit of an evergreen tree of the genus '
                    'Citrus.</dd>\n</dl>')
        actual = convert_markdown_to_html_helper(test_str, build_config())

        self.assertEqual(expected, actual)

    def test_definition_lists_with_br(self):
        test_str = ("Apple<br>: Pomaceous fruit of plants of the genus Malus in the family "
                    "Rosaceae.<br><br>Orange<br>: The fruit of an evergreen tree of the genus Citrus.")
        expected = ('<dl>\n<dt>Apple</dt>\n<dd>Pomaceous fruit of plants of the genus Malus in the family '
                    'Rosaceae.</dd>\n<dt>Orange</dt>\n<dd>The fruit of an evergreen tree of the genus '
                    'Citrus.</dd>\n</dl>')
        actual = convert_markdown_to_html_helper(test_str, build_config())

        self.assertEqual(expected, actual)

    def test_definition_lists_with_cloze(self):
        test_str = ("{{c1::Apple}}\n: Pomaceous fruit of plants of the genus Malus in the family Rosaceae.\n\n{{"
                    "c2::Orange}}\n: The fruit of an evergreen tree of the genus Citrus.")
        expected = ('<dl>\n<dt>{{c1::Apple}}</dt>\n<dd>Pomaceous fruit of plants of the genus Malus in the family '
                    'Rosaceae.</dd>\n<dt>{{c2::Orange}}</dt>\n<dd>The fruit of an evergreen tree of the genus '
                    'Citrus.</dd>\n</dl>')
        actual = convert_markdown_to_html_helper(test_str, build_config())

        self.assertEqual(expected, actual)


def normalize_whitespace(text):
    """Normalize whitespace by collapsing multiple spaces and newlines into single spaces."""
    return re.sub(r'\s+', ' ', text).strip()


def build_config(
        automatic=True,
        wrap_with_p_tags=False,
        replace_non_breaking_spaces=False,
        remove_empty_divs=False,
        abbr=False,
        attr_list=False,
        def_list=True,
        fenced_code=True,
        footnotes=False,
        md_in_html=False,
        tables=True,
        admonition=False,
        codehilite=True,
        legacy_attrs=False,
        legacy_em=False,
        meta=False,
        nl2br=False,
        sane_lists=False,
        smarty=False,
        toc=False,
        wikilinks=False,
):
    """
    Configures markdown processing with the specified settings.

    Returns:
        dict: A dictionary with the markdown configuration.
    """
    return {
        "automatic": automatic,
        "wrap_with_p_tags": wrap_with_p_tags,
        "replace_non_breaking_spaces": replace_non_breaking_spaces,
        'remove_empty_divs': remove_empty_divs,
        "extensions": {
            "abbr": abbr,
            "attr_list": attr_list,
            "def_list": def_list,
            "fenced_code": fenced_code,
            "footnotes": footnotes,
            "md_in_html": md_in_html,
            "tables": tables,
            "admonition": admonition,
            "codehilite": codehilite,
            "legacy_attrs": legacy_attrs,
            "legacy_em": legacy_em,
            "meta": meta,
            "nl2br": nl2br,
            "sane_lists": sane_lists,
            "smarty": smarty,
            "toc": toc,
            "wikilinks": wikilinks,
        },
    }
