import json
import re
from typing import List
from aqt import gui_hooks
import markdown
from bs4 import BeautifulSoup
from anki.hooks import addHook
from aqt.editor import Editor
from aqt.qt import *
from aqt import mw

addon_path = os.path.dirname(__file__)
br_pattern = re.compile(r'<br>')
nbsp_pattern = re.compile(r'&nbsp;')
mathjax_pattern = re.compile(r'(\\\(.+?\\\)|\\\[.+?\\\])')
gt_pattern = re.compile(r'&gt;')


def convert_selection(editor: Editor) -> None:
    html = convert_markdown_to_html_helper(editor.web.selectedText(), mw.addonManager.getConfig(__name__))
    js = "setTimeout(function() { document.execCommand('%s', false, %s); }, 40); " % ("insertHTML", json.dumps(html))

    editor.web.eval(js)


def add_markdown_button(buttons: List[str], editor: Editor) -> List[str]:
    button = editor.addButton(os.path.join(addon_path, 'markdown-logo.svg'), "test", convert_selection)
    buttons.append(button)
    return buttons


def remove_p_tags(html: str) -> str:
    """Remove all <p> tags from output HTML. See config.json for more info."""
    soup = BeautifulSoup(html, 'html.parser')

    for p in soup.find_all('p'):
        p.unwrap()

    return str(soup)


def replace_br_tags(md: str) -> str:
    """The Editor loves to add in <br> whenever it gets the chance. This breaks Markdown parsing"""
    return br_pattern.sub('\n', md)


def replace_gt_entities(md: str) -> str:
    """The Editor converts `>` to `&gt;`. This breaks Markdown parsing"""
    return gt_pattern.sub('>', md)


def replace_nbsp(md: str) -> str:
    """The editor inserts non-breaking spaces (&nbsp;) with aplomb. We convert these to regular spaces, because they
    break Markdown parsing"""
    return nbsp_pattern.sub(' ', md)


def convert_markdown_to_html_helper(md: str, config: dict) -> str:
    if '<anki-mathjax>' in md or re.search(mathjax_pattern, md):
        return md

    extensions = [f"markdown.extensions.{key}" for key, value in config['extensions'].items() if value]
    md = replace_gt_entities(replace_br_tags(md))

    if config['replace_non_breaking_spaces']:
        md = replace_nbsp(md)

    # We have to process the text in parts, because Anki uses \(\) and \[\] for Mathjax delimiters. markdown.markdown
    # will remove the backslashes.  Hence, we split the string based on these delimiters and ignore the text
    # contained within them.
    parts = re.split(mathjax_pattern, md)
    processed_parts = []
    for part in parts:
        if mathjax_pattern.match(part):
            processed_parts.append(part)
            continue
        processed_parts.append(markdown.markdown(part, extensions=extensions))

    html = ''.join(processed_parts)

    if config['wrap_with_p_tags']:
        return html
    return remove_p_tags(html)


def convert_markdown_to_html(md: str, _: Editor) -> str:
    return convert_markdown_to_html_helper(md, mw.addonManager.getConfig(__name__))


addHook("setupEditorButtons", add_markdown_button)

if mw.addonManager.getConfig(__name__)['automatic']:
    gui_hooks.editor_will_munge_html.append(convert_markdown_to_html)
