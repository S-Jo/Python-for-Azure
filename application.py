from flask import Flask, request, make_response, jsonify, render_template, redirect
import pyodbc

app = Flask(__name__)

@app.route("/")
def hello():
    return "App is working"

def results(action,filterr,fundname):
    action = action
    filtertype = filterr
    fund = fundname
    server = 'tcp:srvforpoc.database.windows.net,1433'
    database = 'DBBotServiceData'
    username = 'srvforpoc'
    password = 'Server@123'
    driver= '{ODBC Driver 17 for SQL Server}'
    try:
        cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    except pyodbc.Error as err:
        return "Couldn't connect to database"
    cursor = cnxn.cursor()
    ans = cursor.execute("SELECT * FROM [dbo].[bot_service] where Fund = '" + fund + "'")
    row = cursor.fetchone()
    if action == "singlefilter":
        if "AUM" in filtertype:
            return "AUM for the " + fund + " is " + str(row[1]) + " Crore."
        elif "Expense Ratio" in filtertype:
            return "Expense Ratio for the " + fund + " is " + str(row[2]) + "."
        elif "Fund Manager" in filtertype:
            return "Fund Manager for the " + fund + " is " + row[3] + "."
        elif "Details" in filtertype:
            return fund + " has AUM of " + str(row[1]) + " Crore, Expense Ratio is " + str(row[2]) + " and it's managed by " + row[3] +"."
        else:
            return "Something went wrong in action singlefilter"
    elif action == "dualfilter":
        if "AUM and Expense Ratio" in filtertype:
            return fund + " has AUM of " + str(row[1]) + " Crore, Expense Ratio is " + str(row[2]) +"."
        if "AUM and Fund Manager" in filtertype:
            return fund + " has AUM of " + str(row[1]) +  " and it's managed by " + row[3] +"."
        if "Fund Manager and Expense Ratio" in filtertype: 
            return " Expense Ratio of " + fund + " is " + str(row[2]) + " and it's managed by " + row[3] +"."
        else:
            return "Something went wrong in action dualfilter"
    else:
        return "Intent/Action not recognized"

# function for response
def fetchjson():
    
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    
    if action == "singlefilter":
        p1 = str(req.get("queryResult").get("parameters").get("Fund"))
        fund = p1.replace("['","")
        fund = fund.replace("']","")             
        filterr = str(req.get("queryResult").get("parameters").get("Filter"))
        #return filterr
        return results(action,filterr,fund)
    elif action == "dualfilter":
        p1 = str(req.get("queryResult").get("parameters").get("Fund"))
        fund = p1.replace("['","")
        fund = fund.replace("']","")             
        filterr = str(req.get("queryResult").get("parameters").get("FilterDual"))
        #return filterr
        return results(action,filterr,fund)
    elif action == "input.welcome":
        return "Hey! Welcome to Franklin Templeton Voice Assistance. Please ask your question"
    else:
        return "Intent not recognized"
    
    #To test local
    '''
    action = "singlefilter"
    p1 = "Expense Ratio"
    p2 = "franklin asian equity fund"
    return results(action,p1,p2)
    '''
        
@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    #return make_response(jsonify(fetchjson()))
    #res = fetchjson()
    return make_response(jsonify({'fulfillmentText': fetchjson()}))

if __name__ == "__main__":
    app.run()
