from unicodedata import name
from xml.etree.ElementTree import Comment
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .models import Leave
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():

    leaves = Leave.query.filter_by(userid= current_user.userid)
    return render_template('home.html', user=current_user, leaves= leaves)

@views.route("/managerapproval", methods=['GET', 'POST'])
@login_required
def managerapproval():
    if request.method=='POST':
        #logic for changing the status of the leave to approve or reject 
        print("logic for approval")
        action= request.form.get('action')
        leaveid = request.form.get("leaveid")
        if action =='2':
            print("Rejected ")
            print("leave app id = ", leaveid)
        else:
            print("Approved ")
            print("leave app id = ", leaveid)

    leaves = Leave.query.filter_by(status= 3)
    return render_template('managerapproval.html', user=current_user, leaves= leaves)

@views.route('/rejectleave/<leaveid>')
def rejectleave(leaveid):

    leave = Leave.query.filter_by(leaveid=leaveid).first()
    leave.status = 2
    db.session.commit()

    return redirect(url_for('views.managerapproval'))

@views.route('/approveleave/<leaveid>')
def approveleave(leaveid):

    leave = Leave.query.filter_by(leaveid=leaveid).first()
    leave.status = 1
    db.session.commit()

    return redirect(url_for('views.managerapproval'))



@views.route("/applyleave", methods=['GET', 'POST'])
@login_required
def applyleave():
    if request.method=='POST':
        startdate= request.form.get('startdate')
        enddate= request.form.get('enddate')
        comment= request.form.get('comment')
        # status 3= pending , 2 = rejected , 1 = Approved 
        newleave = Leave(startdate = startdate, enddate=enddate, comment= comment, status=3 , userid= current_user.userid)
        db.session.add(newleave)
        db.session.commit()
        flash("Applied for the leave", category="success")
        return redirect(url_for('views.home'))
    else:
        return render_template('applyleave.html', user=current_user)
