from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
import pymysql 
import re 



app = Flask(__name__)

app.secret_key = 'weareateamofidkhowmany'

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'sql6433489'
app.config['MYSQL_DATABASE_PASSWORD'] = 'tC7bZ7lzuf'
app.config['MYSQL_DATABASE_DB'] = 'sql6433489'
app.config['MYSQL_DATABASE_HOST'] = 'sql6.freemysqlhosting.net'
mysql.init_app(app)


@app.route("/")
def home():
    if 'loggedin' in session:
   
        # User is loggedin show them the home page
        return render_template('home.html', username=session['id'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



@app.route("/login", methods=['GET', 'POST'])
def login():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST'and 'inputId' in request.form and 'inputPassword' in request.form:
        # Create variables for easy access
        username = request.form['inputId']
        password = request.form['inputPassword']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM user WHERE id = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
   
    # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            # session['username'] = account['username']
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
    return render_template('login.html', msg=msg)

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
   # Redirect to login page
    return redirect(url_for('login'))

@app.route("/adminCust")
def adminCust():
    return render_template("customerDataInput.html")
    
