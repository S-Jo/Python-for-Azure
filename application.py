from flask import Flask, request, make_response, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

def results():
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    try:
        action = req.get("queryResult").get("action")
    except AttributeError:
        return "JSON Request is not sent to the server"

    # return a fulfillment response
    return {'fulfillmentText': 'This is a response from webhook.'}

@app.route("/Webhook", methods=['GET', 'POST'])
def webhook():
    return make_response(jsonify(results()))
    #return jsonify("Webhook Successfull")

if __name__ == "__main__":
    app.run()
