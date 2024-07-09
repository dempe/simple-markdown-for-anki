## Overview

Anki addon that allows you to type your notes in Markdown and have it automatically converted to HTML.  NOTE: this happens only when you are finished editing, not as you are typing.  You need to close the editor, or if you're in the browser, navigate to the next card (`Ctrl-Shift-N`) then back.  You should then see the changes.

If you don't want your notes to be automatically converted, you can use the Markdown button provided.  Select the Markdown text you want to convert, and hit the button.

Also includes various Markdown extensions that can be enabled or disabled as you like.  [config.md](https://github.com/dempe/simple-markdown-for-anki/blob/main/config.md) has more info.

## Goal

The goal of this addon was to keep things as simple as possible.  All the other Markdown addons were too cumbersome and complex for me. I just wanna write my notes in Markdown and forget I have this addon installed.  I think I've accomplished that.  All the functionality is provided in 60 lines of Python.

## A note on code blocks (or any other multi-line Markdown syntax)

As of January 2024 (I haven't checked the exact version), the Anki editor regrettably inserts `<br>` tags when ever you hit `Enter`.  This really messes with the Markdown formatting, especially for code blocks.  The workaround that I use is to type my code blocks in the editor's HTML editor (`Ctrl-Shift-X`).  The HTML editor does not insert  `<br>` tags, though entering Markdown in the HTML editor is kinda ironic.

## Another note on code blocks and syntax highlighting

The `fenced_code` extension (enabled by default) allows you to enter code blocks.  Moreover, you can specify the language of the code like in Github flavored Markdown.  ````` ```php ```` will produce `<pre><code class="language-php">`.  This allows you to include syntax highlighting for your code blocks.

FWIW, to install a syntax highlighter:

- Copy the downloaded JS code into your `collection.media` directory (for example, `highlight.min.js`)
- Prefix the JS library name with `_` (for example, `highlight.min.js` -> `_highlight.min.js`).
  - This is so Anki doesn't try to delete it since it's not being referenced by any field.
- Copy an associated CSS file for styling and also prefix it with an `_` (e.g., `_github-dark.min.css`)
- Edit your cards to call the JS library and load the CSS like so:

```html
<link rel="stylesheet" href="_github-dark.min.css">
<script src="_highlight.min.js"></script>
<script>hljs.highlightAll();</script>
```
