import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Notification(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    title = sa.Column(sa.String, index=True, nullable=False)
    detail = sa.Column(sa.String)
    active = sa.Column(sa.Boolean, default=True)
    sender_id = sa.Column(sa.ForeignKey('user.id'), nullable=False)
    reciever_id = sa.Column(sa.ForeignKey('user.id'), nullable=False)

    sender = relationship('User', foreign_keys=[sender_id])
    reciever = relationship('User', foreign_keys=[reciever_id])
