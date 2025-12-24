from flask import Flask, request, jsonify
import model  # your chatbot logic file

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    reply = model.ask(user_message)  # function already exists in repo
    return jsonify({"response": reply})

@app.route("/")
def home():
    return "ChatBot API Working"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
