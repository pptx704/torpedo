import unittest
from os import path
from ..template import (
    Snippet,
    Template,
    SnippetParsingError
)
from .utils import (
    snippet_text_1,
    snippet_text_2,
    snippet_text_3,
    snippet_html_1,
    snippet_html_2
)

class SnippetTest(unittest.TestCase):
    def test_plain_snippets(self):
        self.assertEqual(Snippet(snippet_text_1).type, 'plain')
        self.assertEqual(Snippet(snippet_text_2).type, 'plain')
        self.assertEqual(Snippet(snippet_text_3).type, 'plain')
    
    def test_html_snippets(self):
        self.assertEqual(Snippet(snippet_html_1).type, 'html')
        self.assertEqual(Snippet(snippet_html_2).type, 'html')

    def test_image_snippets(self):
        image_1 = Snippet(path.join(path.dirname(__file__), 'files', 'test_image.jpg'))
        image_2 = Snippet(path.join(path.dirname(__file__), 'files', 'test_image.png'))

        self.assertEqual(image_1.type, 'image')
        self.assertEqual(image_2.type, 'image')
    
    def test_audio_snippets(self):
        audio_1 = Snippet(path.join(path.dirname(__file__), 'files', 'test_audio.wav'))
        audio_2 = Snippet(path.join(path.dirname(__file__), 'files', 'test_audio.mp3'))

        self.assertEqual(audio_1.type, 'audio')
        self.assertEqual(audio_2.type, 'audio')

    def test_binary_snippets(self):
        binary_1 = Snippet(path.join(path.dirname(__file__), 'files', 'test_csv_1000.csv'))
        binary_2 = Snippet(path.join(path.dirname(__file__), 'files', 'test_excel_1000.xlsx'))
        binary_3 = Snippet(path.join(path.dirname(__file__), 'files', 'test_tsv_1000.txt'))

        self.assertEqual(binary_1.type, 'bin')
        self.assertEqual(binary_2.type, 'bin')
        self.assertEqual(binary_3.type, 'bin')

        with self.assertRaises(SnippetParsingError) as context:
            Snippet(path.join(path.dirname(__file__), 'files', 'test_executable.exe'))
        
        self.assertTrue("Filetype not allowed" in str(context.exception))

class TemplateTest(unittest.TestCase):

    def test_load_media(self):
        template = Template("Demo Template (no media)")
        template.add_snippet(
            Snippet(snippet_text_1),
            Snippet(snippet_html_2),
            Snippet(path.join(path.dirname(__file__), 'files', 'test_audio.wav')),
            Snippet(path.join(path.dirname(__file__), 'files', 'test_excel_1000.xlsx')),
            Snippet(path.join(path.dirname(__file__), 'files', 'test_tsv_1000.txt')),
            Snippet(path.join(path.dirname(__file__), 'files', 'test_image.png'))
        )

        self.assertEqual(len(template.snippets), 6)

    def test_multi_text(self):
        template = Template("Demo Template (multi text)")

        with self.assertRaises(SnippetParsingError) as context:
            template.add_snippet(
                Snippet(snippet_text_1),
                Snippet(snippet_text_2),
                Snippet(snippet_text_3),
                Snippet(snippet_html_2)
            )
        
        self.assertTrue("Another plain MIMEType already present" in str(context.exception))

    def test_multi_html(self):
        template = Template("Demo Template (multi html)")

        with self.assertRaises(SnippetParsingError) as context:
            template.add_snippet(
                Snippet(snippet_text_1),
                Snippet(snippet_html_1),
                Snippet(snippet_html_2)
            )
        
        self.assertTrue("Another html MIMEType already present" in str(context.exception))