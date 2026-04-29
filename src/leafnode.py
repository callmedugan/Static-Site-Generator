from src.htmlnode import HTMLNode

class LeafNode(HTMLNode):
    # requires tag and value, no children, and props optional
    def __init__(self, tag, value, props: dict | None = None):
        super().__init__(tag, value, None, props)

    # renders a leaf node as an html string
    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value.")
        if not self.tag:
            return str(self.value)

        #build tags
        if self.props:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
    # called when trying to show a string representation of instance
    def __repr__(self) -> str:
        return f"HTMLNode(Tag: {self.tag}, Value: {self.value}, Props: {self.props})"