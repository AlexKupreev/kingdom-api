from kingdom_api.models import User
from kingdom_api.extensions import ma, db
from flask_security import hash_password


class HashedPassword(ma.Field):
    """Password field that deserializes to a Version object."""

    def _deserialize(self, value, *args, **kwargs):
        return hash_password(value)

    def _serialize(self, value, *args, **kwargs):
        return str(value)


class UserSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    # password = ma.String(load_only=True, required=True)
    password = HashedPassword(load_only=True, required=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
