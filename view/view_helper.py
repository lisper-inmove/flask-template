# -*- coding: utf-8 -*-

import os
import importlib.util
from pathlib import Path

from submodules.utils.sys_env import SysEnv
from submodules.utils.logger import Logger

logger = Logger()


class ViewHelper:

    def __init__(self, directory):
        self.directory = directory
        self.ctrls = dict()

    def load_ctrl(self, path=None):
        """加载所有ctrl."""
        if path is None:
            root_dir = SysEnv.get(SysEnv.APPROOT)
            path = os.path.join(root_dir, self.directory)
        for root, dirs, files in os.walk(path):
            for directory in dirs:
                self.load_ctrl(os.path.join(root, directory))
            for _f in files:
                self.load_ctrl_from_file(os.path.join(root, _f))

    def load_ctrl_from_file(self, filepath):
        """加载某一个ctrl."""
        if not filepath.endswith("py"):
            return
        filename = Path(filepath).name
        if filename.startswith(".#"):  # 忽略emacs生成的临时文件
            return
        spec = importlib.util.spec_from_file_location(self.directory, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for attr in module.__dict__.keys():
            if attr.startswith("__"):
                continue
            _ctrl = module.__dict__.get(attr)
            if not hasattr(_ctrl, "___name___"):
                continue
            if _ctrl.___name___ in self.ctrls:
                continue
            logger.info(f"导入ctrl: {_ctrl} {id(self.ctrls)}")
            self.ctrls.update({_ctrl.___name___: _ctrl})
