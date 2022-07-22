from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TV_INTERCEPT_REDIRECTS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
debug = DebugToolbarExtension(app)

# initialize boggle game
boggle_game = Boggle()

# routes
@app.route("/")
def home():
    """Homepage will show board"""
    
    # create the board and store it in flask session
    game_board = boggle_game.make_board()
    session['board'] = game_board

    return render_template("index.html", board=game_board)


@app.route("/check-word")
def word_check():
    word = request.args["word"]
    board = session["board"]
    res = boggle_game.check_valid_word(board, word)

    return jsonify({'result': res})


@app.route("/post-score", methods=["POST"])
def post_score():
    score = request.json["score"]
    high_score = session.get("high_score", 0)
    number_of_plays = session.get("number_plays", 0)

    session["number_plays"] = number_of_plays + 1
    session["high_score"] = max(score, high_score)

    return jsonify(brokeRecord=score>high_score)



