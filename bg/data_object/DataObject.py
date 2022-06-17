#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/6/10 15:12
# @Author: niujianyu
# @File  : DataObject.py
from bg.data_object.InnerObject import InnerObject


class DataObject:
    class_field = "class_field"
    default_class_field = "default_class_field"

    def __init__(self, private_field, inner_object):
        self.private_field = private_field
        self.inner_object = inner_object
        self.default_private_field = "default_private_field"

    def print(self):
        print("self.private_field: %s" % self.private_field)
        print("self.default_private_field: %s" % self.default_private_field)

    def get_private_field(self):
        print("get_private_field()")
        return self.private_field

    def get_default_private_field(self):
        print("get_default_private_field()")
        return self.default_private_field

    def set_private_field(self, private_field):
        print("set_private_field()")
        self.private_field = private_field

    def test_bg1(self, inner_object):
        self.set_private_field(self.private_field+"_test_bg1")
        print(self.get_private_field())
        print(self.get_default_private_field())
        print(self.get_class_field())
        print(self.get_default_class_field())
        print("------------------Inner Object---------------------")
        inner_object.print_content()

    @classmethod
    def get_class_field(cls):
        print("get_class_field()")
        return cls.class_field

    @classmethod
    def set_class_field(cls, class_field):
        print("set_class_field()")
        cls.class_field = class_field

    @classmethod
    def get_default_class_field(cls):
        print("get_default_class_field()")
        return cls.default_class_field

if __name__ == "__main__":
    inner_object = InnerObject()
    data_object = DataObject("DataObject", inner_object)
    data_object.test_bg1()