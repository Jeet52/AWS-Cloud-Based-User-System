
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this in production!

# MySQL config
db_config = {
    'host': 'userdb.ch62kqu8cwq7.us-east-2.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Patel2025',
    'database': 'userdb'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Home redirects to login
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Register (Create)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()

        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username=%s OR email=%s", (username, email))
            if cursor.fetchone():
                flash('Username or email already exists!', 'error')
                return render_template('register.html')

            cursor.execute(
                "INSERT INTO users (username, email, password_hash, first_name, last_name) VALUES (%s, %s, %s, %s, %s)",
                (username, email, hashed_password, first_name, last_name)
            )
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Database error: {e}", 'error')
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')

# Login (Read)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email'].strip()
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username=%s OR email=%s", (username_or_email, username_or_email))
            user = cursor.fetchone()
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash('Logged in successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username/email or password.', 'error')
        except Exception as e:
            flash(f"Database error: {e}", 'error')
        finally:
            cursor.close()
            conn.close()

    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('login'))

    return render_template('dashboard.html', username=session.get('username'))

# Admin user search (Read with filters)
@app.route('/users', methods=['GET', 'POST'])
def users():
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('login'))

    search_results = []
    if request.method == 'POST':
        search_term = request.form['search'].strip()
        filter_by = request.form['filter_by']

        query = "SELECT username, email, first_name, last_name FROM users WHERE "
        params = ()

        if filter_by == 'username':
            query += "username LIKE %s"
            params = (f"%{search_term}%",)
        elif filter_by == 'email':
            query += "email LIKE %s"
            params = (f"%{search_term}%",)
        elif filter_by == 'name':
            query += "(first_name LIKE %s OR last_name LIKE %s)"
            params = (f"%{search_term}%", f"%{search_term}%")

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            search_results = cursor.fetchall()
        except Exception as e:
            flash(f"Database error: {e}", 'error')
        finally:
            cursor.close()
            conn.close()

    return render_template('users.html', users=search_results)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
