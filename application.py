from flask import Flask, request, make_response, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Universe!"

@app.route("/webhook")
def webhook():
    #return "Hello from Webhook!"
    #req = request.get_json(silent=True, force=True)
    #try:
    #    action = req.get('queryResult').get('action')
    #except AttributeError:
    #    return 'json error'
    # return a fulfillment response
    return "sneha"
    #{'fulfillmentText': 'This is a response from webhook.'}

if __name__ == "__main__":
    app.run()
