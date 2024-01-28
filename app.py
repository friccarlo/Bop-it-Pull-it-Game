from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

SCORE_FILE = "scores.txt"

def read_scores():
    if not os.path.exists(SCORE_FILE):
        open(SCORE_FILE, 'a').close()

    scores = []
    with open(SCORE_FILE, "r") as file:
        for line in file:
            parts = line.strip().split(": ")
            if len(parts) == 2:
                username, score = parts
                scores.append((username, int(score)))
    scores.sort(key=lambda x: x[1], reverse=True)  # Sort scores in descending order
    return scores

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_score', methods=['POST'])
def submit_score():
    try:
        data = request.json
        username = data['username']
        score = data['score']

        with open(SCORE_FILE, "a") as file:
            file.write(f"{username}: {score}\n")

        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/get_high_score')
def get_high_score():
    scores = read_scores()
    if scores:
        high_score_entry = max(scores, key=lambda x: x[1])
        return jsonify(player=high_score_entry[0], highScore=high_score_entry[1])
    return jsonify(player="No scores yet", highScore=0)

@app.route('/get_all_scores')
def get_all_scores():
    scores = read_scores()
    return jsonify(scores=scores)

if __name__ == '__main__':
    app.run(debug=True)
