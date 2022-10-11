import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class Cats(db.Model):
    __tablename__ = 'cats'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    breed = db.Column(db.String(100))
    describe = db.Column(db.Text)
    img_url = db.Column(db.Text)
