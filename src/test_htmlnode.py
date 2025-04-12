import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(None, None, None, {
    "href": "https://www.google.com",
    "target": "_blank",
})
        expected_outcome = f' href="https://www.google.com" target="_blank"'
        self.assertEqual(HTMLNode.props_to_html(node), expected_outcome)
        
    def test_repr(self):
        node = HTMLNode("p", "this is a test", "test, test", None)
        expected = "HTMLNode(p, this is a test, children: test, test, {})"
        self.assertEqual(HTMLNode.__repr__(node), expected)
        
    def test_raises_not_implemented_error(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            HTMLNode.to_html(node)
            
class testLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_pros(self):
        node = LeafNode("a", "Hi, everyone!", {"href": "https://www.hello.world"})
        self.assertEqual(node.to_html(), '<a href="https://www.hello.world">Hi, everyone!</a>')
        
    def test_value(self):
        node = LeafNode("div", "wish you were here", {"Heaven": "From hell"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "wish you were here")
        node.props_to_html == '"Heaven="From hell"'
        
class testParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_to_html_with_grand_grandchildren(self):
        grand_grandchild_node = LeafNode("a", "grand_grandchild")
        grandchild_node = ParentNode("b", [grand_grandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b><a>grand_grandchild</a></b></span></div>",
        )
        
    def test_to_html_with_grand_grandchildren2(self):
        grand_grandchild_node1 = LeafNode("a", "grand_grandchild1")
        grand_grandchild_node2 = LeafNode("a", "grand_grandchild2")
        grandchild_node = ParentNode("b", [grand_grandchild_node1, grand_grandchild_node2])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b><a>grand_grandchild1</a><a>grand_grandchild2</a></b></span></div>",
        )
        
class test_text_node_to_html_node(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
 
    def test_text_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
 
    def test_text_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
 
    def test_text_link(self):
        node = TextNode("This is a text node", TextType.LINK, "www.felix.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "www.felix.com"})
 
                
if __name__ == "__main__":
    unittest.main()