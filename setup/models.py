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
    score = db.Column(db.Integer())
    # the name of the player
    name = db.Column(db.String(30))
    mines = db.Column(db.Integer)
    difficulty = db.Column(db.String)


class GameInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    length = db.Column(db.Integer)
    updated_time = db.Column(db.Integer)
    game_over = db.Column(db.Integer, default=0)
    disabled_nodes = db.Column(MutableList.as_mutable(PickleType), default=[])
    start_time = db.Column(db.Float)
    leader_board = db.Column(db.Integer, default=0)
