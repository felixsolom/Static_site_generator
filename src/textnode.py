from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    text_content = text_node.text
    text_type = text_node.text_type
    match text_type:
        case TextType.TEXT:
            return LeafNode(None, text_content)
        case TextType.BOLD:
            return LeafNode("b", text_content) 
        case TextType.ITALIC:
            return LeafNode("i", text_content)     
        case TextType.CODE:
            return LeafNode("code", text_content)     
        case TextType.LINK:
            return LeafNode("a", text_content, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_content}) 
        case _:
            raise Exception("Text node must be of valid type")    
    
        
        


