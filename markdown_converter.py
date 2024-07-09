import json
import re
from typing import List
from aqt import gui_hooks
import markdown
from bs4 import BeautifulSoup
from anki.hooks import addHook
from aqt.editor import Editor
from aqt.qt import *


addon_path = os.path.dirname(__file__)
br_pattern = re.compile(r'<br>')


def load_meta():
    with open(os.path.join(addon_path, 'meta.json'), 'r') as file:
        return json.load(file)


def convert_selection(editor: Editor) -> None:
    html = convert_markdown_to_html_helper(editor.web.selectedText())
    js = "setTimeout(function() { document.execCommand('%s', false, %s); }, 40); " % ("insertHTML", json.dumps(html))

    editor.web.eval(js)


def add_markdown_button(buttons: List[str], editor: Editor) -> List[str]:
    button = editor.addButton(os.path.join(addon_path, 'markdown-logo.svg'), "test", convert_selection)
    buttons.append(button)
    return buttons


def remove_p_tags(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    for p in soup.find_all('p'):
        p.unwrap()

    return str(soup)


def replace_br_tags(md: str) -> str:
    """The Editor loves to add in <br> whenever it gets the chance.  This breaks Markdown"""
    return br_pattern.sub('\n', md)


def convert_markdown_to_html_helper(md: str, meta: dict) -> str:
    config = meta['config']
    extensions = [f"markdown.extensions.{key}" for key, value in config['extensions'].items() if value]
    html = markdown.markdown(replace_br_tags(md), extensions=extensions)

    if config['wrap_with_p_tags']:
        return html
    return remove_p_tags(html)


def convert_markdown_to_html(md: str, _: Editor) -> str:
    return convert_markdown_to_html_helper(md, load_meta())


addHook("setupEditorButtons", add_markdown_button)

if load_meta()['config']['automatic']:
    gui_hooks.editor_will_munge_html.append(convert_markdown_to_html)