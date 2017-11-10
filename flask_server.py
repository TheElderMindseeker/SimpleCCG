from flask import Flask, request
from game_engine import play
from set_reader import import_card_set_from_file


app = Flask(__name__)


@app.route('/', methods=('GET',))
@app.route('/fight', methods=('GET',))
def fight():
    angel_deck = request.args.get('angel_deck', '')
    demon_deck = request.args.get('demon_deck', '')
    if len(angel_deck) == 0 or len(demon_deck) == 0:
        return "Provide angel_deck and demon_deck parameters in your GET request"

    angel_deck = tuple(map(int, angel_deck.split(',')))
    demon_deck = tuple(map(int, demon_deck.split(',')))

    card_set = import_card_set_from_file("test_set.scg")

    angel = 0
    demon = 0
    tests = 10000
    for i in range(tests):
        result = tuple(play(card_set, (angel_deck, demon_deck)))
        angel += result[0]
        demon += result[1]

    response = "<p>Angel winrate: " + str(100 * angel / tests) + "%</p>"
    response += "<p>Demon winrate: " + str(100 * demon / tests) + "%</p>"
    response += "<p>Draw rate: " + str(100 * (1 - (angel + demon) / tests)) + "%</p>"
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)