from datetime import datetime
import uuid

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.dialects.postgresql import UUID

from src.bot__db.db import db


class BaseModel(db.Model, SerializerMixin):
    __abstract__ = True

    identifier = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow())
