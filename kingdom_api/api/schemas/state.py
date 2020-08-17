from kingdom_api.models import State
from kingdom_api.extensions import ma, db


class StateSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)

    class Meta:
        model = State
        sqla_session = db.session
        load_instance = True
