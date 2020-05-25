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
    
    if action == "input.unknown":
        return {"fulfillmentText": "Received Fallback intent"}
    elif action == "input.welcome":
        return {"fulfillmentText": "Received Welcome intent"}
    else:
        return {"fulfillmentText": "Intent not recognized"}
    
    #return {"fulfillmentText": "This is a response from webhook."}
    
@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    return make_response(jsonify(results()))

if __name__ == "__main__":
    app.run()
