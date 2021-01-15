from flask import Flask,render_template,redirect,request,url_for
import mysql.connector
import json
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

secret_ = None
if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80)

def get_secret():
    secret_name = "dev/beta/myapp"
    region_name = "us-east-1"
    session = boto3.session.Session()
    print("Session established")
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)

@app.route('/')
def index():
    users = read_DB()
    msg = "Users available are "
    html_script = ""
    if len(users) == 0:
	msg = "No Users Available, "
    for user in users:
        html_script = html_script + user[1] + "\n"
    html_script = html_script + "  "
    return "Hello... " + msg + html_script + ",  Click on <a href='/insert'>AddNew</a> to add Users"

def read_DB():
    secrets = get_secret()
    mydb = mysql.connector.connect(
              host=secrets["host"],
              user=secrets["username"],
              password=secrets["password"],
              database=secrets["dbname"]
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
    secrets = get_secret()
    mydb = mysql.connector.connect(
              host=secrets["host"],
              user=secrets["username"],
              password=secrets["password"],
              database=secrets["dbname"]
           )
    sql = "INSERT INTO Persons (ID, Name) VALUES (%s, %s)"
    val = (id1, name)
    mycursor=mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for('index'))


