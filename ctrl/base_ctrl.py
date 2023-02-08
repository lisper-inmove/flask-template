# -*- coding: utf-8 -*-

from flask import request

from base_cls import BaseCls
from view.errors import PopupError


class BaseCtrl(BaseCls):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.operate = kargs.get('operate', None)
        self._manager = None
        self._OPF = dict()
        self._init(*args, **kargs)

    def _init(self, *args, **kargs):
        """子类要有自己的初始化工作就重载此函数."""
        pass

    def get_obj_by_id(self, id):
        if self._manager is None:
            return None
        return self._manager.get_obj_by_id(id)

    def update_obj(self, obj):
        if self._manager is None:
            return None
        return self._manager.update_obj(obj)

    def delete_obj(self, obj):
        if self._manager is None:
            return None
        return self._manager.delete_obj(obj)

    def list_objs(self, matcher, sortby=None, page=None, size=None):
        if self._manager is None:
            return None
        return self._manager.list_objs(matcher, sortby, page, size)

    def get_param(self, key, default=None):
        method = request.method
        if method == "POST":
            return request.get_json().get(key, default)
        elif method == "GET":
            return request.args.get(key, default)
        return default

    def get_header_param(self, key, default):
        return request.headers.get(key, default)

    def do_operate(self):
        if self.operate is None:
            raise PopupError(f"操作未实现: {self.operate}")
        if self.operate not in self._OPF:
            raise PopupError(f"操作未实现: {self.operate}")
        return self._OPF[self.operate]()
