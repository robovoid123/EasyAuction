import sqlalchemy as sa

from app.db.base_class import Base


class User(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    full_name = sa.Column(sa.String, index=True)
    email = sa.Column(sa.String, index=True, nullable=False)
    hashed_password = sa.Column(sa.String, nullable=False)
    is_active = sa.Column(sa.Boolean(), default=True)
    is_superuser = sa.Column(sa.Boolean(), default=False)
