from flask import render_template, flash, redirect, url_for, jsonify
import requests

from app import app, db, models, tasks, AmateurHelper

from .forms import EditAmateurForm


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

@app.route('/amateur/<amateurId>')
def amateur(amateurId):
	amateur = models.Amateur.query.get(amateurId)
	return render_template("amateur.html", amateur=amateur)

@app.route('/createAmateur', methods=['GET', 'POST'])
def createAmateur():
	form = EditAmateurForm()
	
	if form.validate_on_submit():
		AmateurHelper.createAmateur(form)
		
		flash('Der Eintrag wurde erstellt')
		return redirect(url_for("amateurs"))
	return render_template('createAmateur.html', form=form)
	
@app.route('/editAmateur/<amateurId>', methods=['GET', 'POST'])
def editAmateur(amateurId):
	form = EditAmateurForm()
	a = models.Amateur.query.get(amateurId)
	if form.validate_on_submit():
		a.name = form.name.data
		AmateurHelper.updateAmateur(a, form)
		
		flash('Your changes have been saved.')
		return redirect(url_for("amateur", amateurId=a.id))
	else:
		form.name.data = a.name
		form.tw.data = a.tw
		form.mdhId.data = a.mdhId
		form.vxId.data = a.vxId
		form.pmId.data = a.pmId
		form.subDomain.data = a.subDomain
	return render_template('editAmateur.html', form=form, amateur=a)
	
# Routen fuer das Starten der Jobs
@app.route('/jobs')
def jobs():
	return render_template('jobs.html')

@app.route('/jobCheckFollowerForUpdates')
def jobCheckFollowerForUpdates():
	tasks.checkFollowerForUpdates()
	flash('Job checkFollowerForUpdates abgeschlossen')
	return redirect(url_for("index"))
	
@app.route('/jobRetweetAndDeleteTweets')
def jobRetweetAndDeleteTweets():
	tasks.retweetAndDeleteTweets()
	flash('Job retweetAndDeleteTweets abgeschlossen')
	return redirect(url_for("index"))