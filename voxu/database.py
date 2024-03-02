from flask_sqlalchemy import SQLAlchemy

from voxu.config import Config
from voxu.models import get_http_request_log_table_class

db = SQLAlchemy()


class DatabaseConfigurator:

    def __init__(self, logging_table_name=Config.logging_table_name, database_url=Config.database_url):
        self.logging_table_name = logging_table_name
        self.database_url = database_url
        db.init_app(Config.app)
        Config.app.config['SQLALCHEMY_DATABASE_URI'] = self.database_url

    def init_db(self):
        with db.engine.connect() as connection:
            # Ensure the table exists
            if not connection.dialect.has_table(connection, self.logging_table_name):
                HTTPRequestLog = get_http_request_log_table_class(self.logging_table_name)
                db.session.create_all(bind=connection.engine, tables=[HTTPRequestLog.__table__])

    def close_db(self, app):
        @app.teardown_appcontext
        def shutdown_session(response_or_exc):
            db.session.remove()
            return response_or_exc
