from src.bot__db.db import db
from src.bot__db.models.base_model import BaseModel


class Currency(BaseModel):
    __tablename__ = 'currency'

    currency_abbr = db.Column(db.String(length=10), nullable=False)
    currency_name = db.Column(db.String(length=100), nullable=False)

    def __str__(self):
        return self.currency_abbr
