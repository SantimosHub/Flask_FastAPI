from flask import Flask, render_template, request, redirect, make_response

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('input_form.html')


@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    email = request.form['email']

    response = make_response(redirect('/welcome'))
    response.set_cookie('username', username)
    response.set_cookie('email', email)
    return response


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/logout')
def logout():
    response = make_response(redirect('/'))
    response.set_cookie('username', '', expires=0)
    response.set_cookie('email', '', expires=0)
    return response


if __name__ == '__main__':
    app.run(debug=True)