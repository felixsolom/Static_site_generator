import unittest
from split_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType

class test_split_node_delimiter(unittest.TestCase):
    def test_bold(self):
        node = TextNode("this is **a** test for a **bold delimiter**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        expected = [
            TextNode("this is ", TextType.TEXT),
            TextNode("a", TextType.BOLD),
            TextNode(" test for a ", TextType.TEXT),
            TextNode("bold delimiter", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_italic(self):
        node = TextNode("this is _a_ test for a _italic delimiter_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
        expected = [
            TextNode("this is ", TextType.TEXT),
            TextNode("a", TextType.ITALIC),
            TextNode(" test for a ", TextType.TEXT),
            TextNode("italic delimiter", TextType.ITALIC)
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_code(self):
        node = TextNode("this is 'a' test for a 'code delimiter'", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "'", TextType.CODE)
        expected = [
            TextNode("this is ", TextType.TEXT),
            TextNode("a", TextType.CODE),
            TextNode(" test for a ", TextType.TEXT),
            TextNode("code delimiter", TextType.CODE)
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_unclosed_delimiter(self):
        node = TextNode("this is 'a' test for a 'code delimiter", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "'", TextType.CODE)
        expected = "delimiter ' not properly closed in text: this is 'a' test for a 'code delimiter"
        self.assertEqual(str(context.exception), expected)
        
    def test_not_text_type_text(self):
        node = TextNode("this is already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("this is already bold", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_multiple_nodes(self):
        node = TextNode("this is 'a' test for a 'code delimiter'", TextType.TEXT)
        node2 = TextNode("this is also 'a' test for a 'code delimiter'", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "'", TextType.CODE)
        expected = [
            TextNode("this is ", TextType.TEXT),
            TextNode("a", TextType.CODE),
            TextNode(" test for a ", TextType.TEXT),
            TextNode("code delimiter", TextType.CODE),
            
            TextNode("this is also ", TextType.TEXT),
            TextNode("a", TextType.CODE),
            TextNode(" test for a ", TextType.TEXT),
            TextNode("code delimiter", TextType.CODE)
        ]
        self.assertEqual(new_nodes, expected)
    