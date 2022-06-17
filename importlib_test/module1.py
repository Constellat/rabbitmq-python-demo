#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/6/9 19:59
# @Author: niujianyu
# @File  : module1.py
class Module1:
    def __init__(self):
        self.a = 'aaaaa'

    def print_a(self):
        print("a: %s" % (self.a))

    def print_b(self):
        print("bbbbbbbb")

    @classmethod
    def print_class_method(cls):
        print("print_class_method: %s" % ('class_method'))

if __name__ == "__main__":
    Module1.print_b(None)

def test():
    print('test outer class')