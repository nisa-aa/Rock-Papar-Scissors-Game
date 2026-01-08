import os
import random
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'stats.db')

app = Flask(__name__)


def get_db_connection():
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	return conn


def init_db():
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute(
		"""
		CREATE TABLE IF NOT EXISTS stats (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			result TEXT NOT NULL,
			player_move TEXT NOT NULL,
			computer_move TEXT NOT NULL,
			played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
		"""
	)
	conn.commit()
	conn.close()


# Initialize the database when running the app directly or inside an app context.
# Avoid using the deprecated `before_first_request` hook on newer Flask versions.


def determine_result(player, computer):
	if player == computer:
		return 'draw'
	wins = {
		'rock': 'scissors',
		'paper': 'rock',
		'scissors': 'paper',
	}
	return 'win' if wins[player] == computer else 'loss'


@app.route('/')
def index():
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute(
		"""
		SELECT
			COUNT(*) as total,
			SUM(CASE WHEN result = 'win' THEN 1 ELSE 0 END) as wins,
			SUM(CASE WHEN result = 'loss' THEN 1 ELSE 0 END) as losses
		FROM stats
		"""
	)
	row = cur.fetchone()
	conn.close()

	total = row['total'] or 0
	wins = row['wins'] or 0
	losses = row['losses'] or 0

	return render_template('index.html', total=total, wins=wins, losses=losses, last=None)


@app.route('/play', methods=['POST'])
def play():
	player_move = request.form.get('move')
	if player_move not in ('rock', 'paper', 'scissors'):
		return redirect(url_for('index'))

	computer_move = random.choice(['rock', 'paper', 'scissors'])
	result = determine_result(player_move, computer_move)

	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute(
		'INSERT INTO stats (result, player_move, computer_move) VALUES (?, ?, ?)',
		(result, player_move, computer_move),
	)
	conn.commit()
	conn.close()

	# Recalculate aggregates
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute(
		"""
		SELECT
			COUNT(*) as total,
			SUM(CASE WHEN result = 'win' THEN 1 ELSE 0 END) as wins,
			SUM(CASE WHEN result = 'loss' THEN 1 ELSE 0 END) as losses
		FROM stats
		"""
	)
	row = cur.fetchone()
	conn.close()

	total = row['total'] or 0
	wins = row['wins'] or 0
	losses = row['losses'] or 0

	last = {'player': player_move, 'computer': computer_move, 'result': result}

	# Create a descriptive story message based on the interaction
	if result == 'draw':
		story_message = f"It is a standoff! Both chose {player_move.capitalize()}."
	else:
		if (player_move == 'rock' and computer_move == 'scissors') or (player_move == 'scissors' and computer_move == 'rock'):
			story_message = 'Rock crushes Scissors!'
		elif (player_move == 'scissors' and computer_move == 'paper') or (player_move == 'paper' and computer_move == 'scissors'):
			story_message = 'Scissors cuts Paper!'
		elif (player_move == 'paper' and computer_move == 'rock') or (player_move == 'rock' and computer_move == 'paper'):
			story_message = 'Paper covers Rock!'
		else:
			story_message = ''

	return render_template('index.html', total=total, wins=wins, losses=losses, last=last, story_message=story_message)


@app.route('/reset')
def reset():
	"""Clear all records from the stats table and redirect to home."""
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute('DELETE FROM stats')
	conn.commit()
	conn.close()
	return redirect(url_for('index'))


if __name__ == '__main__':
	with app.app_context():
		init_db()
	app.run(debug=True)

