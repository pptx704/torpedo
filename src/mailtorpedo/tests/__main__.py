import unittest

from .reader import (
    CSVReaderTest,
    ExcelReaderTest
)
from .template import (
    SnippetTest,
    TemplateTest
)

from .binder import (
    BinderInitTest,
    BinderParseTest
)

if __name__ == "__main__":
    unittest.main()
