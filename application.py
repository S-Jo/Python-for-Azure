from flask import Flask, request, make_response, jsonify, render_template, redirect
import pyodbc

app = Flask(__name__)

@app.route("/")
def hello():
    return "App is working"

def results(action,filterr,fundname,fundmanager,Notes):
    
    action = action
    filtertype = filterr
    fund = fundname
    mgr = fundmanager
    usr_input = Notes
    server = 'tcp:srvforpoc.database.windows.net,1433'
    database = 'DBBotServiceData'
    username = 'srvforpoc'
    password = 'Server@123'
    driver= '{ODBC Driver 17 for SQL Server}'

    try:
        cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    except pyodbc.Error as err:
        return "Couldn't connect to database"
    
    #Single Filter & Dual Filter Intent
    cursor1 = cnxn.cursor()
    query1 = cursor1.execute("SELECT * FROM [dbo].[bot_service] where Fund = '" + fund + "'")
    ans1 = cursor1.fetchone()

    #Funds Under Management    
    cursor2 = cnxn.cursor()
    query2 = cursor2.execute("SELECT Fund FROM [dbo].[bot_service] where [Fund Manager] = '" + mgr + "'")
    ans2 = cursor2.fetchall()
    res = []
    for r in ans2:
        res.append(r[0])

    #Function Logic   
    if action == "singlefilter":
        if "aum" in filtertype.lower():
            return "AUM for the " + fund + " is " + str(ans1[1]) + " Crore."
        elif "expense ratio" in filtertype.lower():
            return "Expense Ratio for the " + fund + " is " + str(ans1[2]) + "."
        elif "fund manager" in filtertype.lower():
            return "Fund Manager for the " + fund + " is " + ans1[3] + "."
        elif "details" in filtertype.lower():
            return fund + " has AUM of " + str(ans1[1]) + " Crore, Expense Ratio is " + str(ans1[2]) + " and it's managed by " + ans1[3] +"."
        else:
            return "Please repeat your question"

    elif action == "dualfilter":
        if "aum and expense ratio" in filtertype.lower():
            return fund + " has AUM of " + str(ans1[1]) + " Crore, Expense Ratio is " + str(ans1[2])
        if "aum and fund manager" in filtertype.lower():
            return fund + " has AUM of " + str(ans1[1]) +  " and it's managed by " + ans1[3] +"."
        if "fund manager and expense ratio" in filtertype.lower(): 
            return "Expense Ratio of " + fund + " is " + str(ans1[2]) + " and it's managed by " + ans1[3] +"."
        else:
            return "Please repeat your question"

    elif action == "Funds&Manager":
        if len(res) == 1:
            return mgr + " manages only one fund and that is " + str(res)
        elif len(res) > 1:
            return mgr + " manages " + str(len(res)) + " funds and they are " + str(res)
        else:
            return "Please repeat your question"

    elif action == "TakeNotes":
        cursor3 = cnxn.cursor()
        cursor3.execute("insert into dbo.user_input values ('" + usr_input + "', getdate())")
        #("insert into dbo.user_input values ('" + usr_input + "')")
        cnxn.commit()
        return "Done"

    else:
        return "I need more training to answer it. Kindly help me by repeating your question."

#This method handles the http requests for the Dialogflow webhook
#and meant to be used in conjunction with the Dialogflow agent
def fetchjson():
    req = request.get_json(force=True)
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'

    fundname = str(req.get("queryResult").get("parameters").get("Fund"))
    fund = fundname.replace("['","")
    fund = fund.replace("']","")  

    if action == "singlefilter":
        filterr = str(req.get("queryResult").get("parameters").get("Filter"))
        #return filterr
        return results(action,filterr,fund,"","")

    elif action == "dualfilter":            
        filterr = str(req.get("queryResult").get("parameters").get("FilterDual"))
        #return filterr
        return results(action,filterr,fund,"","")

    elif action == "Funds&Manager":
        mgr = str(req.get("queryResult").get("parameters").get("FundManager"))
        return results(action,"","",mgr,"")

    elif action == "TakeNotes":
        user_input = str(req.get("queryResult").get("parameters").get("WriteBack"))
        comment = user_input.replace("take notes ","")
        return results(action,"","","",comment)

    elif action == "input.welcome":
        return "Greetings from Franklin Voice. How may I assit you?"

    else:
        return "Intent not recognized"
    
    #To test locally
    '''
    action = "TakeNotes"
    notes = "Hello Franklin"
    Mgr = "Roshi Jain"
    p1 = "expense ratio"
    p2 = "franklin asian equity fund"
    #return results(action,p1,p2,"")
    return results(action,"","","",notes)
    '''

@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    #return make_response(jsonify(fetchjson()))
    #res = fetchjson()
    return make_response(jsonify({'fulfillmentText': fetchjson()}))

if __name__ == "__main__":
    app.run()
