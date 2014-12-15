# coding=utf-8
"""Test for scan."""
import os

from .utils import TestNodeListAndDir
from ..pipes.scan import directory


class TestScan(TestNodeListAndDir):

    """Unittest for dataprocessor.pipes.scan.

    Attributes
    ----------
    tempdir_paths : list
        list of project root dir path
    node_list : list

    """

    def setUp(self):
        """Prepare test environment."""
        self._generate_test_directories()

    def _generate_test_directories(self):
        """Generate test directories.

        Generated directories and files are as follows,

        (dir-path, including-dirs, including-files)

        ('/tmpdir_path', ['run0', 'run1', 'run2'], [])
        ('/tmpdir_path/run0', ['run0', 'run1'], ['test.conf'])
        ('/tmpdir_path/run0/run0', ['data'], [])
        ('/tmpdir_path/run0/run0/data', [], ['hoge.conf'])
        ('/tmpdir_path/run0/run1', [], ['test.conf'])
        ('/tmpdir_path/run1', [], ['test.conf'])
        ('/tmpdir_path/run2', ['data'], [])
        ('/tmpdir_path/run2/data', [], ['test.conf'])
        ('/tmpdir_path/run2/dummy', [], [])
        ('/tmpdir_path/run3', ['data'], [])  # symboliclink to run2

        """
        import tempfile
        self.tempdir_path = tempfile.mkdtemp()
        root = self.tempdir_path
        for i in range(3):
            os.mkdir(os.path.join(root, "run" + str(i)))
        for i in range(2):
            open(os.path.join(root, "run" + str(i), "test.conf"),
                 "w").close()
        for i in range(2):
            os.mkdir(os.path.join(root, "run0", "run" + str(i)))
        os.mkdir(os.path.join(root, "run2", "data"))
        os.mkdir(os.path.join(root, "run2", "dummy"))
        os.mkdir(os.path.join(root, "run0", "run0", "data"))
        open(os.path.join(root, "run0", "run1", "test.conf"), "w").close()
        open(os.path.join(root, "run2", "data", "test.conf"), "w").close()
        open(os.path.join(root, "run0", "run0", "data", "hoge.conf"),
             "w").close()
        os.symlink(os.path.join(root, "run2"), os.path.join(root, "run3"))

    def test_directory_for_first_scan1(self):
        """Test for initial scan."""
        node_list = []
        root_dir = self.tempdir_path
        # whitelist specifies directory.
        node_list = directory(node_list, root_dir, "data")
        compare_node_list = [
            {'path': root_dir,
             'parents': [],
             'children': [os.path.join(root_dir, "run2")],
             'name': os.path.basename(root_dir),
             'type': 'project'},
            {'path': os.path.join(root_dir, "run0"),
             'parents': [],
             'children': [os.path.join(root_dir, "run0/run0")],
             'name': 'run0',
             'type': 'project'},
            {'path': os.path.join(root_dir, "run0/run0"),
             'parents': [os.path.join(root_dir, "run0")],
             'children': [],
             'name': 'run0',
             'type': 'run'},
            {'path': os.path.join(root_dir, "run2"),
             'parents': [root_dir],
             'children': [],
             'name': 'run2',
             'type': 'run'}]
        self.assertEqual(node_list, compare_node_list)

    def test_directory_for_first_scan2(self):
        """Test for initial scan."""
        node_list = []
        root_dir = self.tempdir_path
        # whitelist have two elements.
        node_list = directory(node_list, root_dir,
                              ["data/hoge*", "data/test*"])
        compare_node_list = [
            {'path': root_dir,
             'parents': [],
             'children': [os.path.join(root_dir, "run2")],
             'name': os.path.basename(root_dir),
             'type': 'project'},
            {'path': os.path.join(root_dir, "run0"),
             'parents': [],
             'children': [os.path.join(root_dir, "run0/run0")],
             'name': 'run0',
             'type': 'project'},
            {'path': os.path.join(root_dir, "run0/run0"),
             'parents': [os.path.join(root_dir, "run0")],
             'children': [],
             'name': 'run0',
             'type': 'run'},
            {'path': os.path.join(root_dir, "run2"),
             'parents': [root_dir],
             'children': [],
             'name': 'run2',
             'type': 'run'}]
        self.assertEqual(node_list, compare_node_list)

    def test_directory_for_first_scan3(self):
        """Test for initial scan."""
        node_list = []
        root_dir = self.tempdir_path
        # whitelist has `..`.
        node_list = directory(node_list, root_dir,
                              "../data")
        compare_node_list = [
            {'path': os.path.join(root_dir, "run0", "run0"),
             'parents': [],
             'children': [os.path.join(root_dir, "run0", "run0", "data")],
             'name': "run0",
             'type': 'project'},
            {'path': os.path.join(root_dir, "run0", "run0", "data"),
             'parents': [os.path.join(root_dir, "run0", "run0")],
             'children': [],
             'name': 'data',
             'type': 'run'},
            {'path': os.path.join(root_dir, "run2"),
             'parents': [],
             'children': [os.path.join(root_dir, "run2", "data"),
                          os.path.join(root_dir, "run2", "dummy")],
             'name': "run2",
             'type': 'project'},
            {'path': os.path.join(root_dir, "run2", "data"),
             'parents': [os.path.join(root_dir, "run2")],
             'children': [],
             'name': 'data',
             'type': 'run'},
            # This path is also added to node list.
            {'path': os.path.join(root_dir, "run2", "dummy"),
             'parents': [os.path.join(root_dir, "run2")],
             'children': [],
             'name': 'dummy',
             'type': 'run'}]
        self.assertEqual(node_list, compare_node_list)

    def test_directory_for_first_scan4(self):
        """Test for initial scan with symbolic link."""
        node_list = []
        root_dir = self.tempdir_path
        # followlinks is `True`.
        node_list = directory(node_list, root_dir,
                              "data/test.conf", followlinks=True)
        compare_node_list = [
            {'path': root_dir,
             'parents': [],
             'children': [os.path.join(root_dir, "run2"),
                          os.path.join(root_dir, "run3")],
             'name': os.path.basename(root_dir),
             'type': 'project'},
            {'path': os.path.join(root_dir, "run2"),
             'parents': [root_dir],
             'children': [],
             'name': 'run2',
             'type': 'run'},
            # Symbolic link is also added to node list.
            {'path': os.path.join(root_dir, "run3"),
             'parents': [root_dir],
             'children': [],
             'name': 'run3',
             'type': 'run'}]
        self.assertEqual(node_list, compare_node_list)

    def test_directory_for_rescan(self):
        """Test for rescan."""
        root_dir = self.tempdir_path
        node_list = [{'path': os.path.join(root_dir, "run0"),
                      'parents': [],   # empty
                      'children': [],  # empty
                      'name': 'run0',
                      'type': 'run'}]
        node_list = directory(node_list, root_dir, "*.conf")
        compare_node_list = [
            {'path': os.path.join(root_dir, 'run0'),
             'parents': [root_dir],             # fill
             'children': [os.path.join(root_dir, 'run0/run1')],  # fill
             'name': 'run0',
             'type': 'run'},
            {'path': root_dir,
             'parents': [],
             'children': [os.path.join(root_dir, 'run0'),
                          os.path.join(root_dir, 'run1')],
             'name': os.path.basename(root_dir),
             'type': 'project'},
            {'path': os.path.join(root_dir, 'run0/run0'),
             'parents': [],
             'children': [os.path.join(root_dir, 'run0/run0/data')],
             'name': 'run0',
             'type': 'project'},
            {'path': os.path.join(root_dir, 'run0/run0/data'),
             'parents': [os.path.join(root_dir, 'run0/run0')],
             'children': [],
             'name': 'data',
             'type': 'run'},
            {'path': os.path.join(root_dir, 'run0/run1'),
             'parents': [os.path.join(root_dir, 'run0')],
             'children': [],
             'name': 'run1',
             'type': 'run'},
            {'path': os.path.join(root_dir, 'run1'),
             'parents': [root_dir],
             'children': [],
             'name': 'run1',
             'type': 'run'},
            {'path': os.path.join(root_dir, 'run2'),
             'parents': [],
             'children': [os.path.join(root_dir, 'run2/data')],
             'name': 'run2',
             'type': 'project'},
            {'path': os.path.join(root_dir, 'run2/data'),
             'parents': [os.path.join(root_dir, 'run2')],
             'children': [],
             'name': 'data',
             'type': 'run'}]
        self.assertEqual(node_list, compare_node_list)

    def test_rescan_failed(self):
        root_dir = self.tempdir_path
        node_list = [{'path': os.path.join(root_dir, "run0"),
                      'children': [],  # empty and no parents key.
                      'name': 'run0',
                      'type': 'run'}]
        with self.assertRaises(KeyError):
            node_list = directory(node_list, root_dir, ["*.conf"])
