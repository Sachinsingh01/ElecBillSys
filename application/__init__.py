from numpy import number
from application.user import User
from application.ditributor import Distributor
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
from datetime import date
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
        roleId = session['role']
        uName = session['uName']
        uId = session['id']
        if roleId == "1":
            return render_template("dash.html", roleId = roleId, uName=uName, uId=uId)
        elif roleId == "2":
            return render_template("consumerDash.html", roleId = roleId, uName=uName, uId=uId)
        elif roleId == "3":
            return redirect(url_for('meterReading'))
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
        # print(f"Account {account}")
        # print(pwd)
        # print(uType == role)
        # print(check_password_hash(pwd,password))
        
        if account and check_password_hash(pwd,password) and uType == role :
            session['loggedin'] = True
            session['id'] = account['user_name']
            session['role'] = role
            print(role)
            if role == "1":
                session["uName"] = "ADMINISTRATOR"
                session["task"] = "add"
                session["taskC"] = "add"
                session["taskD"] = "add"
                return redirect(url_for('dashboard'))
            elif account and role == "2":
                cursor.execute("SELECT CONCAT(Con_First_Name , ' ' , Con_Last_Name) as Name from consumer where Con_No = %s", (session['id']))
                session["uName"] = cursor.fetchone()['Name']
                return redirect(url_for('dashboardCon'))
                # return redirect(url_for('billDetail'))
            elif role == "3":
                session["uName"] = "METER GUY"
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
        roleId = session['role']
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
                # Only sending Role because user is Admin and username is Administrator
                return render_template("customerDataInput.html", msg = msg, val = task, js = js, roleId = roleId, uName=session["uName"], uId=session["id"])
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
                return render_template("customerDataInput.html", val = task, js = js, roleId = roleId, uName=session["uName"], uId=session["id"])
            # End Update

            # Begin Delete
            elif task == "del":
                js = {"fname":"", "lname":"", "cid":"", "address":"", "taluka":"", "district":"", "pinCode":"", "meterId":"", "conType":"", "contact":"", "sanctionedLoad":""}
                cid = request.form['inputConFilID']
                print(cid)
                conn = mysql.connect()
                consumer = Consumer(conn, request)
                try:
                    consumer.getConsumer(cid)
                except Exception as e:
                    print(e)
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
                        except Exception as e:
                            print(e)
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
                return render_template("customerDataInput.html", val = task, js = js, roleId = roleId, uName=session["uName"], uId=session["id"]) 
            #Delete end
        # User is loggedin show them the home page
        return render_template("customerDataInput.html", val = task, js = js, roleId = roleId, uName=session["uName"], uId=session["id"])
    # User is not loggedin redirect to login page

    return redirect(url_for('login'))

@app.route("/uploadFile", methods=["GET", "POST"])
def uploadFile():
    if request.method == "POST":
        roleId = session['role']
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

    # Only sending role because user is admin            
    return render_template("meterReading.html", roleId = roleId, uName=session["uName"], uId=session["id"])

#Functionality has to be added
@app.route("/fileComplaint", methods=["GET", "POST"])
def fileComplaint(): 
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method=="POST":
        #take values from the submitted form
        billId = request.form['inputBillId']
        connectionId = request.form['inputConnID']
        complaintCategory = request.form['inputCompType']
        comment = request.form['inputCompDesc']
        created = str(date.today())
        updated = str(date.today())
        status = 'unresolved'
        try:
            #query to insert the new complaint into the bill_complain table
            cursor.execute("INSERT INTO bill_complain(`bill_id`,`co_id`,`category`,`status`,`comment`,`created`,`updated`) VALUES(%s,%s,%s,%s,%s,%s,%s)",(billId,connectionId,complaintCategory,status,comment,created,updated))
            print("Success!")
            conn.commit()
        except Exception as e:
            print(e)

    return render_template("fileComplaint.html", uName=session["uName"], uId=session["id"])

@app.route("/complainList", methods=["GET", "POST"])
def complainList():
    roleId = session['role']
    
    complainCategory = [1,2,2,1]
    complainIDs = [1991,1992,1993,1994]
    connectionIDs = [3001,3002,3003,3004]
    length = 4
    complainStatus = [1,2,1,2]
    return render_template("complainList.html", uName=session["uName"], uId=session["id"],complainStatus=complainStatus,complainCategory=complainCategory,complainIDs=complainIDs,connectionIDs=connectionIDs,length=length, roleId = roleId)

@app.route("/complainDetail")
def complainDetail():
    bid = request.args['id']
    print(f"BID : {bid}")
    conNo = session["id"]
    roleId = session['role']
    conn = mysql.connect()
    bill = Bill(conn)
    breakUP = bill.getBillBreakUp(bid)
    consumer = Consumer(conn)
    consumer.getConsumer(conNo)
    connection = Connection(conn,request)
    connection.getConnectionByMeterNo(bill.meterNo)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT San_Load, Con_Type FROM connection_type WHERE Con_Type_ID = %s ",(connection.conType))
        temp = cursor.fetchone()
        sancLoad = temp["San_Load"]
        conType = temp["Con_Type"]
        js = {"fname":consumer.fname, "amount":round(bill.amount,2),"instDt":connection.installationDate,"email":consumer.email, "instNo":connection.installationID,"lname":consumer.lname, "cid":consumer.cid, "address":connection.connAddress, "taluka":connection.connTaluka, "district":connection.connDistrict, "pinCode":connection.connPin, "meterId":connection.meterNo, "conType":conType, "contact":consumer.contact, "sanctionedLoad":sancLoad, "breakUP":breakUP}
        consumerName = consumer.fname + " " + consumer.lname
        print(js)
        return render_template("complainDetail.html", js=js, consumer=consumer, connection=connection, bill=bill, roleId = roleId, consumerNo = conNo, consumerName = consumerName)
    except Exception as e:
        print(e)
        return redirect(url_for('complainList'))

@app.route("/billTimeline")
def billTimeline():
    return render_template("billTimeline.html")  


@app.route("/billsList")
def billsList():
    cNo = session["id"]
    roleId = session['role']
    if roleId == "1":
        conn = mysql.connect()
        bill = Bill(conn)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        billNos,billDates, meterNos, amountDues, unitsConsumed, connectionIDs, prevDates = [],[],[],[],[],[],[]
        cursor.execute("SELECT Con_No FROM consumer")
        cNos = cursor.fetchall()
        for cNo in cNos:
            billNo,billDate, meterNo, amountDue, unitsConsume, connectionID, prevDate = bill.getBillsByCNo(cNo["Con_No"])
            billNos.append(billNo)
            billDates.append(billDate)
            meterNos.append(meterNo)
            amountDues.append(amountDue)
            unitsConsumed.append(unitsConsume)
            connectionIDs.append(connectionID)
            prevDates.append(prevDate)
        billNos = [j for sub in billNos for j in sub]
        billDates = [j for sub in billDates for j in sub]
        meterNos = [j for sub in meterNos for j in sub]
        amountDues = [j for sub in amountDues for j in sub]
        unitsConsumed = [j for sub in unitsConsumed for j in sub]
        connectionIDs = [j for sub in connectionIDs for j in sub]
        prevDates = [j for sub in prevDates for j in sub]
        length = len(billNos)
        BillPaymentStatus = [True,False,False,True,False]
        consumerName = ""
    elif roleId == "2":
        print(f"CNO = {cNo}")
        conn = mysql.connect()
        bill = Bill(conn)
        billNos,billDates, meterNos, amountDues, unitsConsumed, connectionIDs, prevDates = bill.getBillsByCNo(cNo)
        length = len(billNos)
        BillPaymentStatus = [True,False,False,True,False]   #should be taken from the db too
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM consumer WHERE Con_No = %s",(cNo))
        record = cursor.fetchone()
        consumerName = record['Con_First_Name'] + " " + record['Con_Last_Name']
    return render_template("billslist.html", uName=session["uName"], uId=session["id"],prevDates=prevDates,billNos=billNos,billDates=billDates,length=length,BillPaymentStatus=BillPaymentStatus,meterNos=meterNos,amountDues=amountDues,unitsConsumed=unitsConsumed,connectionIDs=connectionIDs, roleId = roleId, consumerNo = cNo, consumerName = consumerName)


@app.route("/billDetail")
def billDetail():
    bid = request.args['id']
    print(f"BID : {bid}")
    conNo = session["id"]
    roleId = session['role']
    conn = mysql.connect()
    bill = Bill(conn)
    breakUP = bill.getBillBreakUp(bid)
    consumer = Consumer(conn)
    consumer.getConsumer(bill.conNo)
    connection = Connection(conn,request)
    connection.getConnectionByMeterNo(bill.meterNo)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT San_Load, Con_Type FROM connection_type WHERE Con_Type_ID = %s ",(connection.conType))
    temp = cursor.fetchone()
    sancLoad = temp["San_Load"]
    conType = temp["Con_Type"]
    js = {"fname":consumer.fname, "amount":round(bill.amount,2),"instDt":connection.installationDate,"email":consumer.email, "instNo":connection.installationID,"lname":consumer.lname, "cid":consumer.cid, "address":connection.connAddress, "taluka":connection.connTaluka, "district":connection.connDistrict, "pinCode":connection.connPin, "meterId":connection.meterNo, "conType":conType, "contact":consumer.contact, "sanctionedLoad":sancLoad, "breakUP":breakUP}
    print(js)
    if roleId == "2":
        consumerName = consumer.fname + " " + consumer.lname
    else:
        consumerName = ""
    return render_template("billDetail.html", uName=session["uName"], uId=session["id"], js=js, connection = connection, consumer=consumer, bill = bill, consumerName = consumerName, consumerNumber = conNo, roleId = roleId) 

@app.route("/adminConn", methods=["POST", "GET"])
def adminConn():
    
    js = {"cid": "", "cno":"", "connType":"", "meterNo":"","caddress":"", "cdistrict":"", "ctaluka":"", "connStatus":"", "cpinCode":"", "installationDate":""}

    if 'loggedin' in session and session['role'] == "1":
        taskC = session["taskC"]
        roleId = session['role']
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

                    # only roleId cuz user is admin
                    return render_template("connectionDataInput.html", msg = msg, val = taskC, js = js, roleId = roleId, uName=session["uName"], uId=session["id"])
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
                    return render_template("connectionDataInput.html", val = taskC, js = js, roleId = roleId, uName=session["uName"], uId=session["id"]) 
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
                    return render_template("connectionDataInput.html", val = taskC, js = js, roleId = roleId, uName=session["uName"], uId=session["id"])
                # End Update
    return render_template("connectionDataInput.html", js=js, val=taskC, roleId = roleId)

    #return render_template("connectionDataInput.html", js=js, val=taskC, roleId = roleId, uName=session["uName"], uId=session["id"])

@app.route("/meterReading", methods=["GET", "POST"])
def meterReading():
    conn = mysql.connect()
    meterRead = MeterReading(conn,session['id'])
    roleId = session['role']
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
    return render_template("meterReading.html", roleId = roleId, uName=session["uName"], uId=session["id"])

@app.route("/test")
def test():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    consumer = Consumer(conn,cursor)
    sql = consumer.validateCId()
    print(sql)
    return "<h1>testing<h1>"

@app.route("/dashboard")
def dashboard():
    if 'pageNo' in request.args:
        pageNo = int(request.args['pageNo'])- 1
    else:
        pageNo = 0
    if 'coNo' in request.args:
        cid = request.args['coNo']  
    else:
        cid = ""
    roleId = session['role']
    # userName = session['']
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if cid == "":
        cursor.execute("SELECT COUNT(*) as c FROM consumer")
        n = cursor.fetchone()["c"]
        import math
        n = math.ceil(n/5)
        cursor.execute("SELECT Con_No FROM consumer ORDER BY Con_No LIMIT %s, %s",(pageNo*5,5))
        conNumbers = cursor.fetchall()
        consumers = []
        numberOfConnections = []
        for conNumber in conNumbers:
            consumer = Consumer(conn)
            consumer.getConsumer(conNumber["Con_No"])
            consumers.append(consumer)
            cursor.execute("SELECT count(*) as c FROM connection WHERE Con_ID = %s",(consumer.conID))
            num = cursor.fetchone()["c"]
            numberOfConnections.append(num)
        print(consumers)
        print(numberOfConnections)
        print(n)
        return render_template("dash.html", roleId = roleId, consumers = consumers, pageNo=pageNo+1, num = numberOfConnections,n=n, uName=session["uName"], uId=session["id"])
    else:
        consumers = []
        numberOfConnections = []
        consumer = Consumer(conn)
        consumer.getConsumer(cid)
        consumers.append(consumer)
        cursor.execute("SELECT count(*) as c FROM connection WHERE Con_ID = %s",(consumer.conID))
        num = cursor.fetchone()["c"]
        numberOfConnections.append(num)
        return render_template("dash.html", roleId = roleId, num=numberOfConnections, pageNo=0, n=0, consumers = consumers, uName=session["uName"], uId=session["id"])

@app.route("/dashboardCon")
def dashboardCon():
    cNo = session["id"]
    roleId = session['role']
    conn = mysql.connect()
    if roleId == "2":
        if 'bid' in request.args:
            bid = request.args['bid']
            bill = Bill(conn)
            bill.getBill(bid)
        else:
            bill = ""
        connections = []
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM consumer WHERE Con_No = %s",(cNo))
        record = cursor.fetchone()
        consumerName = record['Con_First_Name'] + " " + record['Con_Last_Name']
        print("Consumer Name")
        print(consumerName)
        return render_template("consumerDash.html",roleId=roleId,consumerName=consumerName,connections = connections,bill=bill, uName=session["uName"], uId=session["id"])
    return render_template("consumerDash.html",roleId=roleId,consumerName="", uName=session["uName"], uId=session["id"])

            # csv="Consumer No, Consumer First Name, Consumer Last Name, Connection No, Meter No, Address, District, Taluka, Pin Code, Contact, Email"


@app.route("/adminDistributor", methods=["POST", "GET"])
def adminDistributor():
    if 'loggedin' in session and session['role'] == "1":
        taskD = session["taskD"]
        roleId = session['role']
        js = {"disId":"","disCompName":"", "disAddress":"", "disDistrict":"", "disPincode":"", "suppplyMonth":"", "disContact":"", "supplyRate":"","created":"", "updated":""}

        if request.method == "POST" and 'taskD' in request.form:
            session["taskD"] = request.form['taskD']
            taskD = session["taskD"]
            print(session["taskD"])
            # Begin Add
            if taskD == "add":
                conn = mysql.connect()
                distributor = Distributor(conn, request)
                msg = None
                try:
                    val = distributor.insertDistributor()
                    if val:
                        conn.commit()
                        msg = "Distributor Succefully Added"
                    else:
                        msg = "Unable to Add Distributor"
                finally:
                    conn.close()
                print(msg)
                return render_template("distributorDataInput.html", msg = msg, val = taskD, js = js, roleId = roleId, uName=session["uName"], uId=session["id"])
            # End Add

            # Begin Update
            elif taskD == "upd":
                disId = request.form['inputDistFilID']
                conn = mysql.connect()
                distributor = Distributor(conn, request)
                msg = None
                # Messages for testing
                print("in Update")
                print(disId)
                print(request.form['stateD'])
                if request.form['stateD'] == "1":
                    try:
                        try:
                            print("actually updating")
                            disId = request.form['inputDistID']
                            print("Printing dis ID", disId)
                            updateDis = distributor.updateDistributor(request, disId)
                            if updateDis:
                                msg = "Distributor updated Sucessfully"
                            else:
                                msg = "Unable to update distributor 1"
                        except:
                            msg = "Unable to update ditributor"
                    finally:
                        conn.close()
                else:
                    findDis = distributor.getDistributor(disId)
                    if not findDis:
                        msg = "Unable to find the Distributor"

                js = {"disId": disId ,"disCompName": distributor.disCompName, "disAddress": distributor.disAddress, "disDistrict": distributor.disDistrict, "disPincode": distributor.disPincode, "suppplyMonth": distributor.supplyPMonth, "disContact":distributor.disContact, "supplyRate": distributor.supplyRate,"created":distributor.created, "updated":distributor.updated}
                print(js)
                print(msg)
                return render_template("distributorDataInput.html", val = taskD, js = js, roleId = roleId, uName=session["uName"], uId=session["id"])
            # End Update

            # Begin Delete
            elif taskD == "del":
                js = {"disId":"","disCompName":"", "disAddress":"", "disDistrict":"", "disPincode":"", "suppplyMonth":"", "disContact":"", "supplyRate":"","created":"", "updated":""}
                disId = request.form['inputDistFilID']
                print(disId)
                conn = mysql.connect()
                distributor = Distributor(conn, request)
                distributor.getDistributor(disId)
                
                msg = None
                print("in Delete")
                print(request.form['stateD'])
                if request.form['stateD'] == "1":
                    try:
                        try:
                            print("actually deleting")
                            print(request.form['inputDistFilID'])
                            disId = request.form['inputDistFilID']
                            
                            val = distributor.deleteDistributor(disId)
                            
                            if val:
                                msg = "Distributor deleted Sucessfully"
                            else:
                                msg = "Unable to delete Distributor"
                        except:
                            msg = "Unable to delete Distributor 1"
                    finally:
                        conn.close()
                else:
                    val2 = distributor.getDistributor(disId)
                    js = {"disId": disId ,"disCompName": distributor.disCompName, "disAddress": distributor.disAddress, "disDistrict": distributor.disDistrict, "disPincode": distributor.disPincode, "suppplyMonth": distributor.supplyPMonth, "disContact":distributor.disContact, "supplyRate": distributor.supplyRate,"created":distributor.created, "updated":distributor.updated}
                    if not val2:
                        msg = "Unable to find the Distributor"
                
                print(js)
                print(msg)
                return render_template("distributorDataInput.html", val = taskD, js = js, roleId = roleId, uName=session["uName"], uId=session["id"]) 
            #Delete end
        # User is loggedin show them the home page
        return render_template("distributorDataInput.html", val = taskD, js = js, roleId = roleId, uName=session["uName"], uId=session["id"])
    # User is not loggedin redirect to login page

    return redirect(url_for('login'))

@app.route("/paymentHistory")
def paymentHistory():
    return render_template("paymentHistory.html", uName=session["uName"], uId=session["id"])
