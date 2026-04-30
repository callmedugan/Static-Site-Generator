import unittest

from src.webpage import *


class TestWebpage(unittest.TestCase):

    def test_extract_title(self):
        # Standard case
        self.assertEqual(extract_title("# Hello"), "Hello")
        
        # Case with leading/trailing whitespace
        self.assertEqual(extract_title("#  Title with spaces  "), "Title with spaces")
        
        # Multiline case where H1 isn't the first line
        markdown = """
        Some intro text
        # The Real Title
        More content
        """
        self.assertEqual(extract_title(markdown.strip()), "The Real Title")

def test_extract_title_exception(self):
    # Missing H1
    with self.assertRaises(Exception) as cm:
        extract_title("## This is an H2, not an H1")
    self.assertEqual(str(cm.exception), "markdown does not contain h1 title")

    # Only plain text
    with self.assertRaises(Exception):
        extract_title("Just some text")


if __name__ == "__main__":
    unittest.main()