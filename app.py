# -*- coding: utf-8 -*-

from flask import Flask
from view.initblueprint import InitBlueprint
from submodules.utils.sys_env import SysEnv

app = Flask(SysEnv.get(SysEnv.APPNAME, "demo"))

InitBlueprint(app)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="服务器", default="127.0.0.1")
    parser.add_argument("--port", help="端口", default=6003)
    parser.add_argument("--debug", help="调试模式", default=True, action="store_true")

    args = parser.parse_args()

    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug
    )
