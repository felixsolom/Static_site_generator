import unittest
from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes

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
        node = TextNode("this is `a` test for a `code delimiter`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("this is ", TextType.TEXT),
            TextNode("a", TextType.CODE),
            TextNode(" test for a ", TextType.TEXT),
            TextNode("code delimiter", TextType.CODE)
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_unclosed_delimiter(self):
        node = TextNode("this is `a` test for a `code delimiter", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        expected = "delimiter ` not properly closed in text: this is `a` test for a `code delimiter"
        self.assertEqual(str(context.exception), expected)
        
    def test_not_text_type_text(self):
        node = TextNode("this is already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("this is already bold", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_multiple_nodes(self):
        node = TextNode("this is `a` test for a `code delimiter`", TextType.TEXT)
        node2 = TextNode("this is also `a` test for a `code delimiter`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
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
        
class test_extract_md_images_links(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links_faulty(self):
        matches = extract_markdown_links(
            "This is text with a ![link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)
        
class test_split_link_and_images(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
    )
        
    def test_split_links_just_link(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
    )
    
    def test_split_links_just_text(self):
        node = TextNode(
            "This is text without a link and another with broken link [second link](https://i.imgur.com/3elNhQu.png",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text without a link and another with broken link [second link](https://i.imgur.com/3elNhQu.png", TextType.TEXT),
            ],
            new_nodes,
    )
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_images_link_leading(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_images_link_broken(self):
        node = TextNode(
            "!image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("!image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
            ],
            new_nodes,
        )
        
class test_text_to_textnode_full_action(unittest.TestCase):
    def test_regular_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
],
            new_nodes
        )
        
    def test_regular_text_2(self):
        text = "This is _text_ with an **bold** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.ITALIC),
    TextNode(" with an ", TextType.TEXT),
    TextNode("bold", TextType.BOLD),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
],
            new_nodes
        )
            
if __name__ == "__main__":
    unittest.main()
    