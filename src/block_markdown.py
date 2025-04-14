from enum import Enum
import re 


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
def block_to_blocktype(block):
    block = block.strip()
    if re.match(r'^#{1,6}', block):
        return BlockType.HEADING 
    if (block.startswith("```") and  
        block.endswith("```")):
            return BlockType.CODE
    lines = block.splitlines()
    count = 0
    for line in lines:
        line = line.strip()
        if line.startswith('>'): 
            count += 1
    if len(lines) == count:
        return BlockType.QUOTE
    count = 0
    for line in lines:
        line = line.strip()
        if line.startswith('- '):
            count += 1
        if len(lines) == count:
            return BlockType.UNORDERED_LIST
    count = 0
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith(f"{i + 1}. "):
            count += 1
        if len(lines) == count:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
             

def markdown_to_blocks(markdown):
    split_blocks = markdown.split('\n\n')
    listed_blocks = []
    for block in split_blocks:
        if block:
            block = block.strip()
            split_block = block.split('  ')
            rejoined_block = ('').join(split_block)
            listed_blocks.append(rejoined_block)
        
    return listed_blocks
    