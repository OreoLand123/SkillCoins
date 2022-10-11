import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class Accounts(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    value = db.Column(db.Integer, nullable=False)
    # attandance = db.Column(db.)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

class Logs(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    acc_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.Integer, db.ForeignKey("reasons.id"), nullable=False)

class Reasons(db.Model):
    __tablename__ = 'reasons'

    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(100), nullable=False)
     

