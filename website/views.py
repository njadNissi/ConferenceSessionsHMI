from flask import Blueprint, render_template, request, flash, jsonify, session, redirect, url_for
# from flask_login import login_required, current_user
import json
import csv, pprint, re
import pandas as pd

SCHEDULES = 'instance/schedule.csv'
STAFF = 'instance/schedule.csv'

views = Blueprint('views', __name__)

##########################DASH BOARDS##########################################################################
@views.route('/', methods=['GET'])
def dashboard():
    """
        Display all the sessions and related inmformations, including details on the lower part of the page
    """
    df = pd.read_csv(SCHEDULES, index_col=0) # leave the id column as the index column
    return render_template("schedule.html", headers=df.columns, body=df.values, total=len(df.values)) 

        
@views.route('/chair/sessions', methods=['GET']) # redirection from auth.login
def chair_sessions():
    """
        returns all the sessions that are to be administered by the logged in session_chair
    """
    user = json.loads(session['user'])
    df = pd.read_csv(SCHEDULES) # include also the iod column
    df = df[df['Chair Id'] == user['staffid']] # select only rows with the given chair id
    df.drop(columns=["Chair Id", 'Chair Full Name'], inplace=True)
    return render_template("schedule_x.html", name=user['username'], headers=df.columns, body=df.values, total=len(df)) # total of sessions for a session chair

##########################DASH SEARCH##########################################################################
@views.route('/sessions/search', methods=['POST'])
def dashboard_search():
    """
        Search from main dashboard or from the session chair's portal
    """
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        df = pd.read_csv(SCHEDULES, index_col=0) # 0th col or 'id' column to be the index 
        body = df[df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]

        if keyword != '': # the request exists
            if 'chair' in request.referrer: # coming from the chair's page
                user = json.loads(session['user'])
                body = body[body['Chair Id'] == user['staffid']] # get the chair's sessions
                return render_template("schedule_x.html", name=user['username'], headers=df.columns, body=body.values) # total of sessions for a session chair
            else: # made from public portal
                return render_template("schedule.html", headers=df.columns, body=body.values)
        else: # case of empty keyword
            return redirect(location=request.referrer)  


@views.route('/chair/sessions/add', methods=['POST'])
def chair_sessions_add():
    """
        returns all the sessions that are to be administered by the logged in session_chair
    """
    if request.method == 'POST': 
        print(request.form)
        user = json.loads(session['user'])
        chair_id = user['staffid']
        chairName = user['username']
        date_time = request.form.get('Date_Time')
        room = request.form.get('Room')
        speaker = request.form.get('Speaker')
        topic = request.form.get('Topic')
        df = pd.read_csv(SCHEDULES)
        df.loc[len(df.index)] = [len(df.index), date_time, chairName, chair_id, room, speaker, topic]
        df.to_csv(SCHEDULES, index=False)    
    return redirect(url_for('views.chair_sessions'))


@views.route('/chair/sessions/remove', methods=['GET'])
def chair_sessions_remove():
    """
        remove a session specified by id
    """
    if request.method == 'GET':
        df = pd.read_csv(SCHEDULES).drop(labels=int(request.args['id'])) # read also id col; ids startb from 1 instead of 0
        """the line bnelow allowes deleting by autoindex and updates indices."""
        # df.reset_index(drop=True, inplace=True, names='id')
        df.to_csv(SCHEDULES, index=False)     
    return redirect(url_for('views.chair_sessions'))