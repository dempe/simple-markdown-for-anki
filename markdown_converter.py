import json
from typing import List
from aqt import gui_hooks
import markdown
from bs4 import BeautifulSoup
from anki.hooks import addHook
from aqt.editor import Editor
from aqt.qt import *


addon_path = os.path.dirname(__file__)


def load_config():
    with open(os.path.join(addon_path, 'config.json'), 'r') as file:
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


def convert_markdown_to_html_helper(md: str) -> str:
    config = load_config()
    extensions = [f"markdown.extensions.{key}" for key, value in config['extensions'].items() if value]
    html = markdown.markdown(md, extensions=extensions)

    if config['wrap_with_p_tags']:
        return html
    return remove_p_tags(html)


def convert_markdown_to_html(md: str, _: Editor) -> str:
    return convert_markdown_to_html_helper(md)


addHook("setupEditorButtons", add_markdown_button)

if load_config()['automatic']:
    gui_hooks.editor_will_munge_html.append(convert_markdown_to_html)