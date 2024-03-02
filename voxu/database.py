from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from voxu.models import get_http_request_log_table_class, Base


class DatabaseConfigurator:

    def __init__(self, app, logging_table_name="http_request_logs", database_url=None):
        self.logging_table_name = logging_table_name
        if database_url is None:
            self.database_url = app.config['SQLALCHEMY_DATABASE_URI']
        else:
            self.database_url = database_url

    def init_db(self):
        engine = create_engine(self.database_url)

        # Ensure the table exists
        if not engine.dialect.has_table(engine.connect(), self.logging_table_name):
            HTTPRequestLog = get_http_request_log_table_class(self.logging_table_name)
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
