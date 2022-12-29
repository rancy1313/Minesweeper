from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory
from flask_login import login_required, current_user
from .models import Nodes
from . import db
import random

features = Blueprint('features', __name__)


@features.route('/', methods=['GET'])
def start():
    return render_template('start.html')


@features.route('/set-game-grid', methods=['POST', 'GET'])
def set_game_grid():
    Nodes.query.delete()
    db.session.commit()
    length = 6
    width = 6
    game = []
    for i in range(length * width):
        node = Nodes()
        db.session.add(node)
        game.append(node)
    db.session.commit()
    # [top(0), top-right(1), right(2), bottom-right(3), bottom(4), bottom-left(5), left(6), top-left(7)]
    for i in range(length * width):
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
    return render_template('start.html', grid=game)


@features.route('/first-node/<int:node_id>', methods=['POST', 'GET'])
def first_node(node_id):
    game = Nodes.query.all()
    # first choice is the first node selected
    first_choice = Nodes.query.filter_by(id=node_id).first()
    # first_choice.status = 1
    # 1/5 of the nodes have mines
    mines = round(len(game) * 0.2)
    while mines != 0:
        node = random.choice(game)
        # we make sure that the first selected node and the surrounding nodes are not a mine
        if first_choice.id != node.id and node.id not in first_choice.surrounding_nodes:
            # we make sure that it doesn't try to place a mine on nodes that already have a mine in it
            # else we will just have a lot less mines on the game
            if node.value != -1:
                node.value = -1
                mines -= 1
    # this loop will assign a value to every node depending on whether there are any bombs surrounding it
    for i in range(len(game)):
        # nodes with value -1 have a bomb, so that is there value
        if game[i].value != -1:
            # game[i].value = 0
            for position in range(8):
                if game[i].surrounding_nodes[position] != -1:
                    node = Nodes.query.filter_by(id=game[i].surrounding_nodes[position]).first()
                    if node.value == -1:
                        game[i].value = 1 + game[i].value

    db.session.commit()
    check_nodes_recursive(first_choice)
    return render_template('start.html', game=game)


'''@features.route('/start_game', methods=['POST', 'GET'])
def start_game():
    Nodes.query.delete()
    db.session.commit()
    length = 10
    width = 10
    mines = round(length * width * .2)
    game = []
    for i in range(length * width):
        node = Nodes()
        db.session.add(node)
        game.append(node)
    db.session.commit()
    while mines != 0:
        node = random.choice(game)
        if node.value != -1:
            node.value = -1
            mines -= 1

    # [top(0), top-right(1), right(2), bottom-right(3), bottom(4), bottom-left(5), left(6), top-left(7)]
    for i in range(length * width):
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
    for i in range(length * width):
        if game[i].value != -1:
            game[i].value = 0
            for position in range(8):
                if game[i].surrounding_nodes[position] != -1:
                    node = Nodes.query.filter_by(id=game[i].surrounding_nodes[position]).first()
                    if node.value == -1:
                        game[i].value = 1 + game[i].value

    db.session.commit()
    return render_template('start.html', game=game)'''


@features.route('/check-value/<int:node_id>', methods=['POST'])
def check_value(node_id):
    print("check val: ", node_id)
    node = Nodes.query.filter_by(id=node_id).first()
    game = Nodes.query.all()
    db.session.commit()
    game_won = 1
    if node.value == -1:
        print('game over')
        mines = Nodes.query.filter_by(value=-1).all()
        for mine in mines:
            mine.status = 2
        db.session.commit()
    else:
        print('value: ', node.value)
        check_nodes_recursive(node)
        remaining_nodes = Nodes.query.filter_by(status=0).all()
        for remaining_node in remaining_nodes:
            if remaining_node.value == 1:
                game_won = 0
        if game_won == 1 and node.value != -1:
            print('game won!!!')
    return render_template('start.html', game=game)


def check_nodes_recursive(node):
    if node.value == 0:
        node.status = 1
        db.session.commit()
        for surrounding_node_id in node.surrounding_nodes:
            if surrounding_node_id != -1:
                surrounding_node = Nodes.query.filter_by(id=surrounding_node_id).first()
                if surrounding_node.value == 0 and surrounding_node.status == 0:
                    check_nodes_recursive(surrounding_node)
                surrounding_node.status = 1
                db.session.commit()
    else:
        node.status = 1
        db.session.commit()


@features.route('/flag_node/<int:node_id>', methods=['POST', 'GET'])
def flag_bomb(node_id):
    print('in flag bomb func')
    game = Nodes.query.all()
    node = Nodes.query.filter_by(id=node_id).first()
    if node.status == 3:
        node.status = 0
    else:
        node.status = 3
    db.session.commit()
    return render_template('start.html', game=game)
