from flask import Blueprint, render_template, request, flash, redirect, url_for, session
# from werkzeug.security import generate_password_hash, check_password_hash
import csv, pprint, json


auth = Blueprint('auth', __name__)

def chk_credentials(id, pwd):
    """
        Returns the name of the session chair, if the name is empty then the login failed.
    """
    UserName = ''
    STAFF_ID = ''
    PWD = ''
    with open('instance/staff.csv') as f:
        reader = csv.reader(f)
        header = next(reader)
        try:
            for row in reader:
                if row[header.index('staff_id')] == id and row[header.index('password')] == pwd:
                    UserName = row[header.index('fullname')]
                    STAFF_ID = id
                    PWD = pwd
                    flash('Logged in successfully!', category='success')
                    # login_user(user, remember=True)
        except RuntimeError:
            print('there was an exception during login...', RuntimeError)
    return UserName
                

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST': # login from browser
        staffid = request.form.get('staffid')
        password = request.form.get('password')
        print(staffid, password, '---->')
        
        UserName = chk_credentials(staffid, password) # check and set global vars
        session['user'] = json.dumps({"username":UserName, "staffid":staffid})
        # session.permanent = True

        if UserName == '':
            flash('Incorrect Credential', category='error')     
            return render_template("login.html") 
        else:
            return redirect(url_for('views.chair_sessions'))
    
    if request.method == 'GET': # already authenticated
        staffid = session['user']
        if staffid != '':
            return redirect(url_for('views.chair_sessions'))  
        else:
            render_template("login.html")

@auth.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        return redirect(url_for('views.dashboard'))
    

@auth.route('/staff', methods=['GET']) # go to login page
def session_chair():
    if 'user' in session:
        return redirect(url_for('auth.login'))
    else:
       return render_template("login.html")