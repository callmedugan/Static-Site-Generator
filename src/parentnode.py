from src.htmlnode import HTMLNode

class ParentNode(HTMLNode):
    # tag and children not optional, no value, and props optional
    def __init__(self, tag, children: list[HTMLNode], props: dict | None = None):
        self.children: list[HTMLNode] = children
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        #build tags
        #add props into opening tag
        children_html = f"<{self.tag} {self.props_to_html()}>" if self.props else f"<{self.tag}>"
        #iterate through children and sandwich in their tags, calling their to_html recursively
        for c in self.children:
            children_html += c.to_html()
        #closing tag
        children_html += f"</{self.tag}>"
        return children_html