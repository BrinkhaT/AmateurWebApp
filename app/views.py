from flask import render_template, flash, redirect, url_for, jsonify
from app import app, db, models, tasks
from .forms import EditAmateurForm
import requests
import json

@app.route('/')
@app.route('/index')
def index():
	tSet = models.TweetsToRetweet.query.all()
	fSet = models.TwitterFollower.query.all()
	return render_template('index.html', tSet=tSet, fSet=fSet)

@app.route('/twitterAccounts')
def twitterAccounts():
	twAccounts = models.TwitterAccount.query.all()
	return render_template("twitterAccounts.html", twAccounts=twAccounts)

@app.route('/amateurs')
def amateurs():
	amateurs = models.Amateur.query.all()
	return render_template("amateurs.html", amateurs=amateurs)

@app.route('/amateur/<id>')
def amateur(id):
	amateur = models.Amateur.query.get(id)
	resp = []
	if amateur.mdhId:
		resp = requests.get("http://www.mydirtyhobby.com/api/amateurs/?naff=83d6AmAU&amateurId="+amateur.mdhId).json()
	return render_template("amateur.html", amateur=amateur, mdhDetails=resp)

@app.route('/createAmateur', methods=['GET', 'POST'])
def createAmateur():
	form = EditAmateurForm()
	
	if form.validate_on_submit():
		a = models.Amateur(name=form.name.data)
		if(form.tw.data != ''):
			a.tw = form.tw.data
			t = models.TwitterFollower(twName=form.tw.data, twConfig=2)
			db.session.add(t)

		if(form.vxId.data != ''):
			a.vxId = form.vxId.data

		if(form.mdhId.data != ''):
			a.mdhId = form.mdhId.data

		if(form.pmId.data != ''):
			a.pmId = form.pmId.data

		if(form.subDomain.data != ''):
			a.subDomain = form.subDomain.data
			
		db.session.add(a)
		db.session.commit()
		flash('Der Eintrag wurde erstellt')
		return redirect(url_for("amateurs"))
	return render_template('createAmateur.html', form=form)
	
@app.route('/editAmateur/<id>', methods=['GET', 'POST'])
def editAmateur(id):
	form = EditAmateurForm()
	a = models.Amateur.query.get(id)
	if form.validate_on_submit():
		a.name = form.name.data
		if(form.tw.data != ''):
			a.tw = form.tw.data
		else:
			a.tw = None

		if(form.vxId.data != ''):
			a.vxId = form.vxId.data
		else:
			a.vxId = None

		if(form.mdhId.data != ''):
			a.mdhId = form.mdhId.data
		else:
			a.mdhId = None

		if(form.pmId.data != ''):
			a.pmId = form.pmId.data
		else:
			a.pmId = None

		if(form.subDomain.data != ''):
			a.subDomain = form.subDomain.data
		else:
			a.subDomain = None

		db.session.add(a)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for("amateur", id=a.id))
	else:
		form.name.data = a.name
		form.tw.data = a.tw
		form.mdhId.data = a.mdhId
		form.vxId.data = a.vxId
		form.pmId.data = a.pmId
		form.subDomain.data = a.subDomain
	return render_template('editAmateur.html', form=form, amateur=a)