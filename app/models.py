from app import db

class Amateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    twitter = db.Column(db.String(30))

    def __repr__(self):
        return '<Amateur %r>' % (self.name)