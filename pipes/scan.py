
def __get_dirs(path):
    return os.walk(path).next()[1]

import os
import time
def __date(path):
    stat = os.stat(path)
    last_modified = stat.st_mtime
    return time.ctime(last_modified)

def directory(run_list,root):
    root = os.path.abspath(os.path.expanduser(root))
    projects = __get_dirs(root)
    for project in projects:
        project_path = os.path.join(root,project)
        run_dirs = __get_dirs(project_path)
        for run_dir in run_dirs:
            path = os.path.join(project_path,run_dir)
            run_list.append({"path" : path,"meta" : {"name" : run_dir, "project" : project, "date" : __date(path), }, }) 
    return run_list

def register(pipe_dics):
    pipe_dics["scan_directory"] = {
        "func" : directory,
        "args" : ["root_path"],
        "desc" : "scan direcoty structure",
        }

if __name__ == "__main__":
    run_list = directory([],"~/data")
    print(run_list)
