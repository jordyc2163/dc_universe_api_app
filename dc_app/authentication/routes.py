
from flask import Blueprint, render_template, request, redirect, url_for, flash
from dc_app.forms import UserSignInForm, UserSignUpForm
from dc_app.models import User, db, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required


auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserSignInForm()
    form.submit_button.label.text = "Sign In"
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in.', 'auth-success')
                return redirect(url_for('site.home'))
            else:
                flash('You Email/Password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')
    return render_template('signin.html', form = form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserSignUpForm()
    form.submit_button.label.text = "Create Account"
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            faction = dict(form.faction.choices).get(form.faction.data)
            user = User(email, first_name = first_name, last_name = last_name, password = password, faction = faction)

            db.session.add(user)
            db.session.commit()

            flash(f"You have successfully created a user account!", 'user-created')
        
            return redirect(url_for('auth.signin'))
    except:
        raise 
    
    return render_template('signup.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))
