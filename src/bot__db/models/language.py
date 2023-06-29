from src.bot__db.db import db
from src.bot__db.models.base_model import BaseModel


class Language(BaseModel):
    __tablename__ = 'language'

    language_abbr = db.Column(db.String(length=3), nullable=False)
    language_name = db.Column(db.String(length=50), nullable=True)

    def __str__(self):
        return self.language_abbr
