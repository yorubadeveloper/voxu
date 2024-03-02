from voxu.config import Config
from voxu.database import db, DatabaseConfigurator
from voxu.models import Base, get_http_request_log_table_class


class Voxu:
    def __init__(self, app=None, logging_table_name=Config.logging_table_name, database_url=Config.database_url):
        self.app = app
        self.logging_table_name = logging_table_name
        self.database_url = database_url
        self.database_configurator = None

    def init_app(self, app: Config.app):
        if self.app is None:
            self.app = app

        # Initialize the database
        self.database_configurator = DatabaseConfigurator(logging_table_name=self.logging_table_name, database_url=self.database_url)


        # Import and initialize middleware
        from .middleware import RequestResponseLoggingMiddleware
        app.wsgi_app = RequestResponseLoggingMiddleware(app.wsgi_app)

        self.database_configurator.close_db(app)
