from src.configs.bot_db__config import db
from src.bot__db.models.base_model import BaseModel


class Phrase(BaseModel):
    __tablename__ = 'phrase'

    phrase_key = db.Column(db.String(length=255), nullable=False)
    description = db.Column(db.Text(), nullable=True)

    def __str__(self):
        return self.phrase_key
