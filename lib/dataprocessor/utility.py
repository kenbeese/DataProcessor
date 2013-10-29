# coding=utf-8


def path_expand(path):
    """
    Get abstract path
    """
    return os.path.expanduser(os.path.abspath(path))


def check_directory(path, silent=True):
    """
    Check whether the directory exists.
    If it does not exist, it will be created.

    @param silent if True, ask whether create directory.
    """
    dir_path = path_expand(path)
    if not os.path.isdir(dir_path):
        if os.path.exists(dir_path):
            raise DataProcessorError("Another file already exists in %s" % dir_path)
        if not silent:
            ans = raw_input("Create directory(%s)? [y/N]" % dir_path)
            if ans not in ["yes", "y"]:
                raise DataProcessorError("Figure directory cannot be created.")
        os.makedirs(dir_path)
    return dir_path


if __name__ == "__main__":
    import doctest
    doctest.testmod()
