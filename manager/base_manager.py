# -*- coding: utf-8 -*-

from functools import wraps

from base_cls import BaseCls
from submodules.utils.misc import Misc
from submodules.utils.idate import IDate


def ignore_none_argument(fn):
    """如果参数有None直接返回，不调用fn."""
    @wraps(fn)
    def inner(*args, **kargs):
        has_none_param = False
        for arg in args:
            if arg is None:
                has_none_param = True
                break
        for _, value in kargs.items():
            if value is None:
                has_none_param = True
                break
        if has_none_param:
            return
        return fn(*args)
    return inner


class BaseManager(BaseCls):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self._init(*args, **kargs)

    def _init(self, *args, **kargs):
        pass

    def create_obj(self, cls):
        obj = cls()
        obj.id = Misc.uuid()
        obj.create_time_sec = IDate.now_timestamp()
        obj.update_time_sec = IDate.now_timestamp()
        return obj

    def update_obj(self, obj):
        obj.create_time_sec = IDate.now_timestamp()
        obj.update_time_sec = IDate.now_timestamp()
