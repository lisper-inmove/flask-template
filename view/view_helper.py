# -*- coding: utf-8 -*-

import os
import re
import inspect
import importlib.util
from pathlib import Path

from submodules.utils.sys_env import SysEnv
from submodules.utils.logger import Logger

from ctrl.base_ctrl import BaseCtrl

logger = Logger()


class ViewHelper:

    pattern = re.compile('(?!^)([A-Z]+)')

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
            if not inspect.isclass(_ctrl):
                continue
            if not issubclass(_ctrl, BaseCtrl):
                continue
            if _ctrl == BaseCtrl:
                continue
            snake_name = self.pattern.sub(r'_\1', _ctrl.__name__).lower()
            name = "_".join(snake_name.split("_")[:-1])
            if name in self.ctrls:
                continue
            self.ctrls.update({name: _ctrl})
            logger.info(f"导入ctrl: {_ctrl} {self.ctrls}")
