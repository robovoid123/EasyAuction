from app.core.config import settings
import sqlalchemy
import databases

database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(settings.SQLALCHEMY_DATABASE_URI,
                                  pool_pre_ping=True)
