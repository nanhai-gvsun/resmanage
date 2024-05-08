# -*- coding: utf-8 -*-
from ...lib import *
from console import gsConsole
from process import gsProcess

@Singleton
class system:
    console=gsConsole()
    process=gsProcess()
    pass

