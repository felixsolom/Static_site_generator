from textnode import TextNode, TextType

DELIMITER_TO_TYPE = {
    "**": TextType.BOLD,
    "_": TextType.ITALIC,
    "'": TextType.CODE
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
        new_nodes.extend(split_nodes)
    return new_nodes
                     