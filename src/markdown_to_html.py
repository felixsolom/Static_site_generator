from block_markdown import markdown_to_blocks, block_to_blocktype
from block_markdown import BlockType
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
import re

def text_nodes_to_html_nodes(text_nodes):
    return [text_node_to_html_node(text_node) for text_node in text_nodes]

def markdown_to_html(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in markdown_blocks:
        if not block.strip():
            continue
        block_type = block_to_blocktype(block)
        
        if block_type == BlockType.PARAGRAPH:
            html_blocks.append(paragraph_to_html(block))
        elif block_type == BlockType.QUOTE:
            html_blocks.append(quote_to_html(block))
        elif block_type == BlockType.HEADING:
            html_blocks.append(header_to_html(block))
        elif block_type == BlockType.ORDERED_LIST:
            html_blocks.append(ordered_list_to_html(block))
        elif block_type == BlockType.UNORDERED_LIST:
            html_blocks.append(unordered_list_to_html(block))
        elif block_type == BlockType.CODE:
            html_blocks.append(code_to_html(block))     
        
    return ParentNode("div", html_blocks)
       
        
def paragraph_to_html(block):
    block = block.replace('\n', ' ')
    text_nodes = text_to_textnodes(block)
    html_nodes = text_nodes_to_html_nodes(text_nodes)
    return ParentNode("p", html_nodes)

def quote_to_html(block):
    lines = block.split('\n')
    cleaned_lines = []
    for line in lines:
        if line.startswith('>'):
            cleaned_lines.append(line[1:].strip())
        else:
            cleaned_lines.append(line)
    cleaned_block = '\n'.join(cleaned_lines)
    text_nodes = text_to_textnodes(cleaned_block)
    html_nodes = text_nodes_to_html_nodes(text_nodes)
    return ParentNode("blockquote", html_nodes)

def code_to_html(block):
    lines = block.split('\n')
    if lines and lines[0].startswith('```'):
        lines = lines[1:]
    if lines and lines[-1].strip() == '```':
        lines = lines[:-1]
    code_content = '\n'.join(lines)
    return ParentNode("pre", [LeafNode("code", code_content)])

def unordered_list_to_html(block):
    items = block.split('\n')
    list_items = []
    for item in items:
        item_text = item.strip()
        if item_text.startswith('* '):
            item_text = item_text[2:]
        elif item_text.startswith('- '):
            item_text = item_text[2:]
        text_nodes = text_to_textnodes(item_text)
        html_nodes = text_nodes_to_html_nodes(text_nodes)
        list_items.append(ParentNode("li", html_nodes))    
    return ParentNode("ul", list_items)

def ordered_list_to_html(block):
    items = block.split('\n')
    list_items = []
    pattern = r"^\d+\.\s+"
    for item in items:
        item_text = item.strip()
        if re.match(pattern, item_text):
            item_text = re.sub(pattern, '', item_text)
        text_nodes = text_to_textnodes(item_text)
        html_nodes = text_nodes_to_html_nodes(text_nodes)    
        list_items.append(ParentNode("li", html_nodes))
    return ParentNode("ol", list_items)

def header_to_html(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
        
    content = block[level:].strip()
    text_nodes = text_to_textnodes(content)
    html_nodes = text_nodes_to_html_nodes(text_nodes)
    return ParentNode(f"h{level}", html_nodes)

def extract_title(markdown):
    pattern = r"^#\s+(.+)$"
    
    for line in markdown.split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            return match.group(1).strip()  
        
    raise ValueError("There is no title to this file")
    