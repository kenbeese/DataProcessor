# codiing=utf-8
"""@DataProcessor.pipes
"""


__all__ = ["ConfManager", "InfoManager", "RunConf",
           "TagFilter", "meta", "project_choose"]

pipes_dics = {}

from . import RunConf, InfoManager, TagFilter, meta, project_choose
meta.register(filter_dic)
project_choose.register(filter_dic)
RunConf.register(pipes_dics)
InfoManager.register(pipes_dics)
TagFilter.register(pipes_dics)
