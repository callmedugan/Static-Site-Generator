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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_various(self):
        # Multiple images
        text_multiple = "![one](url1.png) and ![two](url2.png)"
        self.assertListEqual(
            [("one", "url1.png"), ("two", "url2.png")], 
            extract_markdown_images(text_multiple)
        )

        # No images
        text_none = "This is just text with no images."
        self.assertListEqual([], extract_markdown_images(text_none))

        # Ignore regular links (should not pick up [link])
        text_with_links = "This is a [link](url1.com) and an ![image](url2.png)"
        self.assertListEqual(
            [("image", "url2.png")], 
            extract_markdown_images(text_with_links)
        )

        # Empty alt text
        text_empty_alt = "![](https://imgur.com)"
        self.assertListEqual(
            [("", "https://imgur.com")], 
            extract_markdown_images(text_empty_alt)
        )

        # Complex alt text with spaces and punctuation
        text_complex = "![Image of a Dog! (with a ball)](dog.png)"
        self.assertListEqual(
            [("Image of a Dog! (with a ball)", "dog.png")], 
            extract_markdown_images(text_complex)
        )

    def test_extract_markdown_links_various(self):
        # Multiple links
        text_multiple = "Check [Google](https://google.com) and [Boot.dev](https://boot.dev)"
        self.assertListEqual(
            [("Google", "https://google.com"), ("Boot.dev", "https://boot.dev")],
            extract_markdown_links(text_multiple)
        )

        # No links
        text_none = "This is just text with no links."
        self.assertListEqual([], extract_markdown_links(text_none))

        # Ignore images (should not pick up ![image])
        text_with_images = "This is an ![image](url1.png) and a [link](url2.com)"
        self.assertListEqual(
            [("link", "url2.com")], 
            extract_markdown_links(text_with_images)
        )

        # Empty link text
        text_empty_anchor = "[](https://empty.com)"
        self.assertListEqual(
            [("", "https://empty.com")],
            extract_markdown_links(text_empty_anchor)
        )

        # Links with special characters in the text
        text_complex = "[Click here for 25% off! (deal ends soon)](https://sale.com)"
        self.assertListEqual(
            [("Click here for 25% off! (deal ends soon)", "https://sale.com")],
            extract_markdown_links(text_complex)
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMG, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_variations(self):
        # Image at the very start
        node_start = TextNode("![img](url) end text", TextType.TEXT)
        self.assertListEqual(
            [TextNode("img", TextType.IMG, "url"), TextNode(" end text", TextType.TEXT)],
            split_nodes_image([node_start])
        )

        # Image at the very end
        node_end = TextNode("start text ![img](url)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("start text ", TextType.TEXT), TextNode("img", TextType.IMG, "url")],
            split_nodes_image([node_end])
        )

        # Only an image
        node_only = TextNode("![img](url)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("img", TextType.IMG, "url")],
            split_nodes_image([node_only])
        )

    def test_split_link_variations(self):
        # Multiple links
        node = TextNode(
            "Click [here](url1) or [there](url2)",
            TextType.TEXT,
        )
        print(split_nodes_link([node]))
        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "url1"),
                TextNode(" or ", TextType.TEXT),
                TextNode("there", TextType.LINK, "url2"),
            ],
            split_nodes_link([node])
        )

        # Link at start and end
        node_edges = TextNode("[start](u1) middle [end](u2)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("start", TextType.LINK, "u1"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("end", TextType.LINK, "u2"),
            ],
            split_nodes_link([node_edges])
        )

    def test_split_images_ignore_links(self):
        # split_nodes_image should ignore regular links
        node = TextNode("This is a [link](url) and an ![image](url)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("This is a [link](url) and an ", TextType.TEXT),
                TextNode("image", TextType.IMG, "url"),
            ],
            split_nodes_image([node])
        )

    def test_split_links_ignore_images(self):
        # split_nodes_link should ignore images
        node = TextNode("This is an ![image](url) and a [link](url)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("This is an ![image](url) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
            ],
            split_nodes_link([node])
        )

    def test_text_to_textnodes_basic(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text)
        )

    def test_text_to_textnodes_complex(self):
        text = "This is **bold**_italic_`code`![img](url)[link](url)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
            TextNode("img", TextType.IMG, "url"),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_no_special(self):
        # Tests that plain text remains a single text node
        text = "Just plain text with no markdown."
        nodes = text_to_textnodes(text)
        expected = [TextNode("Just plain text with no markdown.", TextType.TEXT)]
        self.assertListEqual(expected, nodes)



if __name__ == "__main__":
    unittest.main()