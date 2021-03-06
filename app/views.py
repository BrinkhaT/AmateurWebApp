from flask import render_template, flash, redirect, url_for, jsonify, make_response
import requests

from app import app, db, models, tasks, AmateurHelper, rssHelper

from .forms import AmateurForm, TwitterFollowerForm


@app.route('/')
@app.route('/index')
def index():
	tSet = db.session.query(models.TweetsToRetweet).filter(models.TweetsToRetweet.twConfig == 1).all()
	fSet = db.session.query(models.TwitterFollower).filter(models.TwitterFollower.twConfig == 1).all()
	return render_template('index.html', tSet=tSet, fSet=fSet)

@app.route('/twitterAccounts')
def twitterAccounts():
	twAccounts = models.TwitterAccount.query.all()
	return render_template("twitterAccounts.html", twAccounts=twAccounts)

@app.route('/tweetsToRetweet')
@app.route('/tweetsToRetweet/<int:page>')
def tweetsToRetweet(page=1):
	tSet = models.TweetsToRetweet.query.paginate(page, 10, False)
	return render_template("tweetsToRetweet.html", tSet=tSet)

@app.route('/twitterFollower')
@app.route('/twitterFollower/<int:page>')
def twitterFollower(page=1):
	fSet = models.TwitterFollower.query.order_by(models.TwitterFollower.twName).paginate(page, 10, False)
	return render_template("twitterFollower.html", fSet=fSet)

@app.route('/createTwitterFollower', methods=['GET', 'POST'])
def createTwitterFollower():
	form = TwitterFollowerForm()
	form.twConfig.choices = [(t.id, t.twName) for t in models.TwitterAccount.query.all()]
	
	if form.validate_on_submit():
		t = models.TwitterFollower(twName = form.twName.data, twConfig = form.twConfig.data)
		db.session.add(t)
		db.session.commit()
		
		flash('Der Eintrag wurde erstellt')
		return redirect(url_for("twitterFollower"))
	return render_template('editTwitterFollower.html', form=form)

@app.route('/editTwitterFollower/<int:followerId>', methods=['GET', 'POST'])
def editTwitterFollower(followerId):
	form = TwitterFollowerForm()
	form.twConfig.choices = [(t.id, t.twName) for t in models.TwitterAccount.query.all()]
	t = models.TwitterFollower.query.get(followerId)
	
	if form.validate_on_submit():
		t.twName = form.twName.data
		t.twConfig = form.twConfig.data
		db.session.add(t)
		db.session.commit()
		
		flash('Your changes have been saved.')
		return redirect(url_for("twitterFollower"))
	else:
		form.twName.data = t.twName
		form.twConfig.data = t.twConfig
	return render_template('editTwitterFollower.html', form=form)

@app.route('/deleteTwitterFollower/<int:followerId>')
def deleteTwitterFollower(followerId):
	t = models.TwitterFollower.query.get(followerId)
	db.session.delete(t)
	db.session.commit()
	return redirect(url_for("twitterFollower")) 

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
	form = AmateurForm()
	
	if form.validate_on_submit():
		AmateurHelper.createAmateur(form)
		
		flash('Der Eintrag wurde erstellt')
		return redirect(url_for("amateurs"))
	return render_template('editAmateur.html', form=form)
	
@app.route('/editAmateur/<amateurId>', methods=['GET', 'POST'])
def editAmateur(amateurId):
	form = AmateurForm()
	a = models.Amateur.query.get(amateurId)
	if form.validate_on_submit():
		a.name = form.name.data
		AmateurHelper.updateAmateur(a, form)
		
		flash('Your changes have been saved.')
		return redirect(url_for("amateurs"))
	else:
		form.name.data = a.name
		form.tw.data = a.tw
		form.mdhId.data = a.mdhId
		form.vxId.data = a.vxId
		form.pmId.data = a.pmId
		form.pmRef.data = a.pmRef
		form.subDomain.data = a.subDomain
	return render_template('editAmateur.html', form=form, amateur=a)
	
@app.route('/deleteAmateur/<amateurId>')
def deleteAmateur(amateurId):
	a = models.Amateur.query.get(amateurId)
	
	#TODO: hier muss noch die Loeschlogik rein
	
	db.session.delete(a)
	db.session.commit()
	return redirect(url_for("amateurs"))

# Route fuer die Anzeige des Logs
@app.route('/log')
def showLog():
	pathLogFile = app.config['LOG_FILE']
	logFile = reversed(open(pathLogFile).readlines())

	return render_template('showLog.html', logFile=logFile)

@app.route('/rss')
def showRssFeed():
	rssEntries = db.session.query(models.RssItem).order_by(models.RssItem.pubDate.desc()).limit(30).all()
	resp = make_response(render_template('rss.html', rssEntries=rssEntries))
	resp.headers['Content-type'] = 'text/xml; charset=utf-8'
	return resp
	
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

@app.route('/jobLowerCaseTwitterFollower')
def jobLowerCaseTwitterFollower():
	tasks.lowerCaseTwitterFollower()
	flash('Job lowerCaseTwitterFollower() abgeschlossen')
	return redirect(url_for("index"))

@app.route('/jobAddAllTwitterFollower')
def jobAddAllTwitterFollower():
	tasks.addAllTwitterFollower()
	flash('Job addAllTwitterFollower() abgeschlossen')
	return redirect(url_for("index"))

@app.route('/jobRunRssChecks')
def jobRunRssChecks():
	tasks.runRssChecks()
	flash('Job runRssChecks() abgeschlossen')
	return redirect(url_for("index"))