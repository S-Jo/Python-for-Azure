from flask import Flask, request, make_response, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Universe!"

@app.route("/webhook")
def webhook():
    return "Hello from Webhook!"

if __name__ == "__main__":
    app.run()
