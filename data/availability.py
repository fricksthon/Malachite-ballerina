import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Availability(SqlAlchemyBase):
    __tablename__ = 'availability'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    item_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("items.id"))
    amount = sqlalchemy.Column(sqlalchemy.Integer)

    user = orm.relationship('User')
    item = orm.relationship('Item')