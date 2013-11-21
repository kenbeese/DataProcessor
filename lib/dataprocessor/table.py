# coding=utf-8
import os.path

from jinja2 import Template

from .nodes import get
from .exception import DataProcessorError


class _TableData(object):

    """table data manager."""

    def __init__(self, node, node_list, table_type, groups):
        self.type = "table"
        self.tags = [table_type]
        self.table = []

        self._dict_path = self.__get_dict_path(groups)
        self._linked_node = self.__get_linked_node(node_list, node[table_type]) # case: empty list

        self.col_groupname = self.__get_groupname(groups, self._dict_path)
        self.row_name = self.__get_valuelist(self._linked_node, "name") # case: node has no 'name' key.
        self.row_path = self.__get_valuelist(self._linked_node, "path")
        self.col_name = self.__get_col_name(groups, self._dict_path,
                                            self._linked_node)

        for idx in range(len(groups)):
            tble = {}
            for node in self._linked_node:
                dic = self.__get_dic_from_path(node, self._dict_path[idx])
                for key in self.col_name[idx]:
                    self.__copy_value(tble, dic, key)
            self.table.append(tble)

    def __get_dict_path(self, groups):
        dict_path = []
        for group in groups:
            if not "dict_path" in group or group["dict_path"] is None:
                dict_path.append([])
            else:
                dict_path.append(group["dict_path"])
        return dict_path

    def __get_groupname(self, groups, dict_path):
        groupname = []
        for idx in range(len(groups)):
            if not "name" in groups[idx] or groups[idx]["name"] is None:
                groupname.append("/".join(dict_path[idx])) # case: dict_path is not list.
            else:
                groupname.append(groups[idx]["name"])
        return groupname

    def __get_linked_node(self, node_list, path_list):
        linked_node = []
        for path in sorted(path_list):
            node = get(node_list, path)
            if not node is None:
                linked_node.append(node)
        return linked_node

    def __get_valuelist(self, dict_list, keyname):
        value = []
        for dic in dict_list:
            if keyname in dic:
                value.append(dic[keyname])
            else:
                value.append("")
        return value

    def __get_col_name(self, groups, dict_path, linked_node):
        col_name = []
        if not linked_node:
            return col_name
        for group in groups:
            group_idx = groups.index(group)
            dic = self.__get_dic_from_path(linked_node[0],
                                           dict_path[group_idx])
            if not "items" in group or group["items"] is None:
                col_name.append(self.__get_allkeys(dic))
            else:
                col_name.append(group["items"])
        return col_name

    def __get_allkeys(self, dic):
        keys = list(dic.keys())
        keys.sort()
        keys.sort(key=len)
        return keys

    def __get_dic_from_path(self, node, dict_path):
        dic = node
        for key in dict_path:
            dic = dic[key] # case: node has no key.
        return dic

    def __copy_value(self, dic_out, dic_in, key):
        try:
            value = dic_in[key]
            if type(value) == str:
                value = unicode(value, "utf-8")
            else:
                value = unicode(value)
        except KeyError:
            value = ""
        try:
            dic_out[key].append(value)
        except KeyError:
            dic_out[key] = [value]


class Table(object):

    """table widget class.

    Create table from dictionary in node.
    If node has dictionary in its values,
    also search dictionary recursively. (e.g. node[key1][key2]...[keyn])

    Parameters
    ----------
    table_type : {'children', 'parents'}
        Table is composed of nodes in node[`table_type`].
    groups : list of dic, optional
        Specify elements in table for each group.
        Default is one group which get all of 'configure' key.
        One group has three keys below at most.
        ----
        dict_path : list of str, optional
            List of key. Default is node itself.
            Search dictionary recursively by `dict_path`.
        items : list of str, optional
            List of key in dictionary specified by `dict_path`.
            Table has only items in `items`.
        name : str, optional
            Group name. Default is "/".join(`dict_path`).

    Examples
    --------
    >>> nodelist = [{'path': '/tmp', 'children': ['/tmp/run1', '/tmp/run0']},
    ...             {'path': '/tmp/run0', 'name': 'run0', 'comment': u'testあ',
    ...              'configure': {'nx':1, 'ny':2}},
    ...             {'path': '/tmp/run1', 'name': 'run1',
    ...              'configure': {'nx': 10, 'ny': 20}}]
    >>> tble = Table(nodelist[0], nodelist,
    ...              groups=[{'dict_path': ['configure']},
    ...                      {'items': ['comment', 'path'], 'name': 'node'}])
    >>> html_str = tble.render()

    """

    def __init__(self, node, node_list, table_type="children",
                 groups=[{"dict_path": ["configure"],
                          "items": None, "name": None},
                         ]):
        if not table_type in node:
            raise DataProcessorError("node has no '%s' key" % table_type)
        self._table_data = _TableData(node, node_list, table_type, groups)

    def render(self):
        """Get a piece of html for table.

        Returns
        -------
        str
            A piece of html composed of the parameters in constructor.

        """

        template = os.path.join(os.path.dirname(__file__),
                                "../../template/widget_table.html")
        with open(template, "r") as f:
            tmpl = Template(f.read())
        return tmpl.render(data=self._table_data)
