from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.auth.forms import LoginForm, RegistrationForm
from app.auth.model import AuthModel

auth = Blueprint("auth", __name__, template_folder="templates/")
auth_model = AuthModel()

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        result = auth_model.authenticate(form.username.data, form.password.data)
        
        if result['status']:
            session['user_id'] = result['data']['id']
            session['username'] = result['data']['username']
            flash(result['msg'], 'success')
            return redirect(url_for('main'))
        else:
            flash(result['msg'], 'danger')
    
    return render_template("auth/login.html", form=form)

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        result = auth_model.register_user(form.username.data, form.first_name.data, form.second_name.data, form.password.data)
        
        if result['status']:
            flash(result['msg'], 'success')
            return redirect(url_for('main'))
        else:
            flash(result['msg'], 'danger')
    
    return render_template("auth/register.html", form=form)

@auth.route("/logout")
def logout():
    session.clear()
    flash("Вы успешно вышли из системы.", "info")
    return redirect(url_for('main'))