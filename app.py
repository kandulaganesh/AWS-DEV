from flask import Flask,render_template,redirect,request,url_for
import mysql.connector
app = Flask(__name__)

print(__name__)

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80)

@app.route('/')
def hello_world():
    users = read_DB()
    msg = "Users available are "
    data = ""
    if len(users) == 0:
	msg = "No Users Available, "
    for user in users:
        data=data + user[1] + "\n"
    data = data + "  "
    return "Hello... " + msg + data + ",  Click on <a href='/insert'>AddNew</a> to add Users"

def read_DB():
    mydb = mysql.connector.connect(
              host="test-1.cbt0glpr7h4n.us-east-1.rds.amazonaws.com",
              user="admin",
              password="kandulaganesh",
              database="TestRDSDB"
            )

    mycursor=mydb.cursor()
    mycursor.execute("SELECT * FROM Persons")
    myresult = mycursor.fetchall()
    return myresult

@app.route('/insert')
def insert_Record():
    return render_template('user-input.html')

@app.route('/insert1',methods=['POST','GET'])
def read_form():
    id1=request.form["id"]
    name=request.form["name"]
    print("Id is ",id)
    print("Name is ",name)
    mydb = mysql.connector.connect(
              host="test-1.cbt0glpr7h4n.us-east-1.rds.amazonaws.com",
              user="admin",
              password="kandulaganesh",
              database="TestRDSDB"
           )
    sql = "INSERT INTO Persons (ID, Name) VALUES (%s, %s)"
    val = (id1, name)
    mycursor=mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for('hello_world'))


