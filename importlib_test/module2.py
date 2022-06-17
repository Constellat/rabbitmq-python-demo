#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/6/9 19:59
# @Author: niujianyu
# @File  : module2.py

class Temp:
    def __init__(self, a):
        self.a = a


if __name__ == "__main__":
    import importlib
    module = importlib.import_module("module1")
    class_ins = getattr(module, 'Module1')
    a_class = class_ins()
    test_func = getattr(module, 'test')
    class_b_func = getattr(class_ins, 'print_b')
    class_a_func = getattr(class_ins, 'print_a')
    class_func = getattr(class_ins, 'print_class_method')
    print(type(class_ins))
    print(type(test_func))
    print(type(class_b_func))
    print(type(class_a_func))
    print(type(class_func))
    test_func()
    class_b_func(class_ins)
    an_function = class_ins.print_b
    # 类获得的实例方法，需要传入至少一个参数代替self
    an_function(self=class_ins)
    a_function = a_class.print_b
    # 对象的实例方法不需要传self
    a_function()
    # 包含self操作的实例方法，使用其他对象替换不影响执行
    class_a_func(Temp(a='this is another object'))
    # 类的类方法，不需要传入参数，通过类调用就会自动传入cls
    class_func()

