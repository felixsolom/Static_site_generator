import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(None, None, None, {
    "href": "https://www.google.com",
    "target": "_blank",
})
        expected_outcome = f'href="https://www.google.com" target="_blank"'
        self.assertEqual(HTMLNode.props_to_html(node), expected_outcome)