from flask import Flask, redirect, url_for, render_template, request, session
import mysql.connector

app = Flask(__name__)

# Secret key for session management (change this to a random string in production)
app.secret_key = '2002'

# Database configuration
db_config = {
    'user': 'root',
    'password': '2002',
    'host': 'localhost',
    'database': 'sign'
}

# Home route
@app.route("/")
def index():
    return render_template('index.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, password)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return "Error occurred while inserting data into the database"

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and user['password'] == password:
                session['email'] = email
                return redirect(url_for('home'))
            else:
                error_message = "Invalid email or password. Please try again."
                return render_template('login.html', error=error_message)

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            error_message = "An error occurred. Please try again later."
            return render_template('login.html', error=error_message)

    return render_template('login.html')

# Secure home page route
@app.route('/home')
def home():
    if 'email' in session:
        return render_template('secure.html')
    else:
        return redirect(url_for('login'))
    
# Logout route
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

