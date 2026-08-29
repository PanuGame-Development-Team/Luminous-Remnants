from ca import *
from usecase.variables import var as _var
from usecase.lib import Event as _Event
from usecase.controller import Controller as _Controller
from usecase.dataprovider import DataProvider as _DataProvider
from usecase.galaxy import Galaxy as _Galaxy
from usecase.handler import Handler as _Handler
from usecase.meteor import Meteor as _Meteor
from usecase.picture import Picture as _Picture
from usecase.renderer import Renderer as _Renderer
from usecase.star import Star as _Star
from entity.entity import Entity as _Entity
class UseCase(Layer):
    var = _var
    Event = _Event
    Controller = _Controller
    DataProvider = _DataProvider
    Galaxy = _Galaxy
    Handler = _Handler
    Meteor = _Meteor
    Picture = _Picture
    Renderer = _Renderer
    Star = _Star
    Entity = _Entity