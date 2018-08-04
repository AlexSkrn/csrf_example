import os
import base64
import uuid

from flask import Flask, request, session
from model import Grade

app = Flask(__name__)
# app.secret_key = os.environ.get('SECRET_KEY').encode()
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'GET':
        session['csrf_token'] = str(uuid.uuid4())
        # print(session['csrf_token'])

    if request.method == 'POST':
        # if request.form['csrf_token'] == session['csrf_token']:
        # Using the instructor's solution
        if request.form.get('csrf_token', None) == session['csrf_token']:
            g = Grade(
                student=request.form['student'],
                assignment=request.form['assignment'],
                grade=request.form['grade'],
            )
            # print("(" + request.form['grade'] + ")")
            g.save()
        # else:
        #     print("""test not passed with session['csrf_token'] being {}
        #     and request.form['csrf_token'] being {}""".format(session['csrf_token'],
        #     request.form['csrf_token']))

    body = """
<html>
<body>
<h1>Enter Grades</h1>
<h2>Enter a Grade</h2>
<form method="POST">
    <label for="student">Student</label>
    <input type="text" name="student"><br>


    <label for="assignment">Assignment</label>
    <input type="text" name="assignment"><br>

    <label for="grade">Grade</label>
    <input type="text" name="grade"><br>

    <input type="submit" value="Submit">

    <input type="hidden" name="csrf_token" value={}>
</form>

<h2>Existing Grades</h2>
""".format(session['csrf_token'])

    for g in Grade.select():
        body += """
<div class="grade">
{}, {}: {}
</div>
""".format(g.student, g.assignment, g.grade)

    return body


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6779))
    app.run(host='0.0.0.0', port=port)
