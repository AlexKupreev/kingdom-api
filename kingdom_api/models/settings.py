from kingdom_api.extensions import db


class Settings(db.Model):
    """Basic game settings model
    """

    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)

    # gold earn by 1 non-army unit
    gold_earn = db.Column(db.Float, nullable=False, default=1.0)
    # gold spent by 1 non-army unit
    gold_spent_worker = db.Column(db.Float, nullable=False, default=1.0)
    # gold spend by 1 army unit
    gold_spent_army = db.Column(db.Float, nullable=False, default=1.0)
    # cost to pay new person for joining
    new_person_cost = db.Column(db.Float, nullable=False, default=1.0)
    # probability of winning of 1 army unit vs 1 enemy unit
    win_probability = db.Column(db.Float, nullable=False, default=1.0)
    # probability of robbing by default
    rob_default_probability = db.Column(db.Float, nullable=False, default=0.0)
    # probability of robbing when there are more enemies
    rob_extra_probability = db.Column(db.Float, nullable=False, default=0.1)
    # desired amount of gold per enemy
    enemy_gold = db.Column(db.Float, nullable=False, default=1.0)
    # rate of enemy units increase depending on collected gold
    enemy_increase = db.Column(db.Float, nullable=False, default=1.0)
    # rate of enemy units decrease depending on collected gold
    enemy_decrease = db.Column(db.Float, nullable=False, default=1.0)
    # uncertainty of gold
    uncertain_gold = db.Column(db.Float, nullable=False, default=1.0)
    # uncertainty of population
    uncertain_population = db.Column(db.Float, nullable=False, default=1.0)
    # uncertainty of army
    uncertain_army = db.Column(db.Float, nullable=False, default=1.0)

    def __init__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)

        # initial settings
        self.initials = dict()

    def __repr__(self):
        return "<Settings %s>" % self.id
