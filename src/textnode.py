from enum import Enum
from src.leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "link"
    IMG = "image"

class TextNode:
    def __init__(self, text, text_type:TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    # called when using == comparison
    def __eq__(self, other) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    # called when trying to show a string representation of instance
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

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
        
# Takes a list of "old nodes", a delimiter, and a text type.
# It should return a new list of nodes, where any "text" type nodes in the input list are (potentially)
# split into multiple nodes based on the syntax. 
def split_nodes(old_nodes:list[TextNode], text_type:TextType) -> list[TextNode]:
    char_dict = {
        TextType.BOLD : "**",
        TextType.ITALIC : "_",
        TextType.CODE : "`"
    }

    if text_type not in char_dict:
        raise ValueError(f"cannot split node with invalid text type of {text_type}")
    
    result = []
    delimiter = char_dict[text_type]

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