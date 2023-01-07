from . import db
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType


# every game is made up of nodes that the user can press to affect the game
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


# Game objects are created when a player wins a game, and the variables in this class are for what is displayed on
# every entry on the leaderboard
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # the score of the player(time when game was finished)
    score = db.Column(db.Integer())
    # the name of the player
    name = db.Column(db.String(30))
    # the mines and the difficulty to display on the leaderboard
    mines = db.Column(db.Integer)
    difficulty = db.Column(db.String)


# gameinfo is the info of the current game, and it is created for every game
class GameInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # just to save the length of the game and use if in the functions relationg to the game
    length = db.Column(db.Integer)
    # this is used to reset the game time on the front end when the back end is called to
    # avoid issues with the time lagging
    updated_time = db.Column(db.Integer)
    # this is a conditional variable that lets us know if the game was lost or won
    game_over = db.Column(db.Integer, default=0)
    # DELETE 'disabled_nodes' NO LONGER IN USE
    disabled_nodes = db.Column(MutableList.as_mutable(PickleType), default=[])
    # the start time variable holds values from the time module to keep track of when the game started and
    # used to update the 'updated_time'
    # up the time for the game
    start_time = db.Column(db.Float)
    # leaderboard is a conditional variable that is set to true if the user gets a high score, and it allows the player
    # box score to display
    leaderboard = db.Column(db.Integer, default=0)
