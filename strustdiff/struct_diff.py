from symbols import *

class CompactJsonDiffSyntax(object):

    def emit_value_diff(self, a, b, s):
        if s == 1.0:
            return {}
        else:
            return {b} if isinstance(b, dict) else b

    def emit_dict_diff(self, a, b, s, added, changed, removed):
        if s == 0.0:
            return {b} if isinstance(b, dict) else b
        elif s == 1.0:
            return {}
        else:
            changed.update(added)
            if removed:
                changed[delete] = list(removed.keys())
            return changed

builtin_syntaxes = {
    'compact': CompactJsonDiffSyntax()
}

class JsonDiffer():

    class Options():
        pass

    def __init__(self, syntax='compact'):
        self.options = JsonDiffer.Options()
        self.options.syntax = builtin_syntaxes.get(syntax)
        self._symbol_map = {
            '$' + symbol.label: symbol
            for symbol in _all_symbols_
        }

    def _obj_diff(self, a, b):
        if a is b:
            return self.options.syntax.emit_value_diff(a, b, 1.0), 1.0
        if isinstance(a, dict) and isinstance(b, dict):
            return self._dict_diff(a, b)
        elif a != b:
            return self.options.syntax.emit_value_diff(a, b, 0.0), 0.0
        else:
            return self.options.syntax.emit_value_diff(a, b, 1.0), 1.0

    def _dict_diff(self, a, b):
        remove = {}
        add = {}
        change = {}

        nremove = 0
        nadd = 0
        nmatch = 0
        smatch = 0.0

        for a_key, a_value in a.items():
            b_value = b.get(a_key, missing)
            #如果b没有该key，则记录到remove字典中
            if b_value is missing:
                nremove += 1
                remove[a_key] = a_value
            else:
                #如果b有该key,则匹配数+1
                nmatch += 1
                #判断value是否还有字典，如果其中一个已经没有字典了，判断值是否相等，相等s=1，不相等s=0则记录
                d, s = self._obj_diff(a_value, b_value)
                #如果不相等，则记录该区别到change字典中
                if s < 1.0:
                    change[a_key] = d
                smatch += 0.5 + 0.5 * s
        for b_key, b_value in b.items():
            #如果b的key不在a中，则记录到add字典中
            if b_key not in a:
                nadd += 1
                add[b_key] = b_value
        n_tot = nremove + nmatch + nadd
        s = smatch / n_tot if n_tot != 0 else 1.0
        return self.options.syntax.emit_dict_diff(a, b, s, add, change, remove),s

    def diff(self, a, b):
        d, s = self._obj_diff(a, b)
        return d


def diff(a, b, cls=JsonDiffer, **kwargs):
    return cls(**kwargs).diff(a, b)



# def to_dict_file(jsonfile):
#     with open(jsonfile, "r", encoding='utf-8') as f:
#         f = f.read()
#         dictfile = json.loads(f)
#         return dictfile
#
# def to_dict_file1(jsonfile):
#     with open(jsonfile, "r", encoding='utf-8') as f:
#         dictfile = json.load(f)
#         return dictfile
#
#
# if __name__=='__main__':
#     x = diff(to_dict_file('61_.json'), to_dict_file('87_.json'), syntax='compact')
#     print(x)
