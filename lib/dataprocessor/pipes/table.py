# coding=utf-8
from jinja2 import Template

from ..nodes import get


class _TableData(object):
    """
    table data manager.
    """

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
                dic = self.__get_dic_from_path(node, self.dict_path[idx])
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
        for group in groups:
            if not "name" in group or group["name"] is None:
                groupname.append("/".join(dict_path)) # case: dict_path is not list.
            else:
                groupname.append(group["name"])
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
    """
    Add parents or children information table to 'widgets' key.
    Alignment sequence of table is pre_meta, confs and post_meta from left.

    notes:
    If any one of pre_meta and post_meta is same as confs,
    this function become something wrong.

    Parameters
    ----------
    table_type : string, optional
        table_type is 'children' or 'parents'.
    pre_meta : list, optional
        Specify any of key in node.
        pre_meta are placed at left side of table.
    post_meta : list, optional
        Specify any of key in node.
        post_meta are placed at right side of table.
    confs : list, optional
        Specify any of key in node['configure'].
        If not specified, confs receive all of key in node['configure'].

    Examples
    --------
    >>> ## second child has no 'comment' key. ##
    >>> nodelist = [{'path': '/tmp', 'children': ['/tmp/run1', '/tmp/run0']},
    ...             {'path': '/tmp/run0', 'name': 'run0', 'comment': 'test',
    ...              'configure': {'nx':1, 'ny':2}},
    ...             {'path': '/tmp/run1', 'name': 'run1',
    ...              'configure': {'nx': 10, 'ny': 20}}]
    >>> tble = Table(nodelist[0], nodelist)
    >>> tble.widget == {
    ...     'type': 'table', 'tags': ['children'],
    ...     'data': {'comment': ['test', None], 'name': ['run0', 'run1'],
    ...              'tags': [None, None], 'nx': [1, 10], 'ny': [2, 20],
    ...              'header': ['name', 'comment', 'nx', 'ny', 'tags'],
    ...              'path': ['/tmp/run0', '/tmp/run1']}}
    True
    >>>
    >>> ## second child has no 'configure' key. ##
    >>> nodelist = [{'path': '/tmp', 'children': ['/tmp/run1', '/tmp/run0']},
    ...             {'path': '/tmp/run0', 'name': 'run0',
    ...              'configure': {'nx': 10, 'ny': 20}},
    ...             {'path': '/tmp/run1', 'name': 'run1'}]
    >>> tble = Table(nodelist[0], nodelist, pre_meta=["name"])
    >>> tble.widget = {
    ...     'type': 'table', 'tags': ['children'],
    ...     'data': {'name': ['run0', 'run1'], 'tags': [None, None],
    ...              'nx': [10, None], 'ny': [20, None],
    ...              'header': ['name', 'nx', 'ny', 'tags'],
    ...              'path': ['/tmp/run0', '/tmp/run1']}}
    >>>
    >>> ## 'configure' of first child is empty. ##
    >>> nodelist = [{'path': '/tmp', 'children': ['/tmp/run1', '/tmp/run0']},
    ...             {'path': '/tmp/run0', 'name': 'run0', 'configure': {}},
    ...             {'path': '/tmp/run1', 'name': 'run1',
    ...              'configure': {'nx': 10, 'ny': 20}}]
    >>> tble = Table(nodelist[0], nodelist, pre_meta=["name"])
    >>> tble.widget == {
    ...     'type': 'table', 'tags': ['children'],
    ...     'data': {'path': ['/tmp/run0', '/tmp/run1'],
    ...              'header': ['name', 'tags'],
    ...              'name': ['run0', 'run1'], 'tags': [None, None]}}
    True
    >>>
    >>>
    >>> html = tble.render('../../../template/widget_table.html', 'o.html')
    """

    def __init__(self, node, node_list, table_type="children",
                 groups=[{"dict_path": ["configure"],
                          "items": None, "name": None},
                         ]):
        if not table_type in node:
            raise RuntimeError("node has no '{0}' key".format(table_type))
        self.table_data = self._TableData(node, node_list, table_type, groups)

    def render(self, template, output_html="output.html"):
        with open(template, "r") as f:
            tmpl = Template(f.read())
        return tmpl.render(self.widget, output_html=output_html)
