# -*- coding: utf-8 -*-

import os
import importlib.util

from flask import Blueprint
from submodules.utils.protobuf_helper import ProtobufHelper as PH
from submodules.utils.sys_env import SysEnv
from submodules.utils.logger import Logger
from view.unify_response import UnifyResponse

name = "view-port"
_view_port = Blueprint(name, name, url_prefix="/<string:source>")

ctrls = dict()

logger = Logger()


def load_ctrl(path=None):
    """加载所有ctrl."""
    if path is None:
        root_dir = SysEnv.get(SysEnv.APPROOT)
        path = os.path.join(root_dir, "ctrl")
    for root, dirs, files in os.walk(path):
        for directory in dirs:
            load_ctrl(os.path.join(root, directory))
        for _f in files:
            load_ctrl_from_file(os.path.join(root, _f))


def load_ctrl_from_file(filepath):
    """加载某一个ctrl."""
    if not filepath.endswith("py"):
        return
    filename = os.path.basename(filepath)
    if filename == "base_ctrl.py":
        return
    spec = importlib.util.spec_from_file_location('ctrl', filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for attr in module.__dict__.keys():
        if attr.startswith("__"):
            continue
        _ctrl = module.__dict__.get(attr)
        if not hasattr(_ctrl, "___name___"):
            continue
        if _ctrl.___name___ in ctrls:
            continue
        logger.info(f"导入ctrl: {_ctrl} {id(ctrls)}")
        ctrls.update({_ctrl.___name___: _ctrl})


@_view_port.route("/<string:operate>", methods=["POST"])
def view_port(source, operate):
    """视图层."""
    ctrl = ctrls[source](operate=operate)
    result = ctrl.do_operate()
    return UnifyResponse.R(PH.to_json(result))


load_ctrl()
