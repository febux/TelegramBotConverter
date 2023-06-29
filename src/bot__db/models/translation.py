from src.bot__db.db import db
from src.bot__db.models.base_model import BaseModel

from sqlalchemy.dialects.postgresql import UUID


class Translation(BaseModel):
    __tablename__ = 'translation'

    phrase_id = db.Column(UUID(as_uuid=True), db.ForeignKey('phrase.identifier'), nullable=False)
    phrase = db.relationship("Phrase", backref=db.backref('translations', lazy='dynamic'))

    language_id = db.Column(UUID(as_uuid=True), db.ForeignKey('language.identifier'), nullable=False)
    language = db.relationship("Language", backref=db.backref('translations', lazy='dynamic'))

    content = db.Column(db.Text(), nullable=False)

    def __str__(self):
        return self.content
