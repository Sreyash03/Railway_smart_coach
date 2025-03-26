from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('rail_info.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            coach_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            comments TEXT NOT NULL       
        )
    ''')
    conn.commit()
    conn.close()

# Route to render the coach_info page
@app.route('/')
def coach_info():
    return render_template('coach_info.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    coach_id = request.form['coach_id']
    name = request.form['name']
    comments = request.form['comments']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Corrected the date format

    # Insert data into the database
    conn = sqlite3.connect('rail_info.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (coach_id, name, timestamp, comments) VALUES (?, ?, ?, ?)', 
                   (coach_id, name, timestamp, comments))
    conn.commit()
    conn.close()

    # Notify all clients about the new user
    socketio.emit('new_user', {'coach_id': coach_id, 'name': name, 'timestamp': timestamp, 'comments': comments})
    
    return redirect(url_for('coach_info'))

# Route to display user information with sorting
@app.route('/users')
def users():
    sort_order = request.args.get('sort', 'asc')  # Get the sort order from the query parameter, default to 'asc'
    conn = sqlite3.connect('rail_info.db')
    cursor = conn.cursor()
    
    if sort_order == 'desc':
        cursor.execute('SELECT * FROM users ORDER BY timestamp DESC')
    else:
        cursor.execute('SELECT * FROM users ORDER BY timestamp ASC')
        
    users = cursor.fetchall()
    conn.close()
    
    return render_template('users.html', users=users, sort_order=sort_order)

# Route to delete a user
@app.route('/delete/<string:coach_id>', methods=['POST'])
def delete_user(coach_id):
    conn = sqlite3.connect('rail_info.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE coach_id = ?', (coach_id,))
    conn.commit()
    conn.close()

    # Notify all clients about the user deletion
    socketio.emit('delete_user', {'coach_id': coach_id})
    
    return redirect(url_for('users'))

# WebSocket event to handle custom messages
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    emit('response', {'data': 'Message received!'})

if __name__ == '__main__':
    init_db()
    socketio.run(app, host='127.0.0.1', port=8000, debug=True)  # Run on port 8000
