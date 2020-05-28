from flask import Flask, request, make_response, jsonify, render_template, redirect
import pyodbc

app = Flask(__name__)

@app.route("/")
def hello():
    return "App is working"

def results(filterr,fundname):
    filtertype = filterr
    fund = fundname
    server = 'srvforpoc.database.windows.net'
    database = 'DBBotServiceData'
    username = 'srvforpoc'
    password = 'Server@123'
    driver= '{ODBC Driver 17 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    ans = cursor.execute("SELECT * FROM [dbo].[bot_service] where Fund = '%s'"%fund)
    row = cursor.fetchone()
    if filtertype == "AUM":
        return "AUM for the " + fund + " is " + str(row[1]) + " Crore."
    elif filtertype == "Expense Ratio":
        return "Expense Ratio for the " + fund + " is " + str(row[2]) + "."
    elif filtertype == "Fund Manager":
        return "Fund Manager for the " + fund + " is " + row[3] + "."
    elif filtertype == "Details":
        return fund + " has AUM of " + str(row[1]) + " Crore, Expense Ratio, " + str(row[2]) + " and managed by " + row[3] +"."
    else:
         return "Something went wrong"

# function for response
def fetchjson():
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    
    if action == "FundAction":
        fund = req.get("queryResult").get("parameters").get("Fund")
        filterr = req.get("queryResult").get("parameters").get("filter")
        res = results(filterr,fund)
        return res
        #return results(filterr,fund)
    else:
        return "Intent not recognized"
    
    #To test local
    '''
    p1 = "Expense Ratio"
    p2 = "franklin asian equity fund"
    return results(p1,p2)
    '''
    
@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    #return make_response(jsonify(fetchjson()))
    #res = fetchjson()
    return make_response(jsonify({'fulfillmentText': fetchjson()}))

if __name__ == "__main__":
    app.run()
    
