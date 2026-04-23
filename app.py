from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO
import time, os

app = Flask(__name__)
app.secret_key = "secret123"

socketio = SocketIO(app, cors_allowed_origins="*")

teams = {}
registered = []
buzz_order = []
buzzer_enabled = False


# ---------------- ROUTES ---------------- #

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/join')
def join():
    return render_template('join.html')


@app.route('/buzzer')
def buzzer():
    return render_template('buzzer.html', team=request.args.get('team'))


@app.route('/admin-login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('username') == "ADMIN" and request.form.get('password') == "admin123":
            session['admin'] = True
            return redirect('/admin')
    return render_template('admin_login.html')


@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect('/admin-login')
    return render_template('admin.html')


@app.route('/board')
def board():
    return render_template('board.html')


# ---------------- CORE LOGIC ---------------- #

def get_result():
    sorted_data = sorted(buzz_order, key=lambda x: x["time"])
    return [{"team": t["team"], "rank": i+1} for i, t in enumerate(sorted_data)]


# ---------------- SOCKET ---------------- #

@socketio.on('connect')
def connect():
    print("Connected:", request.sid)
    socketio.emit('team_list', registered)
    socketio.emit('buzzer_state', buzzer_enabled)
    socketio.emit('update', get_result())


@socketio.on('request_update')
def request_update():
    socketio.emit('update', get_result(), to=request.sid)


@socketio.on('disconnect')
def disconnect():
    print("Disconnected:", request.sid)

    if request.sid in teams:
        team = teams.pop(request.sid)
        if team in registered:
            registered.remove(team)

    socketio.emit('team_list', registered)


@socketio.on('register')
def register(data):
    team = data.get('team')
    if not team:
        return

    teams[request.sid] = team

    if team not in registered:
        registered.append(team)

    socketio.emit('team_list', registered)
    socketio.emit('buzzer_state', buzzer_enabled)


@socketio.on('toggle')
def toggle():
    global buzzer_enabled
    buzzer_enabled = not buzzer_enabled
    socketio.emit('buzzer_state', buzzer_enabled)


@socketio.on('buzz')
def buzz():
    global buzz_order

    if not buzzer_enabled:
        return

    team = teams.get(request.sid)
    if not team:
        return

    if any(t['team'] == team for t in buzz_order):
        return

    buzz_order.append({
        "team": team,
        "time": time.time()
    })

    socketio.emit('update', get_result())


@socketio.on('reset')
def reset():
    global buzz_order
    buzz_order = []
    socketio.emit('update', [])


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, allow_unsafe_werkzeug=True)
