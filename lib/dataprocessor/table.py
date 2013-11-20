# coding=utf-8
import os.path

from jinja2 import Template

from nodes import get


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
            value = str(dic_in[key])
        except KeyError:
            value = ""
        try:
            dic_out[key].append(value)
        except KeyError:
            dic_out[key] = [value]


class Table(object):

    """table widget class.

    Create table from dictionary in node.
    Also search dictionary recursively.

    Parameters
    ----------
    table_type : {'children', 'parents'}
        Table is composed of nodes in node[`table_type`].
    groups : list of dic, optional
        Specify elements in table for each group.
        Default is one group which get all of 'configure' key.
        one group has three keys at most.

    Examples
    --------
    >>> nodelist = [{'path': '/tmp', 'children': ['/tmp/run1', '/tmp/run0']},
    ...             {'path': '/tmp/run0', 'name': 'run0', 'comment': 'test',
    ...              'configure': {'nx':1, 'ny':2}},
    ...             {'path': '/tmp/run1', 'name': 'run1',
    ...              'configure': {'nx': 10, 'ny': 20}}]
    >>> tble = Table(nodelist[0], nodelist,
    ...              groups=[{'dict_path': ['configure']},
    ...                      {'items': ['comment', 'path'], 'name': 'node'}])
    >>> tble._table_data.table == [
    ...     {'nx': ['1', '10'], 'ny': ['2', '20']},
    ...     {'comment': ['test', ''], 'path': ['/tmp/run0', '/tmp/run1']}]
    >>> tble._table_data.type == 'table'
    >>> tble._table_data.tags == ['children']
    >>> tble._table_data.col_groupname == ['configure', 'node']
    >>> tble._table_data.row_name == ['run0', 'run1']
    >>> tble._table_data.col_name == [['nx', 'ny'], ['comment', 'path']]
    >>> tble._table_data.row_path == ['/tmp/run0', '/tmp/run1']
    >>>
    >>> html_str = tble.render()

    """

    def __init__(self, node, node_list, table_type="children",
                 groups=[{"dict_path": ["configure"],
                          "items": None, "name": None},
                         ]):
        if not table_type in node:
            raise RuntimeError("node has no '{0}' key".format(table_type))
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
