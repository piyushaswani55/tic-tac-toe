from flask import Flask, render_template, session, request, redirect, url_for
from flask.helpers import url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def init(size):
    session["size"] = size
    session["board"] = [[None for i in range(
        session["size"])] for j in range(session["size"])]
    session["turn"] = "X"
    session["turns"] = 0
    session["message"] = "Enter size of the board" if size == 0 else f"{session['turn']}'s Turn"


def checkWinner():
    board = session["board"]
    size = session["size"]
    for i in range(size):
        won = True
        temp = board[i][0]
        if not temp:
            continue
        for j in range(1, size):
            if board[i][j] == temp:
                continue
            else:
                won = False
                break
        if won:
            return won

    for i in range(size):
        won = True
        temp = board[0][i]
        if not temp:
            continue
        for j in range(1, size):
            if board[j][i] == temp:
                continue
            else:
                won = False
                break
        if won:
            return won

    won = True
    temp = board[0][0]
    for (i, j) in zip(range(1, size), range(1, size)):
        if board[i][j] == temp:
            continue
        else:
            won = False
            break
    if won:
        return won

    won = True
    temp = board[0][size-1]
    for i, j in zip(range(1, size), range(size-2, -1, -1)):
        if board[i][j] == temp:
            continue
        else:
            won = False
            break
    if won:
        return won
    return False


def playTurn():
    board = session["board"]
    row = int(request.args.get("row"))
    col = int(request.args.get("col"))
    board[row][col] = session["turn"]
    session["board"] = board
    session["turns"] += 1
    if session["turns"] >= session["size"]*2 - 1:
        if checkWinner():
            session["message"] = f"{session['turn']} wins"
            return
        elif session["turns"] >= session["size"] * session["size"]:
            session["message"] = "Game Draw"
            return
    session["turn"] = "O" if session["turn"] == "X" else "X"
    session["message"] = f"{session['turn']}'s Turn"


@ app.route("/", methods=["GET", "POST"])
def index():
    if "board" not in session or not session["board"]:
        size = int(request.form.get('size')) if request.form.get(
            'size') is not None else 0
        if size % 2 == 0 or size < 3 or size > 11:
            size = 0
        init(size)
    return render_template("index.html", board=session["board"], turn=session["turn"], message=session["message"], size=session["size"])


@ app.route("/play")
def play():
    playTurn()
    return redirect(url_for("index"))


@ app.route("/reset")
def reset():
    init(0)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
