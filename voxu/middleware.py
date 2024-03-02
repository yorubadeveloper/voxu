import json
from werkzeug.wrappers import Request, Response
from voxu.models import get_http_request_log_table_class


class RequestResponseLoggingMiddleware:
    def __init__(self, app, db_session):
        self.app = app
        self.HTTPRequestLog = get_http_request_log_table_class()
        self.db_session = db_session

    def __call__(self, environ, start_response):
        # Wrap the incoming environment in a request and handle it
        request = Request(environ)
        response_body = []
        response_headers = []
        status_code = []
        original_start_response = start_response

        # Define a function to capture response data
        def custom_start_response(status, headers, exc_info=None):
            status_code.append(status)
            response_headers.extend(headers)
            return original_start_response(status, headers, exc_info)

        response = self.app(environ, custom_start_response)

        # Construct the response object
        response_ = Response(
            response=b''.join(response_body),
            status=status_code[0],
            headers=response_headers
        )

        # Log the request and response
        self.log_request_response(request, response_)

        return response

    def log_request_response(self, request, response):
        # Create log entry
        log_entry = self.HTTPRequestLog(
            ip_address=request.remote_addr,
            method=request.method,
            url=request.url,
            headers=json.dumps(dict(request.headers)),
            body=request.get_data(as_text=True),
            response_status=response.status_code,
            response_headers=json.dumps(dict(response.headers)),
            response_body=response.get_data(as_text=True)
        )
        self.db_session.add(log_entry)
        try:
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise e
        finally:
            self.db_session.close()
