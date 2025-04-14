import unittest
from block_markdown import markdown_to_blocks, block_to_blocktype, BlockType

class test_markdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks_2(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    1. This is an ordered list
    2. with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "1. This is an ordered list\n2. with items",
            ],
        )
        
class test_blocks_to_blocktype(unittest.TestCase):
    def test_heading(self):
        md = """
        #CHAPTER I.
        Down the Rabbit-Hole
        
        """
        block = block_to_blocktype(md)
        self.assertEqual(
            block,
            BlockType.HEADING
        )
    def test_code(self):
        md = """
        ```##CHAPTER I.
        Down the Rabbit-Hole```
        
        """
        block = block_to_blocktype(md)
        self.assertEqual(
            block,
            BlockType.CODE
        )
    def test_quote(self):
        md = """
        >Alice was beginning to get very tired of sitting by her sister on the
        >bank, and of having nothing to do: once or twice she had peeped into
        >the book her sister was reading, but it had no pictures or
        >conversations in it, “and what is the use of a book,” thought Alice
        >'without pictures or conversations?'
        """
        block = block_to_blocktype(md)
        self.assertEqual(
            block,
            BlockType.QUOTE
        )
    def test_unordered_list(self):
        md = """
        -  Alice was beginning to get very tired of sitting by her sister on the
        - bank, and of having nothing to do: once or twice she had peeped into
        - the book her sister was reading, but it had no pictures or
        - conversations in it, “and what is the use of a book,” thought Alice
        - 'without pictures or conversations?'
        """
        block = block_to_blocktype(md)
        self.assertEqual(
            block,
            BlockType.UNORDERED_LIST
        )
    def test_ordered_list(self):
        md = """
        1. Alice was beginning to get very tired of sitting by her sister on the
        2. bank, and of having nothing to do: once or twice she had peeped into
        3. the book her sister was reading, but it had no pictures or
        4. conversations in it, “and what is the use of a book,” thought Alice
        5. 'without pictures or conversations?'
        """
        block = block_to_blocktype(md)
        self.assertEqual(
            block,
            BlockType.ORDERED_LIST
        )
    def test_paragraph(self):
        md = """
        Alice was beginning to get very tired of sitting by her sister on the
        2. bank, and of having nothing to do: once or twice she had peeped into
        the book her sister was reading, but it had no pictures or
        4. conversations in it, “and what is the use of a book,” thought Alice
        5. 'without pictures or conversations?'
        """
        block = block_to_blocktype(md)
        self.assertEqual(
            block,
            BlockType.PARAGRAPH
        )
        
    if __name__ == "__main__":
        unittest.main()