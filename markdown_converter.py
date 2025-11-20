import json
import re
import os
from typing import List
from markdown_core import convert_markdown_to_html_helper
from aqt import gui_hooks
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

def convert_markdown_to_html(md: str, _: Editor) -> str:
    return convert_markdown_to_html_helper(md, mw.addonManager.getConfig(__name__))


addHook("setupEditorButtons", add_markdown_button)

if mw.addonManager.getConfig(__name__)['automatic']:
    gui_hooks.editor_will_munge_html.append(convert_markdown_to_html)
