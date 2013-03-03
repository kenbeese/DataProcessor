class func(object):
    def __init__(self, fn_list):
        self.fn_list = fn_list

    def call(self, funcname, *args):
        if len(args) == len(self.args(funcname)):
            return self.fn_list[funcname]["act"](*args)
        else:
            raise Warning("args is not match. this function is " + self.help(funcname))


    def help(self, funcname):
        return ("function   : " + str(funcname) + "\n" +
                "arguments  : " + str(self.fn_list[funcname]["args"]) + "\n" +
                "description: " + str(self.fn_list[funcname]["desc"]))

    def names(self):
        return self.fn_list.keys()

    def args(self, name):
        return self.fn_list[name]["args"]
