import unittest

from ..filetype import FileType
from ..filetype import guess_filetype_from_path


class TestFileType(unittest.TestCase):

    def test_get_filetype(self):
        self.assertEqual(FileType.ini,
                         guess_filetype_from_path("/path/to/hoge.ini"))
        self.assertEqual(FileType.ini,
                         guess_filetype_from_path("/path/to/hoge.conf"))
        self.assertEqual(FileType.yaml,
                         guess_filetype_from_path("/path/to/hoge.yml"))
        self.assertEqual(FileType.yaml,
                         guess_filetype_from_path("/path/to/hoge.yaml"))
        # TODO catch exception after #169 is merges
        # self.assertEqual(FileType.NONE, guess_filetype_from_path("/path/to/hoge.jpg"))
