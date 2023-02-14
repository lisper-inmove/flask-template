# -*- coding: utf-8 -*-

from enum import IntEnum
from collections import namedtuple
from submodules.utils.sys_env import SysEnv
from submodules.utils.protobuf_helper import ProtobufHelper


class Constants:

    # 完全匹配
    EXACT_MATCH = 0x01
    # 前缀匹配
    PREFIX_MATCH = 0x02
    # 后缀匹配
    SUFFIX_MATCH = 0x03
    # 前缀,后缀匹配
    SP_MATCH = 0x04


class ObjStatus(IntEnum):

    # 0表示启用状态
    ACTIVE = 0x00
    # -1表示禁用状态
    INACTIVE = ~ACTIVE
    # 1表示删除状态
    DELETED = 0x01


class BaseCls:

    ENV_TEST = "test"
    ENV_PROD = "prod"

    def __init__(self, *args, **kargs):
        self.C = Constants
        self.PH = ProtobufHelper
        self.ObjStatus = ObjStatus
        self.ListObjCls = namedtuple("ListObjCls", ['objs', 'count'])

    @property
    def is_test_env(self):
        return SysEnv.get(SysEnv.RUNTIME_ENVIRONMENT, self.ENV_PROD) == self.ENV_TEST

    @property
    def is_prod_env(self):
        return SysEnv.get(SysEnv.RUNTIME_ENVIRONMENT, self.ENV_PROD) == self.ENV_PROD
