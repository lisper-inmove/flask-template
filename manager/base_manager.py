# -*- coding: utf-8 -*-

from functools import wraps

from base_cls import BaseCls
from submodules.utils.misc import Misc
from submodules.utils.idate import IDate
from view.errors import PopupError


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
        self._da = None
        self._init(*args, **kargs)

    def _init(self, *args, **kargs):
        pass

    def get_obj_by_id(self, id):
        if self._da is None:
            return None
        return self._da.get_obj_by_id(id)

    def update_obj(self, obj):
        if self._da is None:
            return None
        obj.update_time_sec = IDate.now_timestamp()
        return self._da.update_obj(obj)

    def delete_obj(self, obj):
        if self._da is None:
            return None
        obj.update_time_sec = IDate.now_timestamp()
        return self._da.delete_obj(obj)

    def list_objs(self, matcher, sortby=None, page=None, size=None):
        if self._da is None:
            return None
        objs = self._da.list_objs(matcher, sortby, page, size)
        return objs

    def create_obj(self, cls):
        obj = cls()
        obj.id = Misc.uuid()
        obj.create_time_sec = IDate.now_timestamp()
        obj.update_time_sec = IDate.now_timestamp()
        return obj

    def update_obj_status(self, obj, status):
        if status is None:
            return
        try:
            s = self.ObjStatus[status]
            obj.status = s
        except KeyError:
            raise PopupError('状态错误')
