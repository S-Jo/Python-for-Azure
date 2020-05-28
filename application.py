from flask import Flask, request, make_response, jsonify, render_template, redirect
import pyodbc

app = Flask(__name__)

@app.route("/")
def hello():
    return "App is working"

def results():
    server = 'tcp:srvforpoc.database.windows.net,1433'
    database = 'DBBotServiceData'
    username = 'srvforpoc'
    password = 'Server@123'
    driver= '{ODBC Driver 17 for SQL Server}'
    cnxn = pyodbc.connect(('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password),timeout=5)
    cursor = cnxn.cursor()
    ans = cursor.execute("SELECT * FROM [dbo].[bot_service] where Fund = 'franklin asian equity fund'")
    row = cursor.fetchone()
    fund = "gyugubi"
    return "AUM for the " + fund + " is " + str(row[1]) + " Crore."
    
@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    return make_response(jsonify({'fulfillmentText': results()}))

if __name__ == "__main__":
    app.run()
