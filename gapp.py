# -*- coding: utf-8 -*-

import argparse
import os

from submodules.utils.sys_env import SysEnv
SysEnv.set(SysEnv.APPROOT, os.getcwd())
from view.gview_port import Api


parser = argparse.ArgumentParser()
parser.add_argument("--host", help="服务器", default="[::]:")
parser.add_argument("--port", help="端口", default=9003)
parser.add_argument("--workers", help="线程数", default=10)

args = parser.parse_args()
api = Api()
api.run(args.host, args.port, args.workers)
