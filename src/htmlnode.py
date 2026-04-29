class HTMLNode:
    def __init__(self, tag=None, value=None, children:list|None=None, props:dict|None=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    # Child classes will override this method to render themselves as HTML
    def to_html(self):
        raise NotImplementedError()
    
    # Returns a formatted string representing the HTML attributes of the node
    def props_to_html(self) -> str:
        if not self.props:
            return ""
        result = ""
        for prop_key in self.props.keys():
            result += f'{prop_key}="{self.props[prop_key]}" '
        return result[:-1]
    
    # called when trying to show a string representation of instance
    def __repr__(self) -> str:
        return f"HTMLNode(Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})"