from src.configs.bot_db__config import db
from src.bot__db.models.base_model import BaseModel
from flask_sqlalchemy.query import Query

from sqlalchemy.dialects.postgresql import UUID


class Translation(BaseModel):
    __tablename__ = 'translation'

    phrase_id = db.Column(UUID(as_uuid=True), db.ForeignKey('phrase.identifier'), nullable=False)
    phrase = db.relationship(
        "Phrase",
        foreign_keys=[phrase_id],
        query_class=Query,
        uselist=False,
    )

    language_id = db.Column(UUID(as_uuid=True), db.ForeignKey('language.identifier'), nullable=False)
    language = db.relationship(
        "Language",
        foreign_keys=[language_id],
        query_class=Query,
        uselist=False,
    )

    translation_content = db.Column(db.Text(), nullable=False)

    def __str__(self):
        return self.translation_content
