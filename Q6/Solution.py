from flask import Flask, jsonify
from dataclasses import dataclass, asdict
@dataclass
class User:
    name: str
    age: int
app = Flask(__name__)
@app.route("/data", methods=["GET"])
def get_data():
    user = User(name="Alice", age=30)
    return jsonify(asdict(user))
if __name__ == "__main__":
    app.run(debug=True)


