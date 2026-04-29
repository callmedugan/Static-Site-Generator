import unittest

from src.blocks import *


class TestBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_types(self):
        # Heading cases
        self.assertEqual(block_to_block_type("# heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### triple heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### hex heading"), BlockType.HEADING)
        
        # Code cases
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        
        # Quote cases
        self.assertEqual(block_to_block_type("> quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> line 1\n> line 2"), BlockType.QUOTE)
        
        # Unordered list cases
        self.assertEqual(block_to_block_type("* item 1\n* item 2"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.UNORDERED_LIST)
        
        # Ordered list cases
        self.assertEqual(block_to_block_type("1. first\n2. second\n3. third"), BlockType.ORDERED_LIST)
        
        # Paragraph (default) case
        self.assertEqual(block_to_block_type("Just a normal paragraph."), BlockType.PARAGRAPH)

    def test_block_to_block_type_edge_cases(self):
        # Invalid Heading (missing space)
        self.assertEqual(block_to_block_type("#heading"), BlockType.PARAGRAPH)
        
        # Invalid Ordered List (wrong start number)
        self.assertEqual(block_to_block_type("2. second\n3. third"), BlockType.PARAGRAPH)
        
        # Invalid Quote (one line missing the >)
        self.assertEqual(block_to_block_type("> quote\nmissing bracket"), BlockType.PARAGRAPH)
        
        # Invalid Unordered List (missing spaces)
        self.assertEqual(block_to_block_type("*no_space"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()