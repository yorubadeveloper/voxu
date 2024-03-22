from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from voxu.models import get_http_request_log_table_class, Base


class DatabaseConfigurator:

    def __init__(self, app):
        self.voxu_table = app.config.get('VOXU_LOG_TABLE', 'http_request_logs')
        self.database_url = app.config.get('SQLALCHEMY_DATABASE_URI', None)
        if not self.database_url:
            raise ValueError("SQLALCHEMY_DATABASE_URI is not set in the app's configuration")

    def init_db(self):
        engine = create_engine(self.database_url)

        # Ensure the table exists
        if not engine.dialect.has_table(engine.connect(), self.voxu_table):
            HTTPRequestLog = get_http_request_log_table_class(self.voxu_table)
            Base.metadata.create_all(engine, tables=[HTTPRequestLog.__table__])

        db_session = scoped_session(sessionmaker(autocommit=False,
                                                 autoflush=False,
                                                 bind=engine))
        return db_session

    def close_db(self, app, db_session):
        @app.teardown_appcontext
        def shutdown_session(response_or_exc):
            db_session.remove()
            return response_or_exc
