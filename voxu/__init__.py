from voxu.database import DatabaseConfigurator
from voxu.models import Base, get_http_request_log_table_class


class Voxu:
    def __init__(self, app=None):
        self.app = app
        self.database_configurator = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.database_configurator = DatabaseConfigurator(app=app)
        db_session = self.database_configurator.init_db()

        # Import and initialize middleware
        from .middleware import RequestResponseLoggingMiddleware
        app.wsgi_app = RequestResponseLoggingMiddleware(app.wsgi_app, db_session)

        # Import and initialize blueprint
        from .voxu_ui import voxu_blueprint
        app.register_blueprint(voxu_blueprint)

        import atexit
        atexit.register(self.database_configurator.close_db, app, db_session)
