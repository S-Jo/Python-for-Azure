from flask import Flask, request, make_response, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    action = req.get('queryResult').get('action')
    
    if action == "Product":
        product = req.get("queryResult").get("parameters").get("Product")
        filterr = req.get("queryResult").get("parameters").get("Filter")
        return {"fulfillmentText": "This is a Product intent"}
    else:
        return {"fulfillmentText": "Intent not recognized"}
    
@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    return make_response(jsonify(results()))

if __name__ == "__main__":
    app.run()
