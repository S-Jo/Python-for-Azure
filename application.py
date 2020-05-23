from flask import Flask, request, make_response, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api/webhook")
def webhook():
    return jsonify("Webhook Successfull")

if __name__ == "__main__":
    app.run()
