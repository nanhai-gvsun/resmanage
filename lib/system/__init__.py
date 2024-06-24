# -*- coding: utf-8 -*-
from .. import Singleton
from .console import gsConsole
from .process import gsProcess
@Singleton
class system:
    console=gsConsole()
    process=gsProcess()
    pass

