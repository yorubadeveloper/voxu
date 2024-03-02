from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

from voxu.database import db

Base = declarative_base()


def get_http_request_log_table_class(table_name='http_request_logs'):
    class HTTPRequestLog(db.Model):
        __tablename__ = table_name
        id = Column(Integer, primary_key=True)
        method = Column(String(10))
        ip_address = Column(String(15))
        url = Column(Text)
        headers = Column(Text)
        body = Column(Text)
        response_status = Column(Integer)
        response_headers = Column(Text)
        response_body = Column(Text)
        timestamp = Column(DateTime, default=datetime.utcnow)

    return HTTPRequestLog
