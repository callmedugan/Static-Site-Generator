from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

## takes a single block of markdown text as input and returns the BlockType representing the type of block it is
def block_to_block_type(text:str) -> BlockType:
    lines = text.split("\n")
    # headings
    if text.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    # code
    if text.startswith("```") and text.endswith("```"):
        return BlockType.CODE
    # all lines start with >
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    #ordered lists
    if all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    #unordered lists
    if all(line.startswith(("* ", "- ")) for line in lines):
        return BlockType.UNORDERED_LIST
    return BlockType.PARAGRAPH






# takes a raw Markdown string (representing a full document) as input and returns a list of "block" strings
def markdown_to_blocks(markdown:str) -> list[str]:
    result = []
    #split on double newlines
    split = markdown.split("\n\n")
    for s in split:
        #remove whitespace
        s = s.strip()
        if len(s) == 0:
            continue
        result.append(s)

    return result