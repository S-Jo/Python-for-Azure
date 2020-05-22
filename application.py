from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Universe!"

@app.route("/webhook")
def webhook():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
