from datetime import datetime
from kingdom_api.extensions import db


class Game(db.Model):
    """Basic game model
    """

    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated = db.Column(db.DateTime, nullable=True, default=None)

    settings = db.relationship("Settings", uselist=False, backref=db.backref("game"))

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)

    def __repr__(self):
        return "<Game %s>" % self.id
