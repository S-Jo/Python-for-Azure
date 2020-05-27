from flask import Flask, request, make_response, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

def results():
	req = request.get_json(force=True)
	action = req.get("queryResult").get("action")    
    	return {"fulfillmentText": "This is a response from webhook."}
    
@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    return make_response(jsonify(results()))

if __name__ == "__main__":
    app.run()
