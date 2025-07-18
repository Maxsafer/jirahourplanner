# app.py
from flask import Flask, render_template, request, redirect, url_for
from datetime import date, timedelta
import os, json
from send_to_jira import send_to_jira

app = Flask(__name__)
DATA_DIR = os.path.join(app.root_path, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def week_dates(start: date):
    return [start + timedelta(days=i) for i in range(7)]

def load_activities(dt: date):
    fname = dt.strftime('%Y%m%d') + '.json'
    path = os.path.join(DATA_DIR, fname)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []

def save_activities(dt: date, activities):
    fname = dt.strftime('%Y%m%d') + '.json'
    path = os.path.join(DATA_DIR, fname)
    with open(path, 'w') as f:
        json.dump(activities, f, indent=2)

def write_url(url):
    clean = url.strip().rstrip('/')
    fname = 'user.env'
    path = os.path.join(DATA_DIR, fname)
    with open(path, 'w') as f:
        # f.write(f"jira_url={clean}/browse/")
        f.write(f"jira_url={clean}")

def load_variable(key):
    """
    Reads DATA_DIR/user.env and returns the value for `key`.
    Returns None if the file or the key is not found.
    """
    fname = 'user.env'
    path = os.path.join(DATA_DIR, fname)
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                # skip empty lines or comments
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k, v = line.split('=', 1)
                if k == key:
                    return v
    except FileNotFoundError:
        return None
    return None

@app.route('/', methods=['GET'])
def index():
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    week = week_dates(monday)
    week_data = {d: load_activities(d) for d in week}
    jira_url = load_variable("jira_url") or "https://your-jira-instance.atlassian.net"
    return render_template('index.html', jira_url=jira_url, week=week, week_data=week_data)

@app.route('/add', methods=['POST'])
def add():
    dt = date.fromisoformat(request.form['date'])
    activities = load_activities(dt)
    activities.append({
        'id': request.form['act_id'],
        'description': request.form['desc'],
        'hours': float(request.form['hours'])
    })
    save_activities(dt, activities)
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    dt = date.fromisoformat(request.form['date'])
    idx = int(request.form['index'])
    activities = load_activities(dt)
    if 0 <= idx < len(activities):
        activities.pop(idx)
        save_activities(dt, activities)
    return redirect(url_for('index'))

@app.route('/edit', methods=['POST'])
def edit():
    dt = date.fromisoformat(request.form['date'])
    idx = int(request.form['index'])
    desc  = request.form.get('desc', '').strip()
    hours = float(request.form.get('hours', 0))
    activities = load_activities(dt)
    if 0 <= idx < len(activities):
        activities[idx]["description"] = desc
        activities[idx]["hours"] = hours
        save_activities(dt, activities)
    return redirect(url_for('index'))

@app.route('/uploadhours', methods=['POST'])
def uploadhours():
    dt = date.fromisoformat(request.form['date'])
    activities = load_activities(dt)
    logs = send_to_jira(activities, load_variable("jira_url"), load_variable("email"), load_variable("api_token"))

    today     = date.today()
    monday    = today - timedelta(days=today.weekday())
    week      = week_dates(monday)
    week_data = {d: load_activities(d) for d in week}
    jira_url  = load_variable("jira_url") or "https://your-jira-instance.atlassian.net"

    return render_template('index.html', week=week, week_data=week_data, jira_url=jira_url, logs=logs)

@app.route('/save_url', methods=['POST'])
def save_url():
    url = request.form['jiraUrl']
    write_url(url)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
