from flask import render_template
from app import app, db, models
import requests
import json

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/readRss')
def redRss():
	resp = requests.get("http://www.mydirtyhobby.com/api/amateurs/?naff=83d6AmAU&limit=10")
	return json.dumps(resp.json())

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