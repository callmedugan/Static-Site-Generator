import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_1(self):
        node = HTMLNode(
            "p", 
            "This is a p tag", 
            [HTMLNode("h1", "This is a heading")], 
            {"href": "https://www.google.com","target": "_blank",}
            )
        
        props_text = node.props_to_html()
        test_text = 'href="https://www.google.com" target="_blank"'

        self.assertEqual(props_text, test_text)

    def test_props_to_html_2(self):
        node = HTMLNode(
            "p", 
            "This is a p tag", 
            [HTMLNode("h1", "This is a heading")], 
            {"id": "main-header", "class": "btn btn-primary",}
            )
        
        props_text = node.props_to_html()
        test_text = 'id="main-header" class="btn btn-primary"'
        
        self.assertEqual(props_text, test_text)
        
    def test_props_to_html_3(self):
        node = HTMLNode(
            "p", 
            "This is a p tag", 
            [HTMLNode("h1", "This is a heading")], 
            {"style": "color: red; padding: 10px;", "onclick": "handleClick()", "data-user-id": "12345",}
            )
        
        props_text = node.props_to_html()
        test_text = 'style="color: red; padding: 10px;" onclick="handleClick()" data-user-id="12345"'
        
        self.assertEqual(props_text, test_text)

    def test_html_repr(self):
        node = HTMLNode(
            "p", 
            "This is a p tag", 
            [HTMLNode("h1", "This is a heading")], 
            {"style": "color: red",}
            )
        
        test_text = "HTMLNode(Tag: p, Value: This is a p tag, Children: [HTMLNode(Tag: h1, Value: This is a heading, Children: None, Props: None)], Props: {'style': 'color: red'})"
        
        self.assertEqual(str(node), test_text)


if __name__ == "__main__":
    unittest.main()