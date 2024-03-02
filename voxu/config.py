from flask import Flask
from pydantic import BaseModel, PostgresDsn


class Config(BaseModel):
    app: Flask = None
    database_url: PostgresDsn
    logging_table_name: str = "http_request_logs"
