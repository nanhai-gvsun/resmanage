# -*- coding: utf-8 -*-
from .. import *
class edict(dict):
    _support=dict(json=load_module("json"))
    _preDefaultName="data_"
    def __str__(self):return self.toString()
    def __getattr__(self, key):
        if key not in self:setattr(self,key,None)
        elif isinstance(self[key],dict):self[key]=Edict(self[key])
        elif isinstance(self[key],list):
            self[key]=[Edict(self[key][i]) if isinstance(self[key][i],dict) else self[key][i] for i in range(len(self[key]))]
        return self[key]            
    def __setattr__(self, key, value):self[key] = value
    def update(self,*args,**kargs):
        if len(args)>=1:
            for d in args:
                if type(d)==list:
                    pass
                else:dict.update(self,*d)
        if len(kargs)>=1:dict.update(self,**kargs)
        return self
    def toString(self):
        try:return self._support["json"].dumps(self, ensure_ascii=False)
        except TypeError as e:return self._support["json"].dumps(self.toJson(), ensure_ascii=False)
    def toJson(self):
        ret=Edict()
        for key in [key for key in self if key[0]!="_"]:
            if callable(self[key]):ret[key]=str(self[key])
            elif isinstance(self[key],Edict):ret[key]=self[key].toJson()
            else:
                try:
                    self._support["json"].dumps({key:self[key]})
                    ret[key]=self[key]
                except TypeError as e:
                    ret[key]=str(self[key])
        return ret
    def toJsonString(self,*args):
        try:return self._support["json"].dumps(self, ensure_ascii=False, indent=4)
        except TypeError as e:return self._support["json"].dumps(self.toJson(), ensure_ascii=False, indent=4)



Edict=edict