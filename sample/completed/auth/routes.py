from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from auth.models import auth_model

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    user_data = auth_model.authenticate_user(username, password)

    if not user_data:
        flash('Неверные логин или пароль')
        return render_template('login.html')

    session['user_id'] = user_data['in_id']
    session['username'] = user_data['login']
    session['user_group'] = user_data['role']

    flash(f'Добро пожаловать, {user_data["login"]}!')
    return redirect(url_for('main_menu'))

# Добавьте этот endpoint
@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return render_template('logout.html')