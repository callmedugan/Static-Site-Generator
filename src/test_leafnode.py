import unittest

from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_raw_text(self):
        node = LeafNode(None, "Just some plain text")
        self.assertEqual(node.to_html(), "Just some plain text")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://google.com" target="_blank">Click me!</a>')

    def test_leaf_to_html_header(self):
        node = LeafNode("h1", "Title Text")
        self.assertEqual(node.to_html(), "<h1>Title Text</h1>")

    def test_leaf_to_html_bold(self):
        node = LeafNode("b", "Bolded text")
        self.assertEqual(node.to_html(), "<b>Bolded text</b>")

    def test_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()