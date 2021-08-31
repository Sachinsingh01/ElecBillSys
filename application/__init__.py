from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
import pymysql 
from werkzeug.utils import secure_filename
import os
import re 



app = Flask(__name__)

app.secret_key = 'weareateamofidkhowmany'

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'sql6433489'
app.config['MYSQL_DATABASE_PASSWORD'] = 'tC7bZ7lzuf'
app.config['MYSQL_DATABASE_DB'] = 'sql6433489'
app.config['MYSQL_DATABASE_HOST'] = 'sql6.freemysqlhosting.net'
mysql.init_app(app)

app.config["CSV_UPLOADS"] = "C:\\Users\\adamle\\Documents\\ElecBillSys\\application\\static\\file"
# app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["CSV"]

def allowed_file(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() == "CSV":
        return True
    else:
        return False

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
    if request.method == 'POST'and 'inputCredentials' in request.form and 'inputId' in request.form and 'inputPassword' in request.form:
        # Create variables for easy access

        username = request.form['inputId']
        password = request.form['inputPassword']
        role = request.form['inputCredentials']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM user WHERE id = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
   
    # If account exists in accounts table in out database
        if account and role == "1":
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['role'] = role
            session["task"] = "add"
            # session['username'] = account['username']
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('adminCust'))
        elif account:
            session['loggedin'] = True
            session['id'] = account['id']
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

@app.route("/adminCust", methods=["POST", "GET"])
def adminCust():
    if 'loggedin' in session and session['role'] == "1":
        print("56843")
        task = session["task"]
        cid = ""
        fname = ""
        lname = ""
        address = ""
        taluka = ""
        district = ""
        pinCode = ""
        meterId = ""
        conType = ""
        contact = ""
        sanctionedLoad = ""
        js = {"fname":fname,"lname":lname,"cid":cid}
        if request.method == "POST" and 'task' in request.form:
            session["task"] = request.form['task']
            task = session["task"]
            print(session["task"])
            #Add start
            if task == "add":
                cid = request.form['inputConID']
                fname = request.form['inputConFName']
                lname = request.form['inputConLName']
                address = request.form['inputConAddress']
                taluka = request.form['inputConTaluka']
                district = request.form['inputConDistrict']
                pinCode = request.form['inputConPin']
                meterId = request.form['inputMeterId']
                conType = request.form['inputConType']
                contact = request.form['inputConContact']
                sanctionedLoad = request.form['inputSancLoad']
                print(cid , fname, lname, address, taluka, district, pinCode, meterId, conType, contact,sanctionedLoad)
                msg = "Customer succefully added"
                print(msg)
                return render_template("customerDataInput.html", msg = msg, val = task, js = js)
            #Add End
            #Update Start
            elif task == "upd":
                cid = request.form['inputConFilID']
                print("In Update " )
                print(cid)
                #Database Query 
                #assumed that data is valid
                fname = "you"
                lname = "Exist"
                address = "no home"
                taluka = "Ponda"
                district = "Confused"
                pinCode = "403406"
                meterId = "PON131231"
                conType = "Domestic"
                contact = "9876543210"
                sanctionedLoad = "1.2"
                js = {"fname":fname,"lname":lname,"cid":cid}
                print(js)
                return render_template("customerDataInput.html", val = task, js = js)
            #Update end

            #delete start
            elif task == "del":
                cid = request.form['inputConFilID']
                print("In Update " )
                print(cid)
                #Database Query 
                #assumed that data is valid
                fname = "you"
                lname = "Exist"
                address = "no home"
                taluka = "Ponda"
                district = "Confused"
                pinCode = "403406"
                meterId = "PON131231"
                conType = "Domestic"
                contact = "9876543210"
                sanctionedLoad = "1.2"
                js = {"fname":fname,"lname":lname,"cid":cid}
                print(js)
                return render_template("customerDataInput.html", val = task, js = js) 
            #Delete end
        # User is loggedin show them the home page
        return render_template("customerDataInput.html", val = task, js=js)
    # User is not loggedin redirect to login page

    return redirect(url_for('login'))

@app.route("/uploadFile", methods=["GET", "POST"])
def uploadFile():
    if request.method == "POST":

        if request.files:
            file = request.files["csvfile"]

            if file.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_file(file.filename):
                filename = secure_filename(file.filename)

                file.save(os.path.join(app.config["CSV_UPLOADS"], filename))

                print("file saved")

                return redirect(request.url)

            else:
                print("That file extension is not allowed")
                return redirect(request.url)
    return render_template("meterReading.html")

@app.route("/complainList")
def complainList():
    return render_template("complainList.html")

@app.route("/complainDetail")
def complainDetail():
    return render_template("complainDetail.html")

@app.route("/billTimeline")
def billTimeline():
    return render_template("billTimeline.html")  

@app.route("/billDetail")
def billDetail():
    return render_template("billDetail.html") 
