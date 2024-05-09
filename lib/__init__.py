# -*- coding: utf-8 -*-
import os,platform,sys,time,types,atexit,time,subprocess
# 加载模块
def load_module(package,mod=None,area=None):
    # 导入模块
    module=__import__(package,fromlist=['xxx'])
    # 如果没有模块名，则返回模块
    if mod is None:
        if area:area[package]=module
        else:return module
    # 如果有模块名，则返回模块中的指定属性
    else:
        if area:area[mod]=getattr(module,mod)
        else:return getattr(module,mod)
# 删除模块
def delete_module(package,mod=None):
    # 获取模块列表
    modlist=load_module("sys").modules
    # 如果存在模块名，则删除指定模块
    if mod:del modlist[mod]
    # 否则删除指定包名
    else:del modlist[package]
# 重新加载模块
def reload_module(package,mod=None):
    # 删除模块
    delete_module(package,mod)
    # 休眠1秒
    time.sleep(1)
    # 重新加载模块
    return load_module(package,mod)
# 单例模式
def Singleton(cls):
    # 创建一个空字典
    _instance = {}
    # 定义一个单例方法
    def _singleton(*args, **kargs):
        # 如果类名不在字典中，则创建一个新的实例
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        # 返回字典中的实例
        return _instance[cls]
    # 返回单例方法
    return _singleton
# 判断是否为Python2
isPY2 = sys.version_info<(3,0,0)
# 判断是否为Python3
isPY3 = sys.version_info>(3,0,0)
if isPY2:
    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    locale=load_module("locale")
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

from lib.data import Edict,edict
OS=Edict(
    ClassName=platform.uname()[0],
    MachineName=platform.uname()[2],
    KernelVersion=platform.uname()[3],
    Type=platform.uname()[4],
    Module=Edict(load=load_module,reload=reload_module,delete=delete_module)
)
isWindows = OS["ClassName"]=="Windows"
isLinux   = OS["ClassName"]=="Linux"
if isLinux:
    os.update(dict(
        CPUCount=int(os.popen("nproc").read()),
        MemoryTotal=int(os.popen("free | awk 'NR==2{print $2}'").read()))
    )

# 如果全局变量里没有System则运行
from lib.system import system
if "System" not in globals():System=system()
