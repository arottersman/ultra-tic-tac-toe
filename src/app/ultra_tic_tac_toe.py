from flask import Flask
app = Flask(__name__)

@app.route('/game', methods=['POST'])
def start_game():
    return 'TODO start game'

@app.route('/move', methods=['POST'])
def make_move():
    return 'TODO make move'
