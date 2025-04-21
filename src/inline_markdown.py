from textnode import TextNode, TextType
import re

DELIMITER_TO_TYPE = {
    "**": TextType.BOLD,
    "_": TextType.ITALIC,
    "`": TextType.CODE
}

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if delimiter not in DELIMITER_TO_TYPE:
        raise ValueError(f"Invalid markdown syntax: {delimiter}")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue 
        split_nodes  = []
        if delimiter in node.text:
            splited_node = node.text.split(delimiter)
            num_of_delimiters = len(splited_node) - 1
            if num_of_delimiters % 2 != 0:
                raise Exception(f"delimiter {delimiter} not properly closed in text: {node.text}")
            for i, segment in enumerate(splited_node):
                if segment:
                    new_node_type = text_type if i % 2 == 1 else TextType.TEXT
                    split_nodes.append(TextNode(segment, new_node_type))
        else:
            split_nodes.append(node)
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((https?:\/\/[^\s)]+|\/[^\s)]+|\.\/[^\s)]+|[^\s)]+)\)"
, text)
    return matches 

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((https?:\/\/[^\s)]+|\/[^\s)]+)\)"
 ,text)
    return matches 

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extracted_links = extract_markdown_links(node.text)
        if not extracted_links:
            new_nodes.append(node)
            continue    
        split_nodes = []
        current_text = node.text
        for link_alt, link in extracted_links:
            link_marker = f"[{link_alt}]({link})"
            parts = current_text.split(link_marker, 1)
            
            if parts[0]:
                split_nodes.append(TextNode(parts[0], TextType.TEXT))
            split_nodes.append(TextNode(link_alt, TextType.LINK, link))
            
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
        if current_text:
            split_nodes.append(TextNode(current_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extracted_links = extract_markdown_images(node.text)
        if not extracted_links:
            new_nodes.append(node)
            continue    
        split_nodes = []
        current_text = node.text
        for image_alt, image_link in extracted_links:
            link_marker = f"![{image_alt}]({image_link})"
            parts = current_text.split(link_marker, 1)
            
            if parts[0]:
                split_nodes.append(TextNode(parts[0], TextType.TEXT))
            split_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
        if current_text:
            split_nodes.append(TextNode(current_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    for delimiter, text_type in DELIMITER_TO_TYPE.items():
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
        
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes           
    
        
    


        
       