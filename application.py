from flask import Flask, request, make_response, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

def results():
    req = request.get_json(force=True)
    
    # fetch action from json
    try:
        action = req.get("queryResult").get("action")
    except AttributeError:
        return {"JSON Request is not sent to the server"}
    
    return {"fulfillmentText": "This is a response from webhook."}

    '''# build a request object
    req = request.get_json(force=True)

    # fetch action from json
    try:
        action = req.get("queryResult").get("action")
    except AttributeError:
        return "JSON Request is not sent to the server"

    if action == "input.unknown":
        return "Received Fallback intent"
    elif: 
        action == "input.welcome"
        return "Received Welcome intent"
    else:
        return "Intent not recognized"
        '''
    
@app.route("/Webhook", methods=['GET', 'POST'])
def webhook():
    return make_response(jsonify(results()))

if __name__ == "__main__":
    app.run()
