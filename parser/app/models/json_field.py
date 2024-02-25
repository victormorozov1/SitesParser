import json
import sqlalchemy
from sqlalchemy.ext import mutable


class Json(sqlalchemy.TypeDecorator):
    impl = sqlalchemy.String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)


mutable.MutableDict.associate_with(Json)
