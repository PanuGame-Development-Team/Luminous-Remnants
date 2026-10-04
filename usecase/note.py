from ca import *
from entity.entity import Entity
class Note:
    def __init__(self):
        self.ind = "notes"
        self.nss = set[Entity.Namespace]()
    def set_note(self,n:Entity.Namespace,key:str,message:str) -> None:
        self.nss.add(n)
        n.dc(self.ind,dict)[key] = message
    def del_note(self,n:Entity.Namespace,key:str) -> None:
        self.nss.add(n)
        try:
            n.dc(self.ind,dict).pop(key)
            return True
        except:
            return False
    def get_messages(self) -> dict[str,list[str]]:
        ls = list(self.nss)
        res = {}
        ls.sort(key=lambda x:x.priority)
        for n in ls:
            res[n.name] = [n.d(self.ind)[i] for i in n.d(self.ind)]
        return res