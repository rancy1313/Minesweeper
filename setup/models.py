from . import db
from sqlalchemy.sql import func
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType


class Nodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # value is the number of mines touching the node
    # if value == -1 then that means it is a bomb
    value = db.Column(db.Integer, default=0)
    # 0 mean hidden / 1 means displayed
    status = db.Column(db.Integer, default=0)
    # list of node ids where index represents the surrounding node
    # I decided on the order to be clockwise starting from top
    # [top, top-right, right, bottom-right, bottom, bottom-left, left, top-left]
    surrounding_nodes = db.Column(MutableList.as_mutable(PickleType), default=[0, 0, 0, 0, 0, 0, 0, 0])


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # the score of the player
    score = db.Column(db.String(20))
    # the name of the player
    name = db.Column(db.String(30))
    bombs = db.Column(db.Integer)