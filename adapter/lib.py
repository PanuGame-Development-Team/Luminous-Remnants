from adapter.settings import *
from entity.lib import Pos
def find_nearest(c_pos:Pos,objectls:list,getpos,get_id=None):
    mdis = 1e9
    index = None
    for obj in objectls:
        pos:Pos = getpos(obj)
        lpos = Pos(pos.x - GENERAL.GRAPH_WIDTH * pos.stx,pos.y,pos.stx,pos.sty)
        rpos = Pos(pos.x + GENERAL.GRAPH_WIDTH * pos.stx,pos.y,pos.stx,pos.sty)
        distance = min(pos - c_pos,rpos - c_pos,lpos - c_pos)
        if distance < mdis:
            if get_id:
                index = get_id(obj)
            else:
                index = obj
            mdis = distance
    return mdis,index