""" Tests the module app.blog.models. """


from unittest import TestCase
from os.path import dirname
from os.path import abspath, join
from app.blog.models import Post


class TestBlogModels(TestCase):

    def setUp(self):
        test_dir = abspath(dirname(__file__))

        markdown_file = join(test_dir, 'assets', 'markdown.md')
        notebook_file = join(test_dir, 'assets', 'notebook.json')

        with open(markdown_file) as f:
            markdown_content = f.read()
        with open(notebook_file) as f:
            notebook_content = f.read()

        self.markdown_post = Post('markdown.md', 'Mickey', '2015-09-19T09:37:17Z', 'Yo!', markdown_content)
        self.notebook_post = Post('notebook.ipynb', 'Mickey', '2015-09-19T09:37:17Z', 'Yo!', notebook_content)

    def tearDown(self):
        pass

    def test_lines(self):
        lines = ['# The first line is the title',
                 '',
                 'The first paragraph is the excerpt.',
                 '',
                 '## A random header',
                 '',
                 'This is a random paragraph.',
                 '',
                 'This is another random paragraph.']

        self.assertEquals(lines, self.markdown_post.top_lines)
        self.assertEquals(lines, self.notebook_post.top_lines)

    def test_title(self):
        self.assertEquals('The first line is the title', self.markdown_post.title)
        self.assertEquals('The first line is the title', self.notebook_post.title)

    def test_excerpt(self):
        self.assertEquals('The first paragraph is the excerpt.', self.markdown_post.excerpt)
        self.assertEquals('The first paragraph is the excerpt.', self.notebook_post.excerpt)

    def test_author(self):
        self.assertEquals('Mickey', self.markdown_post.author)
        self.assertEquals('Mickey', self.notebook_post.author)

    def test_message(self):
        self.assertEquals('Yo!', self.markdown_post.last_commit_message)
        self.assertEquals('Yo!', self.notebook_post.last_commit_message)

    def test_timestamp(self):
        self.assertEquals('Saturday 19 September 2015', self.markdown_post.timestamp)
        self.assertEquals('Saturday 19 September 2015', self.notebook_post.timestamp)

    def test_slug(self):
        self.assertEquals('the-first-line-is-the-title', self.markdown_post.slug)
        self.assertEquals('the-first-line-is-the-title', self.notebook_post.slug)
