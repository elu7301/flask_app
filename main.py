from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

users = {}

@app.route('/')
def index():
    message = request.args.get('message', '')
    return render_template('index.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user['password_hash'], password):
            return redirect(url_for('dashboard', username=username))
        else:
            message = 'Неверное имя пользователя или пароль'
    return render_template('login.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        newusername = request.form['newusername']
        newpassword = request.form['newpassword']
        confirmpassword = request.form['confirmpassword']

        if newpassword != confirmpassword:
            message = 'Пароли не совпадают'
        elif newusername in users:
            message = 'Пользователь с таким именем уже существует'
        else:
            hashed_password = generate_password_hash(newpassword, method='pbkdf2:sha256', salt_length=16)
            registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            users[newusername] = {
                'password_hash': hashed_password,
                'registration_date': registration_date
            }
            return redirect(url_for('index', message='Вы успешно зарегистрованы, можете войти'))
    return render_template('register.html', message=message)

@app.route('/dashboard')
def dashboard():
    username = request.args.get('username')
    if not username or username not in users:
        return redirect(url_for('login'))

    user_info = users[username]
    return render_template('dashboard.html', username=username, user_login=username,
                           registration_date=user_info['registration_date'])

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
