# coding=utf-8


def __append(vals, l, d):
    for c in l:
        if c in d:
            vals.append(d[c])
        else:
            vals.append("")


def dump(run_list, csv_filename, comma=","):
    result_list = []
    confs = []
    for run in run_list:
        if "path" not in run or "meta" not in run or "configure" not in run:
            continue
        conf = run["configure"]
        for c in conf:
            if c not in confs:
                confs.append(c)
        result_list.append(run)
    confs.sort()
    confs.sort(key=len)

    pre_meta = ["name", "date"]
    post_meta = ["tags", "comment"]

    with open(csv_filename, 'w') as f:
        f.write(comma.join(pre_meta) + comma + comma.join(confs)
                + comma + comma.join(post_meta)+'\n')
        for run in result_list:
            vals = []
            __append(vals, pre_meta, run["meta"])
            __append(vals, confs, run["configure"])
            __append(vals, post_meta, run["meta"])
            f.write(comma.join(vals) + '\n')


def register(pipes_dics):
    pipes_dics["output_csv"] = {
        "func": dump,
        "args": ["csv_filename"],
        "desc": "output to csv",
    }
