import sqlalchemy as sa
from app.db.base_class import Base


class Image(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    url = sa.Column(sa.String)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
