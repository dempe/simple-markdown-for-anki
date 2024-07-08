from aqt import gui_hooks
from .markdown_converter import convert_markdown_to_html

gui_hooks.editor_will_munge_html.append(replace_all_backticks)
