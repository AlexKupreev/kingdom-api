from flask_security import RoleMixin

from kingdom_api.extensions import db


class Role(db.Model, RoleMixin):
    """Basic role model
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    permissions = db.Column(db.String(255))

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)

    def __repr__(self):
        return "<Role %s>" % self.username


class RolesUsers(db.Model):
    """roles-users pivot table
    """
    __tablename__ = 'roles_users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
