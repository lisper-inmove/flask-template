# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask_cors import CORS
from submodules.utils.sys_env import SysEnv
SysEnv.set(SysEnv.APPROOT, os.getcwd())
from view.initblueprint import InitBlueprint

app = Flask(SysEnv.get(SysEnv.APPNAME, "demo"))

InitBlueprint(app)
CORS(app)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="服务器", default="0.0.0.0")
    parser.add_argument("--port", help="端口", default=6003)
    parser.add_argument("--debug", help="调试模式", default=False, action="store_true")

    args = parser.parse_args()

    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug
    )
