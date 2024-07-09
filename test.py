import unittest

from __init__ import *


class UnitTests(unittest.TestCase):
    def test_sanity(self):
        self.assertEqual("<p><code>x == 2</code></p>", convert_markdown_to_html("`x == 2`", None))

    def test_code_is_inserted_in_paragraph(self):
        self.assertEqual("<p>Here's some code: <code>x == 2</code>.</p>", convert_markdown_to_html("Here's some code: `x == 2`.", None))

    def test_everything_is_not_wrapped_in_h1(self):
        self.assertEqual("<h1>Heading 1</h1>\n<p>Here's some code: <code>x == 2</code>.</p>", convert_markdown_to_html("# Heading 1\nHere's some code: `x == 2`.", None))

    # def test_extension_list(self):
    #     with open(os.path.join(addon_path, 'config.json'), 'r') as file:
    #         config = json.load(file)
    #     actual = build_extension_list(config)
    #     expected = ['extra', 'smarty']
    #
    #     self.assertListEqual(expected, actual)