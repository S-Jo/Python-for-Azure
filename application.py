from flask import Flask, request, make_response, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

def results():
    # build a request object
    try:
        req = request.get_json(force=True)
    except AttributeError:
        return "No JSON Request is received. Try running the API from Dialogflow"
    
    # fetch action from json
    try:
        action = req.get("queryResult").get("action")
    except AttributeError:
        return "No JSON Request is received. Try running the API from Dialogflow"
    
    if action == "Product":
        product = req.get("queryResult").get("parameters").get("Product")
        filterr = req.get("queryResult").get("parameters").get("Filter")
        return filterr        
    '''   
        return {"fulfillmentText:" + product + " - " + filterr}
    #return {"fulfillmentText": "This is a response from webhook."}
    '''
    
@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    return make_response(jsonify(results()))

if __name__ == "__main__":
    app.run()
