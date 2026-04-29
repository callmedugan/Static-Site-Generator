from enum import Enum
from src.leafnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "link"
    IMG = "image"

class TextNode:
    def __init__(self, text:str, text_type:TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    # called when using == comparison
    def __eq__(self, other) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    # called when trying to show a string representation of instance
    def __repr__(self) -> str:
        if not self.url:
            return f"TextNode({self.text}, {self.text_type.value})"
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
#converts a text_node into a leaf node - this will be called after the markdown is split
def text_node_to_html_node(text_node:TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMG:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text,})
        case _:
            raise Exception(f"invalid text node type: {text_node.text_type}")
        

text_type_char_dict = {
    TextType.BOLD : "**",
    TextType.ITALIC : "_",
    TextType.CODE : "`"
}
# Takes a list of "old nodes" and a text type.
# It should return a new list of nodes, where any "text" type nodes in the input list are (potentially)
# split into multiple nodes based on the syntax. 
def split_nodes(old_nodes:list[TextNode], text_type:TextType) -> list[TextNode]:
    if text_type not in text_type_char_dict:
        raise ValueError(f"cannot split node with invalid text type of {text_type}")
    
    result = []
    delimiter = text_type_char_dict[text_type]

    # loop through the given list of nodes and start splitting
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        #check for opening and closing markdown
        split = node.text.split(delimiter)
        if len(split) % 2 == 0:
            raise Exception(f"{node.text} is not valid markdown")
        #loop through the split text
        is_text = True
        for s in split:
            if len(s) != 0:
                result.append(TextNode(s, TextType.TEXT) if is_text else TextNode(s, text_type))
            is_text = not is_text
    return result

# returns list of tuples (alt text, url)
def extract_markdown_images(text:str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

# returns list of tuples (anchor text, url)
def extract_markdown_links(text:str) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

# split raw markdown text into TextNodes based on images and links
def split_nodes_image(old_nodes:list[TextNode]) -> list[TextNode]:
    result = []

    for node in old_nodes:
        #skip text nodes
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        #pull out all the tuples for each node
        img_tuples = extract_markdown_images(node.text)
        #keep splitting the same string
        node_text_string = node.text

        for img in img_tuples:
            #split in 2 sections
            sections = node_text_string.split(f"![{img[0]}]({img[1]})", 1)
            #add the first half
            if len(sections[0]) > 0:
                result.append(TextNode(sections[0], TextType.TEXT))
            #add the img in the middle
            result.append(TextNode(img[0], TextType.IMG, img[1]))
            #update the string to split net iteration if there was still more text on the end
            node_text_string = "" if len(sections) == 1 else sections[1]

        #create another node if there was more text
        if len(node_text_string) > 0:
            result.append(TextNode(node_text_string, TextType.TEXT))

    return result

def split_nodes_link(old_nodes:list[TextNode]) -> list[TextNode]:
    result = []

    for node in old_nodes:    
        #skip text nodes
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        #pull out all the tuples for each node
        link_tuples = extract_markdown_links(node.text)
        #keep splitting the same string
        node_text_string = node.text
        
        for link in link_tuples:
            #split in 2 sections
            sections = node_text_string.split(f"[{link[0]}]({link[1]})", 1)
            #add the first half
            if len(sections[0]) > 0:
                result.append(TextNode(sections[0], TextType.TEXT))
            #add the link in the middle
            result.append(TextNode(link[0], TextType.LINK, link[1]))
            #update the string to split net iteration if there was still more text on the end
            node_text_string = "" if len(sections) == 1 else sections[1]

        #create another node if there was more text
        if len(node_text_string) > 0:
            result.append(TextNode(node_text_string, TextType.TEXT))

    return result

# Time to put all the "splitting" functions together into a
# function that can convert a raw string of markdown-flavored text into a list of TextNode object
def text_to_textnodes(text:str) -> list[TextNode]:
    result = [TextNode(text, TextType.TEXT)]
    result = split_nodes(result, TextType.BOLD)
    result = split_nodes(result, TextType.ITALIC)
    result = split_nodes(result, TextType.CODE)
    result = split_nodes_image(result)
    result = split_nodes_link(result)
    return result