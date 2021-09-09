from flask import Flask, request, session, redirect, url_for, render_template, Response
from flask.helpers import flash
from flaskext.mysql import MySQL
import pymysql
from pymysql import cursors 
from werkzeug.utils import secure_filename
import os
from .consumer import Consumer
from .fileToDB import MeterReading
from .Billing import Bill
import re 
from .connection import Connection
import hashlib
import os
# import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.secret_key = 'weareateamofidkhowmany'

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

app.config["CSV_UPLOADS"] = "C:\\Users\\adamle\\Documents\\ElecBillSys\\application\\static\\file\\get"
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
    msg = ''
    if request.method == 'POST'and 'inputCredentials' in request.form and 'inputId' in request.form and 'inputPassword' in request.form:
        username = request.form['inputId']
        print(username)
        password = request.form['inputPassword']
        # hash_password = generate_password_hash(password)
        # print(hash_password)
        role = request.form['inputCredentials']
        print(role)
        
        cursor.execute('SELECT * FROM login_info WHERE user_name = %s', (username))
        account = cursor.fetchone()
        pwd = account['password']
        uType = account['user_type']
        print(f"Account {account}")
        print(pwd)
        print(uType == role)
        print(check_password_hash(pwd,password))
        
        if account and check_password_hash(pwd,password) and uType == role :
            session['loggedin'] = True
            session['id'] = account['user_name']
            session['role'] = role
            print(role)
            if role == "1":
                session["task"] = "add"
                session["taskC"] = "add"
                return redirect(url_for('adminCust'))
            elif account and role == "2":
                return redirect(url_for('billsList'))
                # return redirect(url_for('billDetail'))
            elif role == "3":
                return redirect(url_for('meterReading'))
        else:
            msg = 'Incorrect Username or Password!'  
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
            # Begin Add
            if task == "add":
                conn = mysql.connect()
                consumer = Consumer(conn,request)
                msg = None
                try:
                    val = consumer.insertConsumer()
                    if val:
                        conn.commit()
                        msg = "Consumer Succefully Added"
                    else:
                        msg = "Unable to Add Consumer"
                finally:
                    conn.close()
                print(msg)
                return render_template("customerDataInput.html", msg = msg, val = task, js = js)
            # End Add

            # Begin Update
            elif task == "upd":
                cid = request.form['inputConFilID']
                conn = mysql.connect()
                consumer = Consumer(conn, request)
                msg = None
                # Messages for testing
                print("in Update")
                print(cid)
                print(request.form['state'])
                if request.form['state'] == "1":
                    try:
                        try:
                            print("actually updating")
                            cid = request.form['realID']
                            print(cid)
                            print("Printing cid")
                            updateCon = consumer.updateConsumer(cid, request)
                            if updateCon:
                                msg = "Customer updated Sucessfully"
                            else:
                                msg = "Unable to update consumer 1"
                        except:
                            msg = "Unable to update consumer"
                    finally:
                        conn.close()
                else:
                    findCon = consumer.getConsumer(cid)
                    if not findCon:
                        msg = "Unable to find the consumer"

                js = {"cid":cid,"fname":consumer.fname, "lname":consumer.lname, "address":consumer.address, "taluka":consumer.taluka, "district":consumer.district, "pinCode":consumer.pinCode, "email":consumer.email, "contact":consumer.contact}
                print(js)
                print(msg)
                return render_template("customerDataInput.html", val = task, js = js)
            # End Update

            # Begin Delete
            elif task == "del":
                js = {"fname":"", "lname":"", "cid":"", "address":"", "taluka":"", "district":"", "pinCode":"", "meterId":"", "conType":"", "contact":"", "sanctionedLoad":""}
                cid = request.form['inputConFilID']
                print(cid)
                conn = mysql.connect()
                consumer = Consumer(conn, request)
                consumer.getConsumer(cid)
                msg = None
                print("in Delete")
                print(request.form['state'])
                if request.form['state'] == "1":
                    try:
                        try:
                            print("actually deleting")
                            print(request.form['realID'])
                            cid = request.form['realID']
                            
                            val = consumer.deleteConsumer(cid)
                            
                            if val:
                                msg = "Customer deleted Sucessfully"
                            else:
                                msg = "Unable to delete cutomer"
                        except:
                            msg = "Unable to delete consumer"
                    finally:
                        conn.close()
                else:
                    val2 = consumer.getConsumer(cid)
                    js = {"cid":cid,"fname":consumer.fname, "lname":consumer.lname, "address":consumer.address, "taluka":consumer.taluka, "district":consumer.district, "pinCode":consumer.pinCode, "email":consumer.email, "contact":consumer.contact}
                    if not val2:
                        msg = "Unable to find the consumer"
                
                print(js)
                print(msg)
                return render_template("customerDataInput.html", val = task, js = js) 
            #Delete end
        # User is loggedin show them the home page
        return render_template("customerDataInput.html", val = task, js = js)
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
                conn = mysql.connect()
                meterReading = MeterReading(conn)
                val = meterReading.readFile()
                if val:
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
    bid = request.args['id']
    print(f"BID : {bid}")
    conNo = session["id"]
    conn = mysql.connect()
    bill = Bill(conn)
    breakUP = bill.getBillBreakUp(bid)
    consumer = Consumer(conn)
    consumer.getConsumer(conNo)
    connection = Connection(conn,request)
    connection.getConnectionByMeterNo(bill.meterNo)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT San_Load, Con_Type FROM connection_type WHERE Con_Type_ID = %s ",(connection.conType))
    temp = cursor.fetchone()
    sancLoad = temp["San_Load"]
    conType = temp["Con_Type"]
    js = {"fname":consumer.fname, "amount":round(bill.amount,2),"instDt":connection.installationDate,"email":consumer.email, "instNo":connection.installationID,"lname":consumer.lname, "cid":consumer.cid, "address":connection.connAddress, "taluka":connection.connTaluka, "district":connection.connDistrict, "pinCode":connection.connPin, "meterId":connection.meterNo, "conType":conType, "contact":consumer.contact, "sanctionedLoad":sancLoad, "breakUP":breakUP}
    print(js)
    return render_template("complainDetail.html", js=js, consumer=consumer, connection=connection, bill=bill)

@app.route("/billTimeline")
def billTimeline():
    return render_template("billTimeline.html")  


@app.route("/billsList")
def billsList():
    cNo = session["id"]
    print(f"CNO = {cNo}")
    conn = mysql.connect()
    bill = Bill(conn)
    billNos,billDates, meterNos, amountDues, unitsConsumed, connectionIDs, prevDates = bill.getBillsByCNo(cNo)
    length = len(billNos)
    BillPaymentStatus = [True,False,False,True,False]   #should be taken from the db too
    return render_template("billslist.html",prevDates=prevDates,billNos=billNos,billDates=billDates,length=length,BillPaymentStatus=BillPaymentStatus,meterNos=meterNos,amountDues=amountDues,unitsConsumed=unitsConsumed,connectionIDs=connectionIDs)

@app.route("/billDetail")
def billDetail():
    bid = request.args['id']
    print(f"BID : {bid}")
    conNo = session["id"]
    conn = mysql.connect()
    bill = Bill(conn)
    breakUP = bill.getBillBreakUp(bid)
    consumer = Consumer(conn)
    consumer.getConsumer(conNo)
    connection = Connection(conn,request)
    connection.getConnectionByMeterNo(bill.meterNo)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT San_Load, Con_Type FROM connection_type WHERE Con_Type_ID = %s ",(connection.conType))
    temp = cursor.fetchone()
    sancLoad = temp["San_Load"]
    conType = temp["Con_Type"]
    js = {"fname":consumer.fname, "amount":round(bill.amount,2),"instDt":connection.installationDate,"email":consumer.email, "instNo":connection.installationID,"lname":consumer.lname, "cid":consumer.cid, "address":connection.connAddress, "taluka":connection.connTaluka, "district":connection.connDistrict, "pinCode":connection.connPin, "meterId":connection.meterNo, "conType":conType, "contact":consumer.contact, "sanctionedLoad":sancLoad, "breakUP":breakUP}
    print(js)
    return render_template("billDetail.html", js=js, connection = connection, consumer=consumer, bill = bill) 

@app.route("/adminConn", methods=["POST", "GET"])
def adminConn():
    
    js = {"cid": "", "cno":"", "connType":"", "meterNo":"","caddress":"", "cdistrict":"", "ctaluka":"", "connStatus":"", "cpinCode":"", "installationDate":""}

    if 'loggedin' in session and session['role'] == "1":
        taskC = session["taskC"]

        js = {"cid": "", "cno":"", "connType":"", "meterNo":"","caddress":"", "cdistrict":"", "ctaluka":"", "connStatus":"", "cpinCode":"", "installationDate":""}
    

        if request.method == "POST" and 'taskC' in request.form:
                session["taskC"] = request.form['taskC']
                taskC = session["taskC"]
                print(session["taskC"])
                # Begin Add
                if taskC == "add":
                    conn = mysql.connect()

                    connection = Connection(conn, request)
                    msg = None
                    try:
                        val = connection.insertConnection()
                        if val:
                            conn.commit()
                            msg = "Connection Succefully Added"
                        else:
                            msg = "Unable to Add Connection"
                    finally:
                        conn.close()
                    print(msg)
                    return render_template("connectionDataInput.html", msg = msg, val = taskC, js = js)
                # End Add

                # Begin Delete
                elif taskC == "del":
                    
                    conid = request.form['inputConnFilID']
                    print(conid)
                    conn = mysql.connect()
                    connection = Connection(conn, request)
                    connection.getConnection(conid)
                    msg = None
                    print("in Delete")
                    print(request.form['stateC'])
                    if request.form['stateC'] == "1":
                        try:
                            try:
                                print("actually deleting")
                                print(request.form['realID'])
                                conid = request.form['realID']
                                
                                val = connection.deleteConnection(conid)
                                
                                if val:
                                    msg = "connection deleted Sucessfully"
                                else:
                                    msg = "Unable to delete connection 1"
                            except:
                                msg = "Unable to delete connection 2"
                        finally:
                            conn.close()
                    else:
                        val2 = connection.getConnection(conid)
                        js = {"cid": connection.connID, "cno":connection.conNo, "connType":connection.conType, "meterNo":connection.meterNo,"caddress":connection.connAddress, "cdistrict":connection.connDistrict, "ctaluka":connection.connTaluka, "connStatus":connection.connStatus, "cpinCode":connection.connPin, "installationDate":connection.installationDate}
                        if not val2:
                            msg = "Unable to find the connection" 
                    print(js)
                    print(msg)
                    return render_template("connectionDataInput.html", val = taskC, js = js) 
                # End Delete

                # Begin Update
                elif taskC == "upd":
                    connid = request.form['inputConnFilID']

                    conn = mysql.connect()
                    connection = Connection(conn, request)
                    msg = None

                    # Messages for testing
                    print("in Update")
                    print("ConnectionID : ",connid)

                    print(request.form['stateC'])
                    if request.form['stateC'] == "1":
                        try:
                            try:
                                print("actually updating")
                                connid = request.form['realID']
                                print("ConnectionID : ",connid)

                                updateConn = connection.updateConnection(connid, request)
                                if updateConn:
                                    msg = "Connection updated Sucessfully"
                                else:
                                    msg = "Unable to update connection 1"
                            except:
                                msg = "Unable to update connection 2"
                        finally:
                            conn.close()
                    else:
                        findConn = connection.getConnection(connid)
                        js = {"cid": connection.connID, "cno":connection.conNo, "connType":str(connection.conType), "meterNo":connection.meterNo,"caddress":connection.connAddress, "cdistrict":connection.connDistrict, "ctaluka":connection.connTaluka, "connStatus":connection.connStatus, "cpinCode":connection.connPin, "installationDate":connection.installationDate}
                        if not findConn:
                            msg = "Unable to find the connection"
                    
                    print(js)
                    print(msg)
                    return render_template("connectionDataInput.html", val = taskC, js = js)
                # End Update

    return render_template("connectionDataInput.html", js=js, val=taskC)

@app.route("/meterReading", methods=["GET", "POST"])
def meterReading():
    conn = mysql.connect()
    meterRead = MeterReading(conn,session['id'])
    if request.method=="POST":
        if 'formStateGet' in request.form:
            csv,filename = meterRead.createMeterReadingFile()
            return Response(csv,
                            mimetype="text/csv",
                            headers={"Content-disposition":
                                    f"attachment; filename={filename}"})
        elif 'formStatePost' in request.form:
            if request.files:
                file = request.files["uploadCsv"]
                if file.filename == "":
                    print("No filename")
                    return redirect(request.url)
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config["CSV_UPLOADS"], filename))
                    conn = mysql.connect()
                    meterReading = MeterReading(conn,session['id'])
                    val = meterReading.readFile()
                    if val:
                        print("file saved")
                        return redirect(request.url)
                else:
                    print("That file extension is not allowed")
                    return redirect(request.url)
    return render_template("meterReading.html")

@app.route("/test")
def test():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    consumer = Consumer(conn,cursor)
    sql = consumer.validateCId()
    print(sql)
    return "<h1>testing<h1>"

@app.route("/nav")
def nav():
    return render_template(".html")

            # csv="Consumer No, Consumer First Name, Consumer Last Name, Connection No, Meter No, Address, District, Taluka, Pin Code, Contact, Email"
