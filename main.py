import os
import random

from flask import (
    Flask,
    session,
    render_template,
    redirect,
    url_for,
    request

)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'vavavava'


@app.route('/', methods=['GET', 'POST'])
def index():
    session.clear()
    return render_template("Hangman.html", score=0)


@app.route('/guess_input', methods=['GET', 'POST'])
def guess_input():
    return render_template("guess_input.html", score=0)


@app.route('/game', methods=['GET', 'POST'])
def game():
    session['answer'] = request.form['answer']
    session['s'] = '_'*len(session['answer'])
    session['puzzle'] = list(session['s'])
    session['score'] = 0
    session['h'] = []  # history of guesses as a list
    session['question'] = ""
    if request.method == 'POST':
        return render_template("Game.html",
                               answer=session['answer'],
                               puzzle=session['puzzle'],
                               puzzle_st=session['s'],
                               score=0,
                               question=session['question']
                               )
    else:
        return redirect(url_for('index'))


@app.route('/guess_random', methods=['GET', 'POST'])
def guess_random():
    words = [line.rstrip().lower() for line in open("words.txt")]
    word = random.choice(words)
    session['answer'] = word
    session['s'] = '_'*len(word)
    session['puzzle'] = list('_'*len(word))
    session['score'] = 0
    session['h'] = []  # history of guesses as a list
    session['question'] = ""
    return render_template("Game.html",
                           answer=session['answer'],
                           puzzle=session['puzzle'],
                           puzzle_st=session['s'],
                           score=0,
                           question=session['question']
                           )


@app.route('/guess_riddle', methods=['GET', 'POST'])
def guess_riddle():
    return render_template("guess_riddle.html", score=0)


@app.route('/riddle_game', methods=['GET', 'POST'])
def riddle_game():
    ctg = request.form['category']
    dct = {}
    f = open("riddles.txt", "r")
    for line in f:
        if line.strip() == '*' + ctg + '*':  # start reading file
            break
    for line in f:
        if "*" not in line and len(line) > 3:  # populate dict with riddles
            (key, val) = line.split("?")
            dct[key+"?"] = val[1:-1]
        else:
            break   # ends reading file
    f.close()
    riddle = random.choice(list(dct.keys()))  # select random riddle
    session['answer'] = dct[riddle]
    session['s'] = '_'*len(session['answer'])
    session['puzzle'] = list(session['s'])
    session['score'] = 0
    session['h'] = []  # history of guesses as a list
    session['question'] = riddle[:-1] + ". Kas?"
    if request.method == 'POST':
        return render_template("Game.html",
                               answer=session['answer'],
                               puzzle=session['puzzle'],
                               puzzle_st=session['s'],
                               score=0,
                               question=session['question']
                               )


@app.route('/guess', methods=['GET', 'POST'])
def guess():
    results = {}
    answer = session['answer']
    session['guess'] = request.form['guess']
    g = session['guess']
    results = check_guesses(answer,
                            g,
                            session['score'],
                            session['puzzle'],
                            session['s'],
                            session['h']
                            )
    session['score'] = results["c"]
    session['s'] = results["s"]
    session['puzzle'] = results["p"]
    session['h'] = results["h"]

    # DEBUG
    # print("answer",answer)
    # print("guess",g)
    # print("puzzle", session['puzzle'])
    # print("s", session['s'])
    # print("h",session['h'])
    # print("score",session['score'])

    if request.method == 'POST':
        return render_template("Game.html",
                               guess=g,
                               answer=answer,
                               puzzle=session['puzzle'],
                               history=session['h'],
                               score=session['score'],
                               puzzle_st=session['s'],
                               question=session['question'])
    else:
        return redirect(url_for('index'))

# functions for guessing algorithm


def word_to_list(w):  # "wheel" ---> "[w, h, e, e, l]"
    p = []
    for i in range(0, len(w)):
        p.append(w[i])
    return p


def puzzle_to_string(p):  # "[w, "_", "_", e, l]" --> "w _ _ e l"
    s = ""
    for i in range(0, len(p)):
        s += p[i]
    return s


def check_guesses(answer, g, c, p, s, h):
    if g not in h:
        h.append(g)
        if g in answer:
            f = answer.find(g)
            while f >= 0:
                p[f] = g.upper()
                f = answer.find(g, f + 1)
            s = puzzle_to_string(p)
        else:
            c += 1
    if c - 6 == 0 or s == answer:
        p = word_to_list(answer.upper())
    return {"p": p, "h": h, "c": c, "s": s.lower()}


port = int(os.environ.get('PORT', 5000))

app.run(host='0.0.0.0', port=port)
