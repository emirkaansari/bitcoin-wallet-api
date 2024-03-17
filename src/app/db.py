import os

from databases import Database
from sqlalchemy import (
    Column,
    DateTime,
    MetaData,
    String,
    Table,
    Float,
    Boolean,
    create_engine
)
from sqlalchemy.sql import func

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

transaction = Table(
    "transaction",
    metadata,
    Column("id", String(16), primary_key=True),
    Column("amount", Float),
    Column("spent", Boolean),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

# databases query builder
database = Database(DATABASE_URL)
