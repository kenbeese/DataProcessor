# coding=utf-8

import os
import sys
import copy

from ..utility import TestNodeListAndDir
sys.path = [sys.path[0]] \
    + [os.path.join(os.path.dirname(__file__), "../../../lib")] \
    + sys.path[1:]
from dataprocessor.pipes.move_node import move_node
from dataprocessor.nodes import get
from dataprocessor.exception import DataProcessorError
sys.path = [sys.path[0]] + sys.path[2:]


class TestMoveNode(TestNodeListAndDir):

    """."""

    def test_move_dir2dir(self):
        """
        move dir to dir

        like as:
        mv tmpdir/p1/run02 tmpdir/p2/

        """

        from_path = os.path.join(self.tempdir_path, "p1/run02")
        dest = os.path.join(self.tempdir_path, "p2")
        changed_path = os.path.join(self.tempdir_path, "p2", "run02")
        # ensure that the path does not exist.
        self.assertIsNone(get(self.node_list, changed_path))
        self.node_list = move_node(self.node_list, from_path, dest)
        self.assertIsNotNone(get(self.node_list, changed_path))

    def test_move_and_rename(self):
        """
        move dir and rename it.

        like as:
        mv tmpdir/p1/run02 tmpdir/run03.

        """

        from_path = os.path.join(self.tempdir_path, "p1/run02")
        dest = os.path.join(self.tempdir_path, "run03")
        changed_path = os.path.join(self.tempdir_path, "run03")
        # ensure that the path does not exist.
        self.assertIsNone(get(self.node_list, changed_path))
        self.node_list = move_node(self.node_list, from_path, dest)
        self.assertIsNotNone(get(self.node_list, changed_path))

    def test_fail1(self):
        """
        fail to move dir because the destination path is already existing file.

        like as:
        mv tmpdir/p1/run02 tmpdir/file1

        """

        from_path = os.path.join(self.tempdir_path, "p1/run02")
        dest = os.path.join(self.tempdir_path, "file1")
        with open(dest, "w"):   # create file
            pass
        with self.assertRaises(DataProcessorError) as cm:
            self.node_list = move_node(self.node_list, from_path, dest)

    def test_fail2(self):
        """
        fail to node dir because the authority of the destination is invalid.

        like as:
        mv tmpdir/p1/run02 tmpdir/invaliddir

        """

        from_path = os.path.join(self.tempdir_path, "p1/run02")
        dest = os.path.join(self.tempdir_path, "invaliddir")
        o_nl = copy.deepcopy(self.node_list)
        os.mkdir(dest, 0000)
        with self.assertRaises(OSError) as cm:
            self.node_list = move_node(self.node_list, from_path, dest)
        os.chmod(dest, 0600)
        self.assertEqual(o_nl, self.node_list)

    def test_move_tree(self):
        """
        move dir tree.

        like as:
        mv tmpdir/p1 tmpdir/p2/

        """

        from_path = os.path.join(self.tempdir_path, "p1")
        dest = os.path.join(self.tempdir_path, "p2")

        self.node_list = move_node(self.node_list, from_path, dest)
        for p in ["p1", "p1/run00", "p1/run01", "p1/run02"]:
            self.assertIsNone(
                get(self.node_list, os.path.join(self.tempdir_path, p)))
            self.assertIsNotNone(get(self.node_list, os.path.join(dest, p)))

    def test_rename_tree(self):
        """
        rename dir tree.

        like as:
        mv tmpdir/p1 tmpdir/p3

        """

        from_path = os.path.join(self.tempdir_path, "p1")
        dest = os.path.join(self.tempdir_path, "p3")

        self.node_list = move_node(self.node_list, from_path, dest)
        for p in ["", "run00", "run01", "run02"]:
            self.assertIsNone(
                get(self.node_list, os.path.join(self.tempdir_path, "p1", p)))
            self.assertIsNotNone(get(self.node_list, os.path.join(dest, p)))
