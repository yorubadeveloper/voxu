from flask import Blueprint, render_template, current_app

from .database import DatabaseConfigurator
from .models import get_http_request_log_table_class

voxu_blueprint = Blueprint('voxu', __name__, url_prefix='/voxu', template_folder='templates')


@voxu_blueprint.route('/logs')
def logs():
    HTTPRequestLog = get_http_request_log_table_class()
    db_session = DatabaseConfigurator(current_app).init_db()
    logs = db_session.query(HTTPRequestLog).all()
    db_session.close()
    return render_template('logs.html', logs=logs)
