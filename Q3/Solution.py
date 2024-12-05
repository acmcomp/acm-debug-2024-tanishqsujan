from flask import Flask, request, render_template_string
app = Flask(__name__)
form_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Submit Form</title>
</head>
<body>
    <h1>Submit Your Name</h1>
    <form action="/submit" method="POST">
        <label for="name">Name:</label>
        <input type="text" id="person_name" name="person_name" required>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""
@app.route('/')
def index():
    return render_template_string(form_template)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.get('person_name', 'Guest')  
    return f"Wassgud, {data}!"

if __name__ == '__main__':
    app.run(debug=True)

