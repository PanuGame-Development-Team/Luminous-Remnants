from ca import *
from entity.galaxy import Galaxy as _Galaxy
from entity.meteor import Meteor as _Meteor
from entity.picture import Picture as _Picture
from entity.star import Star as _Star
from entity.lib import Pos as _Pos,\
        Resource_id as _Resource_id,\
    ResourceManager as _ResourceManager,\
            average as _average
class Entity(Layer):
    Galaxy = _Galaxy
    Meteor = _Meteor
    Picture = _Picture
    Star = _Star
    Pos = _Pos
    Resource_id = _Resource_id
    ResourceManager = _ResourceManager
    average = _average