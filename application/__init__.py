from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
import pymysql 
from werkzeug.utils import secure_filename
import os
from .consumer import Consumer
import re 



app = Flask(__name__)

app.secret_key = 'weareateamofidkhowmany'

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
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
        cursor.execute('SELECT * FROM user WHERE id = %s AND password = %s', (int(username), password))
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
        sanctionedLoad = 0
        print("hi")
        js = {"fname":fname, "lname":lname, "cid":cid, "address":address, "taluka":taluka, "district":district, "pinCode":pinCode, "meterId":meterId, "conType":conType, "contact":contact, "sanctionedLoad":sanctionedLoad}
        print("i am here")
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
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                consumer = Consumer(conn,cursor,cid , fname, lname, address, taluka, district, pinCode, meterId, conType, contact,sanctionedLoad)
                msg = None
                if not consumer.validateCId():
                    msg = "Invalid User ID"
                elif not consumer.validateMeterID():
                    msg = "Invalid Meter ID"
                elif not consumer.validateDistrict():
                    msg = "Invalid District"
                elif not consumer.validateTaluka():
                    msg = "invalid Taluka"
                
                if msg == None:
                    try:
                        val = consumer.insertConsumer()
                        if val:
                            conn.commit()
                            msg = "Customer succefully added"
                        else:
                            msg = "Unable to add Customer"
                    finally:
                        conn.close()
                print(msg)
                return render_template("customerDataInput.html", msg = msg, val = task, js = js)
            #Add End
            #Update Start
            elif task == "upd":
                cid = request.form['inputConFilID']
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                consumer = Consumer(conn,cursor,cid, fname, lname, address, taluka, district, pinCode, meterId, conType, contact,sanctionedLoad)
                msg = None
                print("in Update")
                print(cid)
                print(request.form['state'])
                if request.form['state'] == "1":
                    try:
                        try:
                            print("actually updating")
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
                            print(fname)
                            val = consumer.updateConsumer(cid, fname, lname, address, taluka, district, pinCode, meterId, conType, contact,sanctionedLoad)
                            if val:
                                msg = "Customer updated Sucessfully"

                            else:
                                msg = "Unable to update consumer"
                        except:
                            msg = "Unable to update consumer"
                    finally:
                        conn.close()
                else:
                    val2 = consumer.getConsumer()
                    if not val2:
                        msg = "Unable to find the consumer"
                js = {"fname":consumer.fname, "lname":consumer.lname, "cid":consumer.cid, "address":consumer.address, "taluka":consumer.taluka, "district":consumer.district, "pinCode":consumer.pinCode, "meterId":consumer.meterId, "conType":consumer.conType, "contact":consumer.contact, "sanctionedLoad":consumer.sanctionedLoad}
                print(js)
                print(msg)
                return render_template("customerDataInput.html", val = task, js = js)
            #Update end

            #delete start
            elif task == "del":
                cid = request.form['inputConFilID']
                print(cid)
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                consumer = Consumer(conn,cursor,cid, fname, lname, address, taluka, district, pinCode, meterId, conType, contact,sanctionedLoad)
                msg = None
                print("in Delete" )
                print(cid)
                print(request.form['state'])
                if request.form['state'] == "1":
                    try:
                        try:
                            print("actually deleting")
                            print(request.form['realID'])
                            val = consumer.deleteConsumer(cid = request.form['realID'])
                            
                            if val:
                                msg = "Customer deleted Sucessfully"

                            else:
                                msg = "Unable to delete cutomer"
                        except:
                            msg = "Unable to delete consumer"
                    finally:
                        conn.close()
                else:
                    val2 = consumer.getConsumer()
                    if not val2:
                        msg = "Unable to find the consumer"
                js = {"fname":consumer.fname, "lname":consumer.lname, "cid":consumer.cid, "address":consumer.address, "taluka":consumer.taluka, "district":consumer.district, "pinCode":consumer.pinCode, "meterId":consumer.meterId, "conType":consumer.conType, "contact":consumer.contact, "sanctionedLoad":consumer.sanctionedLoad}
                print(js)
                print(msg)
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

<<<<<<< HEAD
@app.route("/adminDist")
def adminDist():
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
    cid="12312"
    task = "add"
    js = {"fname":fname, "lname":lname, "cid":cid, "address":address, "taluka":taluka, "district":district, "pinCode":pinCode, "meterId":meterId, "conType":conType, "contact":contact, "sanctionedLoad":sanctionedLoad}
    print(js)
    return render_template("distributorDataInput.html", val = task, js=js) 
=======
@app.route("/test")
def test():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    consumer = Consumer(conn,cursor)
    sql = consumer.validateCId()
    print(sql)
    return "<h1>testing<h1>"


                    # try:
                    #     try:
                    #         # cursor.execute("INSERT INTO Consumer VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(cid,fname,lname,address,taluka,district,pinCode,meterId,conType,int(sanctionedLoad),contact))
                    #         val = consumer.insertConsumer()
                    #         conn.commit()
                    #         # NB : you won't get an IntegrityError when reading
                    #     except:
                    #         print("Exception")
                    #         return None
                    # finally:
                    #     conn.close()
                    # val = consumer.deleteConsumer()
                    # if val:
                    #     msg = "Customer deleted Sucessfully"
                    # else:
                    #     msg = "Unable to delete cutomer"
>>>>>>> 0cba7139c044a285ad94b2c1f8d5fe76b5c3c0ef
