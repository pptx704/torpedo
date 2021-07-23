import unittest
from os import path
from ..reader import (
    CSVReader,
    ExcelReader
)

class CSVReaderTest(unittest.TestCase):
    def setUp(self):
        self.csv_reader = CSVReader(path.join(path.dirname(path.abspath(__file__)), 'files/test_csv_1000.csv'), "Email")
        self.tsv_reader = CSVReader(path.join(path.dirname(path.abspath(__file__)), 'files/test_tsv_1000.txt'), "Email")
        self.csv_dict = self.csv_reader.parsed_dict()
        self.tsv_dict = self.tsv_reader.parsed_dict()
        
    def test_header_csv_reader(self):
        self.assertEqual(self.csv_reader.delimiter, ',')
        self.assertEqual(self.csv_reader.headers, ['Name', 'Age', 'Email', 'Username', 'Rank'])

    def test_header_tsv_reader(self):
        self.assertEqual(self.tsv_reader.delimiter, '\t')
        self.assertEqual(self.tsv_reader.headers, ['Name', 'Age', 'Email', 'Username', 'Rank'])

    def test_parse_csv_dict(self):
        self.assertDictEqual(self.csv_dict[0], {'Name':'da211f', 'Age':'26', 'Email':'da211f@example.com', 'Username':'43d49f95', 'Rank':'1'})
        self.assertDictEqual(self.csv_dict[108], {'Name':'8564a9', 'Age':'32', 'Email':'8564a9@example.com', 'Username':'52186932', 'Rank':'4'})
        self.assertDictEqual(self.csv_dict[255], {'Name':'2bada9', 'Age':'34', 'Email':'2bada9@example.com', 'Username':'0059152e', 'Rank':'9'})
        self.assertDictEqual(self.csv_dict[292], {'Name':'98eacf', 'Age':'25', 'Email':'98eacf@example.com', 'Username':'854070bd', 'Rank':'10'})

    def test_parse_tsv_dict(self):
        self.assertDictEqual(self.tsv_dict[14], {'Name':'6c636f', 'Age':'23', 'Email':'6c636f@example.com', 'Username':'36da3434', 'Rank':'24'})
        self.assertDictEqual(self.tsv_dict[78], {'Name':'2d004b', 'Age':'25', 'Email':'2d004b@example.com', 'Username':'c855e96b', 'Rank':'42'})
        self.assertDictEqual(self.tsv_dict[636], {'Name':'26763e', 'Age':'20', 'Email':'26763e@example.com', 'Username':'46fa3283', 'Rank':'44'})
        self.assertDictEqual(self.tsv_dict[897], {'Name':'70f60b', 'Age':'22', 'Email':'70f60b@example.com', 'Username':'fbc12372', 'Rank':'22'})

    def test_csv_header_error(self):
        reader = CSVReader(path.join(path.dirname(path.abspath(__file__)), 'files/test_csv_1000.csv'), "Random")
        with self.assertRaises(ValueError) as context:
            reader.parsed_dict()
        
        self.assertTrue("No column with header" in str(context.exception))

    def test_tsv_header_error(self):
        reader = CSVReader(path.join(path.dirname(path.abspath(__file__)), 'files/test_tsv_1000.txt'), "Random")
        with self.assertRaises(ValueError) as context:
            reader.parsed_dict()
        
        self.assertTrue("No column with header" in str(context.exception))

class ExcelReaderTest(unittest.TestCase):
    def setUp(self):
        self.excel_reader_sheet1 = ExcelReader(path.join(path.dirname(path.abspath(__file__)), 'files/test_excel_1000.xlsx'), 'Email', sheet=0)
        self.excel_reader_sheet2 = ExcelReader(path.join(path.dirname(path.abspath(__file__)), 'files/test_excel_1000.xlsx'), 'Email', sheet=1)
        self.sheet1_dict = self.excel_reader_sheet1.parsed_dict()
        self.sheet2_dict = self.excel_reader_sheet2.parsed_dict()

    def test_loaded_sheet(self):
        self.assertEqual(self.excel_reader_sheet1.sheet.title, "test_csv_1000")
        self.assertEqual(self.excel_reader_sheet2.sheet.title, "test_tsv_1000")

    def test_load_sheet_by_name(self):
        excel_reader_sheet1 = ExcelReader(path.join(path.dirname(path.abspath(__file__)), 'files/test_excel_1000.xlsx'), 'Email', sheet="test_csv_1000")
        excel_reader_sheet2 = ExcelReader(path.join(path.dirname(path.abspath(__file__)), 'files/test_excel_1000.xlsx'), 'Email', sheet="test_tsv_1000")

        self.assertEqual(excel_reader_sheet1.sheet.title, "test_csv_1000")
        self.assertEqual(excel_reader_sheet2.sheet.title, "test_tsv_1000")
    
    def test_check_headers(self):
        self.assertEqual(self.excel_reader_sheet1.headers, ['Name', 'Age', 'Email', 'Username', 'Rank'])
        self.assertEqual(self.excel_reader_sheet2.headers, ['Name', 'Age', 'Email', 'Username', 'Rank'])

    def test_parse_sheet1(self):
        self.assertDictEqual(self.sheet1_dict[0], {'Name':'da211f', 'Age':'26', 'Email':'da211f@example.com', 'Username':'43d49f95', 'Rank':'1'})
        self.assertDictEqual(self.sheet1_dict[108], {'Name':'8564a9', 'Age':'32', 'Email':'8564a9@example.com', 'Username':'52186932', 'Rank':'4'})
        self.assertDictEqual(self.sheet1_dict[255], {'Name':'2bada9', 'Age':'34', 'Email':'2bada9@example.com', 'Username':'0059152e', 'Rank':'9'})
        self.assertDictEqual(self.sheet1_dict[292], {'Name':'98eacf', 'Age':'25', 'Email':'98eacf@example.com', 'Username':'854070bd', 'Rank':'10'})
        self.assertDictEqual(self.sheet1_dict[685], {'Name':'73014f', 'Age':'21', 'Email':'73014f@example.com', 'Username':'dc1202b0', 'Rank':'9'})

    def test_parse_sheet2(self):
        self.assertDictEqual(self.sheet2_dict[14], {'Name':'6c636f', 'Age':'23', 'Email':'6c636f@example.com', 'Username':'36da3434', 'Rank':'24'})
        self.assertDictEqual(self.sheet2_dict[78], {'Name':'2d004b', 'Age':'25', 'Email':'2d004b@example.com', 'Username':'c855e96b', 'Rank':'42'})
        self.assertDictEqual(self.sheet2_dict[636], {'Name':'26763e', 'Age':'20', 'Email':'26763e@example.com', 'Username':'46fa3283', 'Rank':'44'})
        self.assertDictEqual(self.sheet2_dict[897], {'Name':'70f60b', 'Age':'22', 'Email':'70f60b@example.com', 'Username':'fbc12372', 'Rank':'22'})
        self.assertDictEqual(self.sheet2_dict[945], {'Name':'df2aff', 'Age':'19', 'Email':'df2aff@example.com', 'Username':'a4b5f7e4', 'Rank':'28'})

    def test_excel_sheet1_header_error(self):
        reader = ExcelReader(path.join(path.dirname(path.abspath(__file__)), 'files/test_excel_1000.xlsx'), 'Random', sheet=0)
        with self.assertRaises(ValueError) as context:
            reader.parsed_dict()
        
        self.assertTrue("No column with header" in str(context.exception))

    def test_excel_sheet2_header_error(self):
        reader = ExcelReader(path.join(path.dirname(path.abspath(__file__)), 'files/test_excel_1000.xlsx'), 'Random', sheet=1)
        with self.assertRaises(ValueError) as context:
            reader.parsed_dict()
        
        self.assertTrue("No column with header" in str(context.exception))