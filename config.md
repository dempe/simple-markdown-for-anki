### automatic

Set to `true` if you want to automatically convert Markdown to HTML (i.e., without selecting text and hitting a 
button).  Note - even in automatic mode, changes do not take effect immediately. Changes will be applied after you 
finish editing.  If you're in the browser, for example, you can hit Ctrl-N to navigate to the next card.  When you 
navigate back, your Markdown will be applied.

If `automatic` is set to `false`, you will have to manually select the Markdown that you wish to convert and hit 
either the Markdown button or the keyboard shortcut.

## wrap_with_p_tags

The [original Markdown specification](https://daringfireball.net/projects/markdown/) actually specifies that 
everything is wrapped in paragraph tags (`<p>`).  This is because Markdown's primary use is for writing documents 
where it makes sense to wrap a non-block HTML element like a code tag in a `<p>`.

Anki automatically wraps fields with `<p>`, so there is no need for this behavior.  Thus, the default value for this 
is `false`.  Set it to `true` if you would like the original behavior.

## extensions

These are various extensions to the Markdown specification that you can enable.  They add additional features such 
as code blocks and tables, for example.

## abbr

Allows text to be wrapped in an `<abbr>` tag.

Documentation [here](https://python-markdown.github.io/extensions/abbreviations/).


## attr_list

Allows you to add HTML attributes to an element.

Documentation [here](https://python-markdown.github.io/extensions/attr_list/).

## def_list

Create definition lists in Markdown.

Documentation [here](https://python-markdown.github.io/extensions/definition_lists/).

## fenced_code

This is an important one.  Allows for adding codeblocks via three backticks or three tildas (```` ``` ````, `~~~`).  
It also allows you to add a language class to your code blocks.

Documentation [here](https://python-markdown.github.io/extensions/fenced_code_blocks/).

## footnotes

Add footnotes via Markdown.

Documentation [here](https://python-markdown.github.io/extensions/footnotes/).

## md_in_html

By default, Markdown ignores any content within a raw HTML block-level element. With the md-in-html extension 
enabled, the content of a raw HTML block-level element can be parsed as Markdown.

Documentation [here](https://python-markdown.github.io/extensions/md_in_html/).

## tables

Another pretty useful one.  Write tables via Markdown.

Documentation [here](https://python-markdown.github.io/extensions/tables/).

## admonition

Documentation [here](https://python-markdown.github.io/extensions/admonition/).

## codehilite

Allows for lots of code syntax highlighting customizations.  All via Markdown!

Documentation [here](https://python-markdown.github.io/extensions/code_hilite/).

## legacy_attrs

Restores Python-Markdown’s original attribute setting syntax.

Documentation [here](https://python-markdown.github.io/extensions/legacy_attrs/).

## legacy_em

Restores Markdown’s original behavior for emphasis and strong syntax when using underscores.

Documentation [here](https://python-markdown.github.io/extensions/legacy_em/).

## meta

Add a YAML metadata block.  Not sure why this would be useful in Anki.

Documentation [here](https://python-markdown.github.io/extensions/meta_data/).

## nl2br
"Cause newlines to be treated as hard breaks; like StackOverflow and GitHub flavored Markdown do."

Documentation [here](https://python-markdown.github.io/extensions/nl2br/).

## sane_lists

Changes Markdown's list-parsing behavior to be "less surprising".

Documentation [here](https://python-markdown.github.io/extensions/sane_lists/).

## smarty

"The SmartyPants extension converts ASCII dashes, quotes and ellipses to their HTML entity equivalents."

Documentation [here](https://python-markdown.github.io/extensions/smarty/).

## toc

Add a table of contents to your cards.  Not sure why you would ever need this in Anki.

Documentation [here](https://python-markdown.github.io/extensions/toc/).

## wikilinks

Add wiki-style links.

Documentation [here](https://python-markdown.github.io/extensions/wikilinks/).
