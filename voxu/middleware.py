import json
from io import BytesIO

from werkzeug.wrappers import Request, Response

from voxu.models import get_http_request_log_table_class


class RequestResponseLoggingMiddleware:
    def __init__(self, app, db_session):
        self.app = app
        self.HTTPRequestLog = get_http_request_log_table_class()
        self.db_session = db_session

    def __call__(self, environ, start_response):
        # Wrap the incoming environment in a request and handle it
        content_length = environ.get('CONTENT_LENGTH', '0').strip()
        has_body = content_length and content_length != '0'

        request = Request(environ)
        if has_body:
            # Buffer the input stream containing the request body
            input_body = request.get_data()
            # Reset the input stream in the environment to a BytesIO containing the read body
            environ['wsgi.input'] = BytesIO(input_body)
            # Ensure the Request object is rebuilt with the updated input stream
            request = Request(environ)
        else:
            input_body = b''

        # Use the input_body for logging which is now safely buffered
        if request.method == 'POST' and has_body:
            data_to_log = input_body.decode('utf-8')
        else:
            data_to_log = ''
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

        for data in response:
            response_body.append(data)
            yield data

        # Construct the response object
        response_ = Response(
            response=b''.join(response_body),
            status=status_code[0],
            headers=response_headers
        )

        # Log the request and response
        unallowed_extensions_in_path = ['.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.woff',
                                        '.woff2',
                                        '.ttf', '.eot', '.otf', '.map', '.json', 'ico', 'xml', 'txt', 'html', 'csv']
        if any([ext in request.path for ext in unallowed_extensions_in_path]):
            return response

        if request.path != '/voxu/logs':
            self.log_request_response(request, response_, data_to_log)

        return response

    def log_request_response(self, request, response, data_to_log):
        # Create log entry
        log_entry = self.HTTPRequestLog(
            ip_address=request.remote_addr,
            method=request.method,
            url=request.url,
            headers=json.dumps(dict(request.headers)),
            body=data_to_log,
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
