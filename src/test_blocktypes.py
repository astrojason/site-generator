import unittest
from block_types import block_to_block_type, BlockType, markdown_to_html_node

class TestBlockTypes(unittest.TestCase):
    def test_is_heading_1(self):
        block_type = block_to_block_type('# This is a header')
        self.assertEqual(block_type, BlockType.HEADING)

    def test_is_heading_2(self):
        block_type = block_to_block_type('## This is a header')
        self.assertEqual(block_type, BlockType.HEADING)

    def test_is_heading_3(self):
        block_type = block_to_block_type('### This is a header')
        self.assertEqual(block_type, BlockType.HEADING)

    def test_is_heading_4(self):
        block_type = block_to_block_type('#### This is a header')
        self.assertEqual(block_type, BlockType.HEADING)

    def test_is_heading_5(self):
        block_type = block_to_block_type('##### This is a header')
        self.assertEqual(block_type, BlockType.HEADING)

    def test_is_heading_6(self):
        block_type = block_to_block_type('###### This is a header')
        self.assertEqual(block_type, BlockType.HEADING)

    def test_is_paragraph_invalid_heading(self):
        block_type = block_to_block_type('####### Too many!')
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_is_code(self):
        markdown = '```This is a code block```'
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.CODE)

    def test_is_paragraph_code_started(self):
        markdown = '```This is not a code block'
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_is_quote_single_line(self):
        markdown = '> This is a single line quote'
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_is_quote_multi_line(self):
        markdown = '> This is a multi line quote\n> This is the second line'
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_is_paragraph_broken_quote(self):
        markdown = '> This is a multi line quote\nThis is the second line not a quote\n > This is the third line, quoted'
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_is_unordered_list_single_line(self):
        markdown = '- This is a single line unordered list'
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.ULIST)

    def test_is_unordered_list_multi_line(self):
        markdown = '- This is a multi line unordered list\n- This is the second line'
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.ULIST)

    def test_is_paragraph_broken_unordered_list(self):
        markdown = '- This is a multi line unordered_list\nThis is the second line not a unordered_list\n - This is the third line, unordered_list'
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_is_ordered_list_single_line(self):
        markdown = '1. This is a single line ordered list'
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.OLIST)

    def test_is_ordered_list_multi_line(self):
        markdown = '1. This is a multi line ordered list\n2. This is the second line'
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.OLIST)

    def test_is_paragraph_broken_ordered_list(self):
        markdown = '1. This is a multi line ordered_list\nThis is the second line not a ordered_list\n 2. This is the third line, ordered_list'
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )