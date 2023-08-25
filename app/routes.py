from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import SignUpForm, LoginForm, Country
from app.models import User, Visited, Wish_List
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/', methods = ['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = db.session.execute(db.select(User).where(User.username==username)).scalar()
        if user is not None and user.check_password(password):
            login_user(user)
            flash("You have successfully logged in" , "success")
            return redirect(url_for('index'))
        
    elif form.is_submitted():
        flash("Your passwords did not match", "danger")
        return redirect(url_for('login'))
    
    # Sign Up

    form2 = SignUpForm()
    if form2.validate_on_submit():
        first_name = form2.first_name.data
        last_name = form2.last_name.data
        username = form2.username.data
        email = form2.email.data
        password = form2.password.data
        
        check_user = db.session.execute(db.select(User).where( (User.username==username) | (User.email==email) )).scalar()
        if check_user:
            flash('A user with that username already exists', 'danger')
            return redirect(url_for('signup'))
        
        new_user = User(first_name = first_name, last_name = last_name, username = username, email = email, password = password)

        db.session.add(new_user)
        db.session.commit()
        flash(f'{new_user.username} has been created', 'success')

        login_user(new_user)
  
        return redirect(url_for('visited'))
    
    return render_template('index.html', form = form, form2 = form2)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    flash("You have successfully logged out", "success")
    return redirect(url_for('index'))

@app.route('/visited', methods = ['GET', 'POST'])
def visited():
    form = Country()

    if form.validate_on_submit():
        name = form.name.data
        
        check_name = db.session.execute(db.select(Visited).where( (Visited.name==name))).scalar()
        if check_name:
            flash(f'{name} is already in your list', 'danger')
            return redirect(url_for('visited'))
        
        new_country = Visited(name = name, user_id = current_user.id)

        db.session.add(new_country)
        db.session.commit()
        flash(f'You added {new_country.name} to your list!', 'success')
  
        return redirect(url_for('visited'))

    return render_template('visited.html', form = form)