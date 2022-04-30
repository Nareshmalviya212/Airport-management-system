from flask import Flask, render_template, request, redirect, url_for
import pymysql
db_connection = None
tb_cursor = None

#create object of Flask class
app = Flask(__name__)

# function to connect to databse
def connectToDb():
    global db_connection, tb_cursor
    db_connection=pymysql.connect(host="localhost",user="root",
    passwd="",database="airport_db",port=3306)
    if(db_connection):
        print("Done!!!")
    else:
        print("Not done")
    tb_cursor=db_connection.cursor()

# function to dicconnect from databse
def disconnectDb():
    db_connection.close()
    tb_cursor.close()

# function to get data from databse
def getAllPassengerData():
    connectToDb()
    selectQuery = "SELECT * FROM airport_system;"
    tb_cursor.execute(selectQuery)
    allData = tb_cursor.fetchall()
    disconnectDb()
    return allData

#function to insert data into the table
def insertIntoTable(name,contact,email,passport,flight,takeoff,land,date):
    connectToDb()
    inserQuery = "INSERT INTO airport_system(NAME,CONTACT,EMAIL,PASSPORT,FLIGHT,TAKEOFF,LAND,DATE) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
    tb_cursor.execute(inserQuery,(name,contact,email,passport,flight,takeoff,land,date))
    db_connection.commit()
    disconnectDb()
    return True

# function to get data of one passenger from databse
def getPassengerID(passenger_id):
    connectToDb()
    selectQuery = "SELECT * FROM airport_system WHERE ID=%s;"
    tb_cursor.execute(selectQuery,(passenger_id,))
    oneData = tb_cursor.fetchone()
    disconnectDb()
    return oneData

#function to update data into the table
def updatePassengerIntoTable(name,contact,email,passport,flight,takeoff,land,date,id):
    connectToDb()
    updateQuery = "UPDATE airport_system SET NAME=%s,CONTACT=%s,EMAIL=%s,PASSPORT=%s,FLIGHT=%s,TAKEOFF=%s,LAND=%s,DATE=%s WHERE ID=%s;"
    tb_cursor.execute(updateQuery,(name,contact,email,passport,flight,takeoff,land,date,id))
    db_connection.commit()
    disconnectDb()
    return True

#function to update data into the table
def deletePassengerFromTable(id):
    connectToDb()
    deleteQuery = "DELETE FROM airport_system WHERE ID=%s;"
    tb_cursor.execute(deleteQuery,(id,))
    db_connection.commit()
    disconnectDb()
    return True


#a method that envoked at server execution
@app.route("/")
@app.route("/index/")
def index():
    allData = getAllPassengerData()
    return render_template("index.html",data = allData)

@app.route("/add/",methods=["GET","POST"])
def addPassenger():
    if request.method == "POST":
        data = request.form
        isiInserted = insertIntoTable(data['txtName'],data['txtContact'],data['txtEmail'],data['txtPassport'],data['txtFlight'],data['txtTakeOff'],data['txtLand'],data['txtDate'])
        if(isiInserted):
            message = "Insertion sucess"
        else:
            message = "Insertion Error"
        return render_template("add.html",message = message)
    return render_template("add.html")

@app.route("/update/",methods=["GET","POST"])
def updatePassenger():
    id = request.args.get("ID",type=int,default=1)
    idData = getPassengerID(id)
    if request.method == "POST":
        data = request.form
        print(data)
        isUpdated = updatePassengerIntoTable(data['txtName'],data['txtContact'],data['txtEmail'],data['txtPassport'],data['txtFlight'],data['txtTakeOff'],data['txtLand'],data['txtDate'],id)
        if(isUpdated):
            message = "Updattion sucess"
        else:
            message = "Updattion Error"
        return render_template("update.html",message = message)
    return render_template("update.html",data=idData)

@app.route("/delete/")
def deletePassenger():
    id = request.args.get("ID",type=int,default=1)
    deletePassengerFromTable(id)
    return redirect(url_for("index"))



#to execute the code
if __name__=='__main__':
    app.run(debug=True)