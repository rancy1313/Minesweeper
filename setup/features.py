from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory, jsonify
from .models import Nodes, GameInfo, Game
from sqlalchemy import desc
from . import db
import random
import os
import time as t

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, 'images/')
if not os.path.isdir(target):
    os.mkdir(target)
features = Blueprint('features', __name__)


# to get mine image
@features.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory('images', filename)


# this function is for the home page
@features.route('/', methods=['GET'])
def start():
    # retrieve the test games by id to delete the oldest games
    tests = db.session.query(Game).filter_by(mines=4).order_by(desc(Game.id)).all()
    # if there are over 5 games then we delete the oldest game
    if len(tests) > 5:
        for i in range(len(tests)):
            # delete any test over 9(keep 5 tests)
            if i > 4:
                db.session.delete(tests[i])
    # I have it set up to save the top 10 games for each game mode(minus test mode)
    # gets easy games by score to delete the games with the lowest scores
    easy = db.session.query(Game).filter_by(mines=15).order_by(desc(Game.score)).all()
    # if there are over 5 games then we delete the oldest game
    if len(easy) > 10:
        # loop over retrieved games
        for i in range(len(easy)):
            # delete any game over 9(keep 10 games)
            if i > 9 and easy[i].score != 0:
                db.session.delete(easy[i])
    # gets medium games by score to delete the games with the lowest scores
    medium = db.session.query(Game).filter_by(mines=34).order_by(desc(Game.score)).all()
    # if there are over 5 games then we delete the oldest game
    if len(medium) > 10:
        # loop over retrieved games
        for i in range(len(medium)):
            # delete any game over 9(keep 10 games)
            if i > 9 and medium[i].score != 0:
                db.session.delete(medium[i])
    # gets hard games by score to delete the games with the lowest scores
    hard = db.session.query(Game).filter_by(mines=94).order_by(desc(Game.score)).all()
    # if there are over 5 games then we delete the oldest game
    if len(hard) > 10:
        # loop over retrieved games
        for i in range(len(hard)):
            # delete any game over 9(keep 10 games)
            if i > 9 and hard[i].score != 0:
                db.session.delete(hard[i])
    # we do not delete any lucky games(score 0 except test lucky games) because the chances of getting those are rare
    # and there might not ever be that many for it to be a problem
    db.session.commit()
    # the leader board is all the saved games
    leaderboard = db.session.query(Game).order_by(Game.score).all()
    return render_template('start.html', leaderboard=leaderboard)


# this function sets up the grid for the game mode chosen
# this function is needed because none of the nodes have values when the grid is first set up because I added a feature
# ,so that the first node chosen is sure to not be a mine. Moreover, I make sure the first node chosen has a value of 0,
# so that it is easier for the user.
@features.route('/set-game-grid/<int:length>', methods=['POST', 'GET'])
def set_game_grid(length):
    # Only one game info is ever needed, so we delete the last one and create a new one
    GameInfo.query.delete()
    # delete every node before since they become useless
    Nodes.query.delete()
    db.session.commit()
    game_info = GameInfo(length=length, updated_time=0)
    db.session.add(game_info)
    # the game list contains every node of the game
    game = []
    # the dimensions of the game are length x length. This can be changed to have the width be a fraction of the
    # length to make it easier for the players.
    for i in range(length * length):
        node = Nodes()
        db.session.add(node)
        game.append(node)
    db.session.commit()
    # this loop goes  through every node in the game and adds the ids of the surrounding nodes
    # the position on the list correlates to the position of the surrounding node
    # [top(0), top-right(1), right(2), bottom-right(3), bottom(4), bottom-left(5), left(6), top-left(7)]
    for i in range(length * length):
        # if i < length that means we are on the top row and there are no nodes above the first row,
        # so set first index to -1
        if i < length:
            # no nodes above, so insert -1 at position at 0(top)
            game[i].surrounding_nodes[0] = -1
            # no nodes above, so insert -1 at position at 1(top-right)
            game[i].surrounding_nodes[1] = -1
            # no nodes above, so insert -1 at position at 7(top-left)
            game[i].surrounding_nodes[7] = -1
        else:
            # that means the node should have another node above it, insert that top node's id at position 1
            game[i].surrounding_nodes[0] = game[i - length].id
            # we can't assign a value to the top-left node for any node on the left most column
            if i % length != 0:
                # insert top-left node id
                game[i].surrounding_nodes[7] = game[i - length - 1].id
            # i  % length == length - 1 then we are at the right most column, and we do not assign ids to the
            # right side of those nodes
            if i % length != length - 1:
                # insert top-right node id
                game[i].surrounding_nodes[1] = game[i - length + 1].id
        # if i % length then we are at the left most column and there are no nodes to the right of that column
        if i % length == 0:
            # there are no nodes on the left so -1 at position 6(left)
            game[i].surrounding_nodes[6] = -1
            # there are no nodes on the left so -1 at position 7(top-left)
            game[i].surrounding_nodes[7] = -1
            # there are no nodes on the left so -1 at position 5(bottom-left)
            game[i].surrounding_nodes[5] = -1
        else:
            # else we are not at the left most column and can assign a left node id
            game[i].surrounding_nodes[6] = game[i - 1].id
            # assign id to position 5(bottom left) but we cannot assign bottom positions to last row as there are no
            # nodes below the last row
            if i < len(game) - length:
                # index i + length - 1 would be the bottom-left node
                game[i].surrounding_nodes[5] = game[i + length - 1].id
        # we assign -1 at position 4(bottom row). We can't do it in the above if statement b/c the above 'if' does not
        # check corner nodes and a lot of corner nodes have bottom nodes
        if i > len(game) - length - 1:
            # assigning -1 at position 4(bottom)
            game[i].surrounding_nodes[4] = -1
            # assigning -1 at position 3(bottom-right)
            game[i].surrounding_nodes[3] = -1
            # assigning -1 at position 5(bottom-left)
            game[i].surrounding_nodes[5] = -1
        else:
            # i + length would be the index of the bottom node
            game[i].surrounding_nodes[4] = game[i + length].id
        # right side
        if i % length == length - 1:
            # assigning -1 to position 2(right)
            game[i].surrounding_nodes[2] = -1
            # assigning -1 to position 1(top-right)
            game[i].surrounding_nodes[1] = -1
            # assigning -1 to position 3(bottom-right)
            game[i].surrounding_nodes[3] = -1
        else:
            # assigning right node id to position 2(right)
            game[i].surrounding_nodes[2] = game[i + 1].id
            if i < len(game) - length - 1:
                game[i].surrounding_nodes[3] = game[i + length + 1].id
    db.session.commit()
    return render_template('start.html', grid=game, game_info=game_info)


# this function is to ensure that the first node chosen isn't a mine, and it sets the value of the selected node to zero
# , so that it can be easier for the players(else only one node might be displayed when selected)
@features.route('/first-node/<int:node_id>', methods=['POST', 'GET'])
def first_node(node_id):
    # retrieve game info
    game_info = GameInfo.query.filter_by(id=1).first()
    # using time module to get start time of the game
    game_info.start_time = t.time()
    # fetch game
    game = Nodes.query.all()
    # first choice is the first node selected
    first_choice = Nodes.query.filter_by(id=node_id).first()
    # can be changed to number of mines depends on difficulty
    mines = round(len(game) * 0.15)
    # this loop assigns mines to nodes and makes sures to assign the correct amount of mines
    while mines != 0:
        node = random.choice(game)
        # we make sure that the first selected node and the surrounding nodes are not a mine
        if first_choice.id != node.id and node.id not in first_choice.surrounding_nodes:
            # we make sure that it doesn't try to place a mine on nodes that already have a mine in it
            # else we will just have a lot less mines on the game
            if node.value != -1:
                # value -1 means it is a mine
                node.value = -1
                # subtract from conditional var to count the number of mines assigned
                mines -= 1
    # this loop will assign a value to every node depending on whether there are any bombs surrounding it
    for i in range(len(game)):
        # nodes with value -1 have a bomb, so that is there value
        if game[i].value != -1:
            # loop through surrounding node's positions
            for position in range(8):
                # the -1 in surrounding node list means there is no node in that position
                if game[i].surrounding_nodes[position] != -1:
                    # get surrounding node by id in node's surrounding list
                    surrounding_node = Nodes.query.filter_by(id=game[i].surrounding_nodes[position]).first()
                    # of surrounding node is a mine, then add 1 to the value of the node
                    if surrounding_node.value == -1:
                        game[i].value = 1 + game[i].value
    db.session.commit()
    # call recursive function to display the according nodes
    check_nodes_recursive(first_choice)
    # check game win status
    check_game_status(first_choice, game_info)
    return redirect(url_for('features.refresh_game'))


# this function is to check the values of the surrounding nodes and activate the corresponding ones
def check_nodes_recursive(node):
    # if the node's value is 0, then we try to call the function again with the values in the node's surrounding nodes
    # if a value 0 then it all the nodes around it need to be activated
    if node.value == 0:
        # set current node to active, so it can't go through function again
        node.status = 1
        # commit here to save the changed for when the function gets called again
        db.session.commit()
        # loop the current node's surrounding nodes
        for surrounding_node_id in node.surrounding_nodes:
            # if node_id is -1 then this is a corner node and there is no node at the surrounding position
            # we don't call those because the query will return a none type
            if surrounding_node_id != -1:
                surrounding_node = Nodes.query.filter_by(id=surrounding_node_id).first()
                # this if statement makes sure we do not get stuck in an infinite loop
                # we make sure to not call the recursive function on surrounding nodes that are already active or else
                # it will go infinite between two nodes
                if surrounding_node.value == 0 and surrounding_node.status == 0:
                    # this is set up to go through all nodes with value 0 first and then set the surrounding
                    # nodes to active
                    check_nodes_recursive(surrounding_node)
                surrounding_node.status = 1
                db.session.commit()
    else:
        # this is to just avoid the recursive and activate nodes that do not have a value of 0
        # in most cases if the value is not zero then the one node is only displayed
        node.status = 1
        db.session.commit()


# this function is to flag nodes that the player think is a mine
@features.route('/flag-node/<int:node_id>', methods=['POST', 'GET'])
def flag_node(node_id):
    game_info = GameInfo.query.filter_by(id=1).first()
    # get the current time
    current_time = t.time()
    # update the game time by subtracting it from the current time to get the seconds passed since the start time
    game_info.updated_time = round(current_time - game_info.start_time)
    node = Nodes.query.filter_by(id=node_id).first()
    # if a node is already flagged, then set it to inactive
    if node.status == 3:
        node.status = 0
    elif game_info.game_over == 0:
        # else flag the node
        node.status = 3
    db.session.commit()
    return redirect(url_for('features.refresh_game'))


# this function is to check the value of the player's selected node
@features.route('/check-node-value/<int:node_id>', methods=['POST', 'GET'])
def check_node_value(node_id):
    # get selected node by id
    node = Nodes.query.filter_by(id=node_id).first()
    # fetch current game info
    game_info = GameInfo.query.filter_by(id=1).first()
    # get current time
    current_time = t.time()
    # update the time by subtracting it from the current time to get the seconds passed since the start time
    game_info.updated_time = round(current_time - game_info.start_time)
    db.session.commit()
    # if current node value -1 then player lost the game
    if node.value == -1:
        # fetch all mines
        mines = Nodes.query.filter_by(value=-1).all()
        # set game to lost
        game_info.game_over = -1
        # activate all mines
        for mine in mines:
            mine.status = 2
        db.session.commit()
    # if node status is 1 then the player is trying to check if they have the right surrounding nodes flagged
    elif node.status == 1:
        # list to keep track of how many flags were wrongly flagged
        wrongly_flagged_nodes = []
        # count the number of flagged nodes
        flagged_nodes = 0
        # count number of mines
        mines = 0
        # loop through surrounding nodes
        for surrounding_node_id in node.surrounding_nodes:
            # node ids that are negative means there are no nodes at that position
            if surrounding_node_id != -1:
                # get surrounding node by id
                surrounding_node = Nodes.query.filter_by(id=surrounding_node_id).first()
                # if value is not -1, but it was flagged then it was wrongly flagged
                if surrounding_node.value != -1 and surrounding_node.status == 3:
                    # status 4 means it is a wrongly flagged node and player get penalty
                    surrounding_node.status = 4
                    # the penalty is 10 seconds added to score
                    # we subtract 10 from the start time to add time to the game(time module stuff)
                    game_info.start_time -= 10
                    # update current time to include penalty time
                    game_info.updated_time = round(current_time - game_info.start_time)
                    wrongly_flagged_nodes.append(node.id)
                    # flash message to player
                    flash('Wrongly flagged nodes!!! +10 seconds to score.', category="error")
                # this if is to set the wrongly flagged nodes to just 'active'
                # this is here so the user doesn't have to click each wrongly flagged node individually and can just
                # select the base node to set them to 'active' all at once
                elif surrounding_node.status == 4:
                    surrounding_node.status = 1
                    wrongly_flagged_nodes.append(node.id)
                    # if a wrongly guessed node was zero and was activated then we run the recursive function to show
                    # the rest of the nodes around
                    if surrounding_node.value == 0:
                        check_nodes_recursive(surrounding_node)
                # count the total number of flagged nodes
                if surrounding_node.status == 3:
                    flagged_nodes += 1
                # count the number of mines
                if surrounding_node.value == -1:
                    mines += 1
        # if there are no wrongly flagged nodes and all the mines were flagged, then the player can click the base node
        # to activate the surrounding nodes that are not mines
        # if flagged nodes == mines and no nodes were wrongly tagged then we can activate the surrounding nodes that are
        # not mines because the player guessed where the mines were
        if len(wrongly_flagged_nodes) == 0 and flagged_nodes == mines:
            # loop through surrounding nodes
            for surrounding_node_id in node.surrounding_nodes:
                # -1 node id means there is no node at that position(corner node)
                if surrounding_node_id != -1:
                    # fetch node by id
                    surrounding_node = Nodes.query.filter_by(id=surrounding_node_id).first()
                    # if node status is 0 and node is not a mine then we can activate all the inactive nodes
                    if surrounding_node.value != -1 and surrounding_node.status == 0:
                        # if on of those inactive nodes were zero then we check the surrounding nodes
                        if surrounding_node.value == 0:
                            check_nodes_recursive(surrounding_node)
                        surrounding_node.status = 1
        db.session.commit()
        # Games can be won when the base is clicked and the surrounding nodes that were activated were the remaining
        # nodes, so we check if all the remaining nodes are only mines
        check_game_status(node, game_info)
    # else a player clicked an inactive node, and we have to call the recursive function to check the surrounding nodes
    else:
        # check surrounding nodes
        check_nodes_recursive(node)
        # check if game was won
        check_game_status(node, game_info)
    return redirect(url_for('features.refresh_game'))


# this function is called to refresh the game(mostly used as a redirect
@features.route('/refresh-game', methods=['POST', 'GET'])
def refresh_game():
    # fetch all the relevant items of the game
    game = Nodes.query.all()
    flagged_nodes = len(Nodes.query.filter_by(status=3).all())
    game_info = GameInfo.query.filter_by(id=1).first()
    db.session.commit()
    return render_template('start.html', game=game, game_info=game_info, flagged_nodes=flagged_nodes)


# when a player wins a game, they can submit their name and scores
@features.route('/submit-score', methods=['POST', 'GET'])
def submit_score():
    # get name from form
    name = request.form.get('name')
    # get user's score when the last node was clicked
    game_info = GameInfo.query.filter_by(id=1).first()
    # calculate the nodes
    mines = round(game_info.length * game_info.length * 0.15)
    # set the difficulty based on the length of game_info
    if game_info.length == 10:
        difficulty = 'Beginner'
    elif game_info.length == 15:
        difficulty = 'Medium'
    elif game_info.length == 25:
        difficulty = 'Hard'
    else:
        difficulty = 'Test Game'
    # create game with the info
    game = Game(name=name, score=game_info.updated_time, mines=mines, difficulty=difficulty)
    db.session.add(game)
    db.session.commit()
    # redirect to start
    return redirect(url_for('features.start'))


# This function is to check if the user has won the game. There are a couple of different instances where the player can
# win, so it is good to split it in this function to check if the player won in those instances
def check_game_status(node, game_info):
    # conditional var
    game_won = 1
    # games can be won after clicking a node, so we check that here
    # fetch remaining nodes and see if they are all mines
    remaining_nodes = Nodes.query.filter(Nodes.status != 1).all()
    for remaining_node in remaining_nodes:
        if remaining_node.value != -1:
            game_won = 0
    # if test is passed then player won
    if game_won == 1 and node.value != -1:
        game_info.game_over = 1
        # we do not have to do this part for test games(length == 5) because those always get added tp the leader
        # board. The 5 most recent test games are always on the leaderboard.
        if game_info.length != 5:
            # calculate the mines to get the list of game difficulty that matches the current game
            mines = round(game_info.length * game_info.length * 0.15)
            corresponding_games = db.session.query(Game).filter_by(mines=mines).order_by(desc(Game.score)).all()
            # if our score is higher than the lowest score on the leaderboard then our score gets added to the
            # board
            # make sure games exist
            if len(corresponding_games) != 0:
                if corresponding_games[0].score > game_info.updated_time:
                    game_info.leaderboard = 1
            else:
                game_info.leaderboard = 1
        # else we show the score box for test games to be added on the leaderboard
        else:
            game_info.leaderboard = 1
        db.session.commit()