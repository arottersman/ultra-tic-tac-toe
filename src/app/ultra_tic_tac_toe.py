import os
import json
import math

from flask import (Flask,
                   request,
                   jsonify,
                   )
import redis

app = Flask(__name__)

# Constants
BOARD_KEY_NAME = 'BOARD_KEY_NAME'
BOARD_SIZE = 3

# Routes
@app.route('/')
def serve_static():
    return app.send_static_file('index.html')


@app.route('/game', methods=['POST'])
def handle_start_game():
    r = connect_redis()
    r.incr(BOARD_KEY_NAME)
    # TODO something is wrong with the key
    game_id = 1 # r.get(BOARD_KEY_NAME)
    board = build_board()
    game = {'id': game_id,
            'board': board,
            'winner': '',
            'turn': 'X',
            'valid_subgames': [x for x in range(9)]}
    r.set(game_id, game)
    return jsonify(game)


@app.route('/game', methods=['GET'])
def handle_get_game():
    body = request.get_json()
    id = body.id if body and body.id else None
    if not id:
        # Set response status code to 400
        return jsonify({'Error': 'Must provide game id'})
    r = connect_redis()
    game = r.get(id)
    if game:
        return jsonify(game)
    else:
        return jsonify({'Error': 'Invalid id'})


@app.route('/move', methods=['POST'])
def handle_make_move():
    # body = request.get_json(force=True)
    body = { 'subgame': 1,
             'cell': 1,
             'id': 1}
    if not body:
        return jsonify({'Error': 'Must provide move'})
    return make_move(body['id'], body['subgame'], body['cell'])


# Helpers
def connect_redis():
    return redis.StrictRedis(host=os.getenv("REDIS_URL"),
                             port=os.getenv("REDIS_PORT"),
                             db=0)

def build_board():
    return [[''] * 9] * 9


def is_valid_move(board, subgame, cell):
    return True


def has_winner(board):
    return ''


def make_move(id, subgame, cell):
    if not id or not subgame or not cell:
        raise Exception('Invalid input')
    r = connect_redis()
    current_game = json.loads(r.get(id))
    if not current_game:
        raise Exception('No game for id')

    if is_valid_move(current_game['board'], subgame, cell):
        i = math.floor(subgame / BOARD_SIZE) + math.floor(cell / BOARD_SIZE)
        j = (subgame % BOARD_SIZE) + (cell % BOARD_SIZE)
        current_game['board'][i][j] = current_game['turn']
        current_game['winner'] = has_winner(current_game['board'])
        current_game['valid_subgames'] = [cell]
        current_game['turn'] = 'X' if current_game['turn'] == 'O' else 'O'
        r.set(id, current_game)
        return jsonify(current_game)


