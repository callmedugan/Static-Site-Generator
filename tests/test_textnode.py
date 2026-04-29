import unittest

from src.textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq_1(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_2(self):
        node = TextNode("This is a different text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_3(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_4(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_text(self):
        node = TextNode("Just plain text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Just plain text")

    def test_text_node_to_html_node_bold(self):
        node = TextNode("Bolded stuff", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bolded stuff")

    def test_text_node_to_html_node_italic(self):
        node = TextNode("Italicized", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italicized")

    def test_text_node_to_html_node_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")

    def test_text_node_to_html_node_link(self):
        node = TextNode("Click here", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_text_node_to_html_node_image(self):
        node = TextNode("Alt text description", TextType.IMG, "https://path/to/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, 
            {"src": "https://path/to/image.png", "alt": "Alt text description"}
        )

    def test_split_nodes(self):
        input_node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes([input_node], TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_multiple(self):
        node = TextNode("This has **bold** and **more bold**", TextType.TEXT)
        new_nodes = split_nodes([node], TextType.BOLD)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_at_start(self):
        node = TextNode("**Bold** at the start", TextType.TEXT)
        new_nodes = split_nodes([node], TextType.BOLD)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_italic(self):
        node = TextNode("Normal, _italic_, normal", TextType.TEXT)
        new_nodes = split_nodes([node], TextType.ITALIC)
        expected = [
            TextNode("Normal, ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", normal", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_unclosed_delimiter(self):
        # This should raise an exception if the closing delimiter is missing
        node = TextNode("This has an `unclosed code block", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes([node], TextType.CODE)

    def test_split_nodes_empty_text(self):
        # Testing how it handles nodes with no text - it should remove them
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes([node], TextType.CODE)
        self.assertEqual(new_nodes, [])


if __name__ == "__main__":
    unittest.main()