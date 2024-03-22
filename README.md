# VOXU
This Python package provides a request logging and viewing system for Flask applications. It allows developers to log and view HTTP requests made to their web applications, facilitating debugging and monitoring.

## Features:
- Middleware to log incoming requests to a database.
- Configurable database connection and table name.
- Dashboard to view logged requests (coming soon).
- API key authentication for accessing the dashboard (coming soon).
- Pydantic models for data validation and serialization (in-progress).

## Usage:

### Installation:
`pip install voxu`

### Initialization:
Set SQLALCHEMY_DATABASE_URI in your Flask app configuration.
Set the table name for request logs (VOXU_LOG_TABLE) in your Flask app configuration. The default table name is 'http_request_logs'.
```python
from flask import Flask
from voxu import Voxu

app = Flask(__name__)
voxu = Voxu()
voxu.init_app(app)
```
**OR**
```python
from flask import Flask
from voxu import Voxu

app = Flask(__name__)
voxu = Voxu(app)
```
### Access Logs:

Navigate to /logs to view all logged requests in a HTML UI.
Configuration:

Configure the database URL and table name during initialization.
Customize middleware and database settings as needed.

## Contributing:
Contributions are welcome! Feel free to open issues or pull requests for bug fixes, enhancements, or new features.

## License:
This project is licensed under the MIT License - see the LICENSE file for details.

