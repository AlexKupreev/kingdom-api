from kingdom_api.extensions import db


class State(db.Model):
    """Basic state model
    """

    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    game = db.relationship("Game", backref=db.backref("states"))

    # gold in a budget
    gold = db.Column(db.Integer, nullable=False, default=0)
    # population in a city
    population = db.Column(db.Integer, nullable=False, default=0)
    # army in a city (<= population)
    army = db.Column(db.Integer, nullable=False, default=0)
    # enemies around a city
    enemies = db.Column(db.Integer, nullable=False, default=0)
    # notifications on the state
    notifications = db.Column(db.Text, nullable=False, default="")
    # reaction move
    reaction_move = db.Column(db.Text, nullable=True, default=None)

    def __init__(self, **kwargs):
        super(State, self).__init__(**kwargs)

    def __repr__(self):
        return "<State %s>" % self.id
