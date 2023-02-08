# -*- coding: utf-8 -*-

from collections import namedtuple
from submodules.utils.sys_env import SysEnv


class Constants:

    # 完全匹配
    EXACT_MATCH = 0x01
    # 前缀匹配
    PREFIX_MATCH = 0x02
    # 后缀匹配
    SUFFIX_MATCH = 0x03
    # 前缀,后缀匹配
    SP_MATCH = 0x04


class BaseCls:

    ENV_TEST = "test"
    ENV_PROD = "prod"

    def __init__(self, *args, **kargs):
        self.C = Constants
        self.ListObjCls = namedtuple("ListObjCls", ['objs', 'count'])

    @property
    def is_test_env(self):
        return SysEnv.get(SysEnv.RUNTIME_ENVIRONMENT, self.ENV_PROD) == self.ENV_TEST

    @property
    def is_prod_env(self):
        return SysEnv.get(SysEnv.RUNTIME_ENVIRONMENT, self.ENV_PROD) == self.ENV_PROD
