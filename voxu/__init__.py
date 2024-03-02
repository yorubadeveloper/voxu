from voxu.database import DatabaseConfigurator
from voxu.models import Base, get_http_request_log_table_class


class Voxu:
    def __init__(self, app=None, logging_table_name="http_request_logs", database_url=None):
        self.app = app
        self.logging_table_name = logging_table_name
        self.database_url = database_url
        self.database_configurator = None

    def init_app(self, app):
        if self.app is None:
            self.app = app

        # Initialize the database
        self.database_configurator = DatabaseConfigurator(app=app, logging_table_name=self.logging_table_name, database_url=self.database_url)
        db_session = self.database_configurator.init_db()


        # Import and initialize middleware
        from .middleware import RequestResponseLoggingMiddleware
        app.wsgi_app = RequestResponseLoggingMiddleware(app.wsgi_app, db_session)

        self.database_configurator.close_db(app, db_session)
