from enum import Enum
from htmlnode import *
from textnode import *
from leafnode import *
from parentnode import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class Block:
    # we want a block to store a string, type, and an html parsed value
    def __init__(self, text:str) -> None:
        self.type = BlockType.PARAGRAPH # default to paragraph
        # store single element, html parent tags, and the children strings
        self.__html = ""
        self.__html_tag = ""
        self.__html_children_tag = ""
        self.__html_children = []

        lines = text.split("\n")

        # headings
        if text.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
            self.type = BlockType.HEADING
            strip = text.lstrip('#')
            h_tag_num = len(text) - len(strip)
            self.__html = strip.strip()
            self.__html_tag = "h" + str(h_tag_num)

        # code
        elif text.startswith("```") and text.endswith("```"):
            self.type = BlockType.CODE
            #strip the ``` away
            # remove \n and leading whitespace
            strip = text.strip("`").strip("\n")
            split = strip.split("\n")
            for s in range(len(split)):
                split[s] = split[s].lstrip()
            self.__html_tag = "pre"
            self.__html_children_tag = "code"
            self.__html_children.append("\n".join(split))

        # all lines start with >
        elif all(line.startswith(">") for line in lines):
            self.type = BlockType.QUOTE
            self.__html = text.replace("> ", "")
            self.__html_tag = "blockquote"

        # ordered lists
        elif all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
            self.type = BlockType.ORDERED_LIST
            # replace both numbers by splitting at first " " and add li closing tag
            for line in lines:
                self.__html_children.append(line.split(" ", 1)[1])
            self.__html_tag = "ol"
            self.__html_children_tag = "li"

        # unordered lists
        elif all(line.startswith(("* ", "- ")) for line in lines):
            self.type = BlockType.UNORDERED_LIST
            # remove both * or - 
            for line in lines:
                clean_text = line.replace("* ", "").replace("- ", "")
                self.__html_children.append(clean_text)
            self.__html_tag = "ul"
            self.__html_children_tag = "li"

        # default to paragraph
        else:
            self.type = BlockType.PARAGRAPH
            # remove \n and leading whitespace
            split = text.split("\n")
            for s in range(len(split)):
                split[s] = split[s].lstrip()
            self.__html = " ".join(split)
            self.__html_tag = "p"

    # returns either the single html element and tag or the parent/children
    def get_html_elements(self) -> dict:
        return {
            "text": self.__html,
            "tag": self.__html_tag,
            "children_tag": self.__html_children_tag,
            "children": self.__html_children
            }

# takes a raw Markdown string (representing a full document) as input and returns a list of strings
def markdown_to_strings(markdown:str) -> list[str]:
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

# converts a full markdown document into a single parent HTMLNode
def markdown_to_html_node(markdown:str) -> ParentNode:
    elements = []
    #convert to strings
    split_strings = markdown_to_strings(markdown)
    for split_string in split_strings:
        # create block to parse the string
        new_block = Block(split_string)
        new_block_html = new_block.get_html_elements()
        # handle the code case first - bypassing the parsing
        if new_block.type == BlockType.CODE and new_block_html["children"]:
            child = LeafNode(new_block_html["children_tag"], new_block_html["children"][0])
            elements.append(ParentNode(new_block_html["tag"], [child]))

        # build the children and parents
        elif new_block_html["children"]:
            child_nodes = []
            for child_text in new_block_html["children"]:
                child_text_nodes = text_to_textnodes(child_text)
                for c in child_text_nodes:
                    new_leaf_node = text_node_to_html_node(c)
                    # spaghetti code ugh
                    if new_leaf_node.tag != new_block_html["children_tag"]:
                        child_nodes.append(ParentNode(new_block_html["children_tag"],[new_leaf_node]))
                    else:
                        child_nodes.append(new_leaf_node)
            elements.append(ParentNode(new_block_html["tag"], child_nodes))

        # else just build the single element
        else:
            child_nodes = []
            text_nodes = text_to_textnodes(new_block_html["text"])
            for node in text_nodes:
                child_nodes.append(text_node_to_html_node(node))
            elements.append(ParentNode(new_block_html["tag"], child_nodes))

    # return the parent div        
    return ParentNode("div", elements)