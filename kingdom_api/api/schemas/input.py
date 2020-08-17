from kingdom_api.extensions import ma


class InputSchema(ma.Schema):

    increase_population = ma.Int(required=False)
    increase_army = ma.Int(required=False)

    class Meta:
        # Include unknown fields in the deserialized output
        # unknown = ma.INCLUDE
        pass
