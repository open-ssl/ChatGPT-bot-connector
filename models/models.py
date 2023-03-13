from datetime import datetime

from sqlalchemy import (
    MetaData, Column, Table, Integer, Float, String, DateTime
)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("first_name", String, nullable=True),
    Column("last_name", String, nullable=True),
    Column("username", String, nullable=True),
    Column("language", String),
    Column("temperature", Float),
    Column("registered_at", DateTime),
)

sub_info = Table(
    "sub_info",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("activity_status", Integer),
    Column("started_at", DateTime, nullable=False),
    Column("expired_at", DateTime, nullable=True),
    Column("request_count", Integer, default=0),
    Column("tokens", Integer, default=50000),
)

sub_archive = Table(
    "sub_archive",
    metadata,
    Column("user_id", Integer),
    Column("started_at", DateTime),
    Column("finished_at", DateTime),
    Column("request_count", Integer),
)
