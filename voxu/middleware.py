from werkzeug.wrappers import Request
from voxu.database import db
from .models import get_http_request_log_table_class


class RequestResponseLoggingMiddleware:
    def __init__(self, app):
        self.app = app
        self.HTTPRequestLog = get_http_request_log_table_class()

    def __call__(self, environ, start_response):
        # Wrap the incoming environment in a request and handle it
        request = Request(environ)
        response = self.app(environ, start_response)

        # Log the request and response
        self.log_request_response(request, response)

        return response

    def log_request_response(self, request, response):
        # Create log entry
        log_entry = self.HTTPRequestLog(
            ip_address=request.remote_addr,
            method=request.method,
            url=request.url,
            headers=dict(request.headers),
            body=request.get_data(as_text=True),
            response_status=response.status,
            response_headers=dict(response.headers),
            response_body=response.get_data(as_text=True)
        )
        db.session.add(log_entry)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        finally:
            db.session.close()
