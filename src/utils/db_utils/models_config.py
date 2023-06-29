from pydantic import BaseModel


class DbConfig(BaseModel):
    uri: str
    track_mod: bool = False
    pool_recycle: int = 60
    pool_pre_ping: bool = True
    record_queries: bool = True


class AdminConfig(BaseModel):
    panel_name: str = 'db'
    admin_swatch: str = 'cerulean'
