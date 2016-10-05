from app import db
import requests
import json

class Amateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    twitter = db.Column(db.String(30))
    mdhId = db.Column(db.String(30))
    mdhLink = db.Column(db.String(120))
    vxId = db.Column(db.String(30))
    pmLink = db.Column(db.String(120))
    subDomain = db.Column(db.String(30))

    def __repr__(self):
        return '<Amateur %r>' % (self.name)

    def getMdhLink(self):
    	if not self.mdhId:
    		return None
    	if self.mdhLink:
    		return self.mdhLink
    	else:
			resp = requests.get("http://www.mydirtyhobby.com/api/amateurs/?naff=83d6AmAU&amateurId="+self.mdhId).json()
			self.mdhLink = resp.get("items")[0].get("url")
			db.session.commit()
        return self.mdhLink