import unittest

from src.parentnode import ParentNode
from src.leafnode import LeafNode

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("span", "child")],
            {"class": "container", "id": "main"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main"><span>child</span></div>'
        )

    def test_headings_and_lists(self):
        node = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode("b", "First item")]),
                ParentNode("li", [LeafNode("i", "Second item")]),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<ul><li><b>First item</b></li><li><i>Second item</i></li></ul>"
        )

    def test_to_html_empty_children_list(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()