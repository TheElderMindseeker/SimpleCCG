from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from game_engine import Game
from set_reader import import_card_set_from_file


class Config(object):
    DEBUG = True
    CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


class DeckForm(FlaskForm):
    angel_deck = StringField(label="Angel Deck")
    demon_deck = StringField(label="Demon Deck")


app = Flask(__name__)
app.config.from_object('flask_server.Config')


@app.route('/', methods=('GET', 'POST'))
@app.route('/fight', methods=('GET', 'POST'))
def fight():
    form = DeckForm()

    if form.validate_on_submit():
        angel_deck = tuple(map(int, form.angel_deck.data.replace(' ', '').split(',')))
        demon_deck = tuple(map(int, form.demon_deck.data.replace(' ', '').split(',')))

        card_set = import_card_set_from_file("test_set.scg")
        game = Game(card_set, (angel_deck, demon_deck))

        angel = 0
        demon = 0
        tests = 100
        for i in range(tests):
            result = tuple(game.play())
            angel += result[0]
            demon += result[1]

        response = "<p>Angel winrate: " + str(100 * angel / tests) + "%</p>"
        response += "<p>Demon winrate: " + str(100 * demon / tests) + "%</p>"
        response += "<p>Draw rate: " + str(100 * (1 - (angel + demon) / tests)) + "%</p>"
        return response

    return render_template("fight.html", form=form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)