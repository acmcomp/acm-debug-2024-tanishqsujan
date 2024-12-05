from flask import Flask

app = Flask(__name__)

@app.route('/hi')
def hi():
    return "hi"

@app.route('/bye')
def bye():
    return "bye"

if __name__ == "__main__":
    app.run(debug=False)

