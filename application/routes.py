from application import app
from flask import render_template

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/next")
def next():
    return "hi"


""" 
conn = mysql.connect()
cursor = conn.cursor()

#endpoint for search
@app.route('/consumerFilter.html', methods=['GET', 'POST'])
def consumerFilter():
    if request.method == "POST":
        cID = request.form['inputConID']
        cursor.execute("SELECT * FROM Consumer WHERE ConID = cID")
        data = cursor.fetchone()
        if len(data) == 0:
            msg = "Invalid Consumer ID"
            return render_template('/consumerFilter.html', msg=msg)
        else:
            cid = data[0]
            fname = data[1]
            lname = data[2]
            address = data[3]
            taluka = data[4]
            district = data[5]
            pinCode = data[6]
            meterId = data[7]
            conType = data[8]
            contact = data[9]
            sanctionedLoad = data[10]

            js = {"cid":cid,"fname":fname,"lname":lname,"address":address,"taluka":taluka,"district":district,"pinCode":pinCode,"meterId":meterId,"conType":conType,"contact":contact,"sanctionedLoad":sanctionedLoad}
            return render_template('/consumerFilter.html',js=js)
    return redirect(url_for('/consumerFilter.html'))
 """