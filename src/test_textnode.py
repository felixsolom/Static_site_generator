import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test2_eq(self):
        node = TextNode("This is a test", TextType.IMAGE)
        node2 = TextNode("This is a test", TextType.IMAGE)
        self.assertEqual(node, node2)
        
    def test3_eq(self):
        node = TextNode("This is a test", TextType.LINK, None)
        node2 = TextNode("This is a test", TextType.LINK, None)
        self.assertEqual(node, node2)
        
    def test4_eq(self):
        node = TextNode("This is a test", TextType.LINK, None)
        node2 = TextNode("This is a test", TextType.BOLD, None)
        self.assertNotEqual(node, node2)
        
    def test5_eq(self):
        node = TextNode("This is a test", TextType.ITALIC, "https://www.net.com")
        node2 = TextNode("This is a test", TextType.ITALIC, "www.net.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()