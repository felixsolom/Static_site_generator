import unittest
from markdown_to_html import markdown_to_html, extract_title

class test_md_to_html(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )
    
class test_extract_title(unittest.TestCase):
    def test_title_extraction(self):
        md = """
        # Alice
        1. Alice was beginning to get very tired of sitting by her sister on the
        2. bank, and of having nothing to do: once or twice she had peeped into
        3. the book her sister was reading, but it had no pictures or
        4. conversations in it, “and what is the use of a book,” thought Alice
        5. 'without pictures or conversations?'
        """
        title = extract_title(md)
        self.assertEqual(title, "Alice")
        
    def test_title_extraction_2(self):
        md = """  
        # Wonder
        ## Land
        1. Alice was beginning to get very tired of sitting by her sister on the
        2. bank, and of having nothing to do: once or twice she had peeped into
        3. the book her sister was reading, but it had no pictures or
        4. conversations in it, “and what is the use of a book,” thought Alice
        5. 'without pictures or conversations?'
        """
        title = extract_title(md)
        self.assertEqual(title, "Wonder")
        