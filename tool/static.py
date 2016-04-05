# Implement of staic_var


def staticVar(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate
