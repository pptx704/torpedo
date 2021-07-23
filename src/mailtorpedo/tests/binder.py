import unittest
from os import path
from random import randint

from ..binder import Binder

from ..reader import (
    CSVReader, 
    ExcelReader
)

from ..template import (
    Template, 
    Snippet
)

from .utils import (
    snippet_text_1,
    snippet_text_2,
    snippet_html_1,
    snippet_html_2
)

from .data_checks import *

class BinderInitTest(unittest.TestCase):    
    def test_text_not_variable(self):
        reader = CSVReader(path.join(path.dirname(__file__), 'files', 'test_csv_1000.csv'), 'Email')
        snippet = Snippet(snippet_text_1)
        template = Template("Test")
        template.add_snippet(snippet)
        binder = Binder(reader, template)

        self.assertEqual(binder.type, 'bulk')
    
    def test_text_not_variable(self):
        reader = CSVReader(path.join(path.dirname(__file__), 'files', 'test_tsv_1000.txt'), 'Email')
        snippet = Snippet(snippet_text_2)
        template = Template("Test")
        template.add_snippet(snippet)
        binder = Binder(reader, template)

        self.assertEqual(binder.type, 'solo')

    def test_html_not_variable(self):
        reader = ExcelReader(path.join(path.dirname(path.abspath(__file__)), 'files/test_excel_1000.xlsx'), 'Email', sheet="test_csv_1000")
        snippet = Snippet(snippet_html_1)
        template = Template("Test")
        template.add_snippet(snippet)
        binder = Binder(reader, template)

        self.assertEqual(binder.type, 'bulk')

    def test_html_not_variable(self):
        reader = ExcelReader(path.join(path.dirname(path.abspath(__file__)), 'files/test_excel_1000.xlsx'), 'Email', sheet="test_tsv_1000")
        snippet = Snippet(snippet_html_2)
        template = Template("Test")
        template.add_snippet(snippet)
        binder = Binder(reader, template)

        self.assertEqual(binder.type, 'solo')

class BinderParseTest(unittest.TestCase):
    def setUp(self):
        self.csv_reader = CSVReader(path.join(path.dirname(__file__), 'files', 'test_csv_1000.csv'), 'Email')
        self.tsv_reader = CSVReader(path.join(path.dirname(__file__), 'files', 'test_tsv_1000.txt'), 'Email')
        self.excel_reader_sheet1 = ExcelReader(path.join(path.dirname(path.abspath(__file__)), 'files/test_excel_1000.xlsx'), 'Email', sheet="test_csv_1000")
        self.excel_reader_sheet2 = ExcelReader(path.join(path.dirname(path.abspath(__file__)), 'files/test_excel_1000.xlsx'), 'Email', sheet="test_tsv_1000")

        self.template = Template("Demo test")

    def test_csv_reader_parse_count(self):
        binder = Binder(self.csv_reader, self.template)
        value = binder.parse()

        self.assertEqual(len(list(value)), 1000)

    def test_tsv_reader_parse_count(self):
        binder = Binder(self.tsv_reader, self.template)
        value = binder.parse()

        self.assertEqual(len(list(value)), 1000)

    def test_excel_reader_sheet1_parse_count(self):
        binder = Binder(self.excel_reader_sheet1, self.template)
        value = binder.parse()

        self.assertEqual(len(list(value)), 999)
    
    def test_excel_reader_sheet2_parse_count(self):
        binder = Binder(self.excel_reader_sheet2, self.template)
        value = binder.parse()

        self.assertEqual(len(list(value)), 999)

    def test_text_parsing_no_var(self):
        template = self.template
        snippet = Snippet(snippet_text_1)
        template.add_snippet(snippet)
        
        # csv reader
        binder = Binder(self.csv_reader, template)
        data = list(binder.parse())

        self.assertEqual(data[randint(0, 999)][1]._payload[0]._payload, data[randint(0, 999)][1]._payload[0]._payload)

        # tsv reader
        binder = Binder(self.csv_reader, template)
        data = list(binder.parse())

        self.assertEqual(data[randint(0, 999)][1]._payload[0]._payload, data[randint(0, 999)][1]._payload[0]._payload)

        # excel sheet1 reader
        binder = Binder(self.excel_reader_sheet1, template)
        data = list(binder.parse())

        self.assertEqual(data[randint(0, 998)][1]._payload[0]._payload, data[randint(0, 998)][1]._payload[0]._payload)

        # excel sheet3 reader
        binder = Binder(self.excel_reader_sheet2, template)
        data = list(binder.parse())

        self.assertEqual(data[randint(0, 998)][1]._payload[0]._payload, data[randint(0, 998)][1]._payload[0]._payload)

    def test_html_parsing_no_var(self):
        template = self.template
        snippet = Snippet(snippet_html_1)
        template.add_snippet(snippet)
        
        # csv reader
        binder = Binder(self.csv_reader, template)
        data = list(binder.parse())

        self.assertEqual(data[randint(0, 999)][1]._payload[0]._payload, data[randint(0, 999)][1]._payload[0]._payload)

        # tsv reader
        binder = Binder(self.csv_reader, template)
        data = list(binder.parse())

        self.assertEqual(data[randint(0, 999)][1]._payload[0]._payload, data[randint(0, 999)][1]._payload[0]._payload)

        # excel sheet1 reader
        binder = Binder(self.excel_reader_sheet1, template)
        data = list(binder.parse())

        self.assertEqual(data[randint(0, 998)][1]._payload[0]._payload, data[randint(0, 998)][1]._payload[0]._payload)

        # excel sheet3 reader
        binder = Binder(self.excel_reader_sheet2, template)
        data = list(binder.parse())

        self.assertEqual(data[randint(0, 998)][1]._payload[0]._payload, data[randint(0, 998)][1]._payload[0]._payload)

    def test_skipping_media(self):
        template = Template("Demo Template (no media)")
        template.add_snippet(
            Snippet(snippet_text_1),
            Snippet(snippet_html_2),
            Snippet(path.join(path.dirname(__file__), 'files', 'test_audio.wav')),
            Snippet(path.join(path.dirname(__file__), 'files', 'test_excel_1000.xlsx')),
            Snippet(path.join(path.dirname(__file__), 'files', 'test_tsv_1000.txt')),
            Snippet(path.join(path.dirname(__file__), 'files', 'test_image.png'))
        )

        csv_binder = Binder(self.csv_reader, template)
        data = list(csv_binder.parse())

        self.assertEqual(len(data[randint(0,999)][1]._payload), 2)

        tsv_binder = Binder(self.tsv_reader, template)
        data = list(tsv_binder.parse())

        self.assertEqual(len(data[randint(0,999)][1]._payload), 2)

        excel_reader_sheet1_binder = Binder(self.excel_reader_sheet1, template)
        data = list(csv_binder.parse())

        self.assertEqual(len(data[randint(0,998)][1]._payload), 2)

        excel_reader_sheet1_binder = Binder(self.excel_reader_sheet1, template)
        data = list(csv_binder.parse())

        self.assertEqual(len(data[randint(0,998)][1]._payload), 2)

    def test_variable_replacements(self):
        template = Template("Demo Template (replaced variables)")
        template.add_snippet(
            Snippet(snippet_text_2),
            Snippet(snippet_html_2),
        )
        binder = Binder(self.csv_reader, template)
        data = list(binder.parse())

        self.assertEqual(data[254][1]._payload[0]._payload, text_message1)
        self.assertEqual(data[318][1]._payload[0]._payload, text_message2)
        self.assertEqual(data[528][1]._payload[0]._payload, text_message3)
        self.assertEqual(data[646][1]._payload[1]._payload, html_message1)
        self.assertEqual(data[821][1]._payload[1]._payload, html_message2)
        self.assertEqual(data[999][1]._payload[1]._payload, html_message3)