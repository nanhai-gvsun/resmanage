# -*- coding: utf-8 -*-
from lib import *
import shutil,errno,stat

path=os.path.dirname(__file__)
SubmitObjective="github"
msg="test"
directory=os.path.abspath(os.path.join(path,".git"))

if isPY3:print(locale.getencoding())
elif isPY2:print(sys.getdefaultencoding())

def handle_remove_readonly(func, path, exc):
    excvalue = exc[1]
    if excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise


if os.path.exists(directory):
    shutil.rmtree(directory,onerror=handle_remove_readonly)


if SubmitObjective=="github":
    gitsource=os.path.abspath(os.path.join(path,"github"))
if os.path.exists(gitsource):
    shutil.copytree(gitsource,directory)

os.system("cd {path} && git add * && git commit -m '{msg}' && git push".format(path=directory,msg=msg))

if isPY3:print(locale.getencoding())
elif isPY2:print(sys.getdefaultencoding())