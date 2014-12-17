# coding=utf-8
import argparse
from .exception import DataProcessorError


def _escape_strings(strings):
    r"""escape to squarebracket and doublequote.

    >>> print(_escape_strings("hoge"))
    hoge
    >>> print(_escape_strings("[hoge"))
    \[hoge
    >>> print(_escape_strings("hoge]"))
    hoge\]
    >>> print(_escape_strings("[hoge]"))
    \[hoge\]
    >>> print(_escape_strings('[ho"ge]'))
    \[ho\"ge\]
    >>> print(_escape_strings("ho'ge"))
    ho'\''ge

    """
    target_chars = "[]\"`"
    ret = []
    if strings is None:
        return ""
    for string in strings:
        if string in target_chars:
            string = '\\' + string
        if string is "'":
            string = "'\\''"
        ret.append(string)
    return "".join(ret)


def _normalize_strings(strings):
    return ' '.join(_escape_strings(strings).split())


class CompletionGenerator(object):

    """Generator of Zsh Completion Function.

    Since this class uses some inner function of argparse,
    this does not work well in some version of argparse.
    This is tested only on argparse of python 2.7.5.

    Attributes
    ----------
    command_name : str
        command name of completion
    parser : argparse.ArgumentParser
        parser of command

    Methods
    -------
    get()
        returns string of Zsh completion function

    """

    def __init__(self, commandname, parser):
        self.commandname = commandname
        self.parser = parser

    def _main_function(self):
        ret = []
        ret.append("")
        ret.append("function _%s (){" % self.commandname)
        ret.append("    typeset -A opt_args")
        ret.append("    local context state line\n")
        ret.append("    integer int=1\n")
        ret.append("    _arguments -w -s -S \\")
        actions = self.parser._actions
        for action in actions:
            opt_str = self._get_option_or_choice_string(action)
            if opt_str:
                ret.append("        " + opt_str)
        if self._get_subparser():
            ret.append("        ':subcmd:->subcmd' \\")
            ret.append(
                "        '*::subcmd-options-or-args:->subcmd-options-or-args'")
            casestring = """
    case $state in
        subcmd)
            _%s_subcmd_list && ret=0
            ;;
        subcmd-options-or-args)
            local curcontext=$curcontext
            curcontext=${curcontext%%:*:*}:%s-$words[1]:
            if (( $+functions[_%s-$words[1]] )); then
                _call_function ret _%s-$words[1]
            else
                _files && ret=0
            fi
            ;;
    esac
""" % (self.commandname, self.commandname, self.commandname, self.commandname)
            ret.append(casestring)
        else:
            ret.append("        '*::arguments:_files'")
            ret.append("    ret=0")
        ret.append("    return ret")
        ret.append("}\n")
        return "\n".join(ret)

    def _subcmd_function(self, subcmd_name):
        ret = []
        ret.append("")
        ret.append("function _%s-%s (){" % (self.commandname, subcmd_name))
        ret.append("    typeset -A opt_args")
        ret.append("    local context state line\n")
        ret.append("    _arguments -w -s -S \\")

        subparser = self._get_subparser()
        parser = subparser.choices[subcmd_name]
        actions = parser._actions
        for action in actions:
            opt_str = self._get_option_or_choice_string(action)
            if opt_str:
                ret.append("        " + opt_str)

        ret.append(
            "        '*::arguments:_files'")
        ret.append("}\n")
        return "\n".join(ret)

    def _subcmd_list_function(self):
        prefmt = """
function _%s_subcmd_list() {
    local -a subcmd_list
    subcmd_list=(
        """ % self.commandname
        aftfmt = """
    )
    _describe -t subcmd 'subcommand list' subcmd_list && return
}
"""
        # extract subcmd name and the help
        subcmds_with_help = {}
        subparser = self._get_subparser()
        for action in subparser._choices_actions:
            subcmds_with_help[action.dest] = _normalize_strings(action.help)

        # for subcmd without help
        for subcmdname in self._get_subcmd_list():
            if subcmdname not in subcmds_with_help:
                subcmds_with_help[subcmdname] = ""
        body = []
        for name, help in subcmds_with_help.items():
            body.append("%s:'%s'" % (name, help))
        return prefmt + "\n        ".join(body) + aftfmt

    def _get_subcmd_list(self):
        return self._get_subparser().choices.keys()

    def _get_option_string(self, action):
        argfmt = ""
        if not action.nargs and isinstance(action, argparse._StoreAction):
            argfmt = ": :_files"
        if isinstance(action.nargs, int) and action.nargs > 0:
            argfmt = ": :_files" * action.nargs
        if action.nargs == '?':
            argfmt = ":: :_files"
        if action.nargs == "+":
            # 10 is hard coding.
            argfmt = ": :_files" + ":: :_files" * 10
        if action.nargs == '*':
            # 10 is hard coding.
            argfmt = ":: :_files" * 10
        if action.choices:
            argfmt = self._get_choice_string(action)
        # for existing both long and short option
        if len(action.option_strings) == 2:
            short_opt = action.option_strings[0]
            long_opt = action.option_strings[1]
            help = _normalize_strings(action.help)
            if help:
                help = "[" + help + "]"
            return "'(%s %s)'{%s,%s}'%s%s' \\" % (
                short_opt, long_opt, short_opt, long_opt, help, argfmt)
        # for one option
        if len(action.option_strings) == 1:
            help = _normalize_strings(action.help)
            if help:
                help = "[" + help + "]"
            return "'(%s)%s%s%s' \\" % (action.option_strings[0],
                                        action.option_strings[0], help, argfmt)

    def _get_choice_string(self, action):
        return "': :(%s)' \\" % (" ".join(action.choices))

    def _get_option_or_choice_string(self, action):
        if len(action.option_strings) == 0 and \
           action.choices and \
           not isinstance(action, argparse._SubParsersAction):
            return self._get_choice_string(action)
        else:
            return self._get_option_string(action)

        # for choice argument

    def _get_subparser(self):
        ret = []
        for action in self.parser._actions:
            if isinstance(action, argparse._SubParsersAction):
                ret.append(action)
        if len(ret) > 1:
            raise DataProcessorError(
                "Does not support two or more subparsers")
        if ret:
            return ret[0]
        else:
            return None

    def get(self):
        """Get zsh completion function string."""
        # func = getattr(self, "_get_%s_format" % self.output_format)
        # return func()
        header = "#compdef %s" % self.commandname
        footer = "_%s" % self.commandname
        body = self._main_function()
        subcmd_functions = []
        if self._get_subparser():
            subcmd_functions = [
                self._subcmd_function(subcmdname)
                for subcmdname in self._get_subcmd_list()]
            body = "\n".join(subcmd_functions) + \
                self._subcmd_list_function() + body
        body = header + body + footer
        return body
